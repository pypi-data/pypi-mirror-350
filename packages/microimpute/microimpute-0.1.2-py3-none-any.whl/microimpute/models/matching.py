"""Statistical matching imputation model using hot deck methods."""

from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import validate_call

from microimpute.config import RANDOM_STATE, VALIDATE_CONFIG
from microimpute.models.imputer import Imputer, ImputerResults
from microimpute.utils.statmatch_hotdeck import nnd_hotdeck_using_rpy2

MatchingHotdeckFn = Callable[
    [
        Optional[pd.DataFrame],
        Optional[pd.DataFrame],
        Optional[List[str]],
        Optional[List[str]],
    ],
    Tuple[pd.DataFrame, pd.DataFrame],
]


class MatchingResults(ImputerResults):
    """
    Fitted Matching instance ready for imputation.
    """

    def __init__(
        self,
        matching_hotdeck: MatchingHotdeckFn,
        donor_data: pd.DataFrame,
        predictors: List[str],
        imputed_variables: List[str],
        seed: int,
        hyperparameters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the matching model.

        Args:
            matching_hotdeck: Function that performs the hot deck matching.
            donor_data: DataFrame containing the donor data.
            predictors: List of column names to use as predictors.
            imputed_variables: List of column names to impute.
            seed: Random seed for reproducibility.
            hyperparameters: Optional dictionary of hyperparameters for the
                matching function, specified after tunning.
        """
        super().__init__(predictors, imputed_variables, seed)
        self.matching_hotdeck = matching_hotdeck
        self.donor_data = donor_data
        self.hyperparameters = hyperparameters

    @validate_call(config=VALIDATE_CONFIG)
    def _predict(
        self, X_test: pd.DataFrame, quantiles: Optional[List[float]] = None
    ) -> Dict[float, pd.DataFrame]:
        """Predict imputed values using the matching model.

        Args:
            X_test: DataFrame containing the recipient data.
            quantiles: List of quantiles to predict.

        Returns:
            Dictionary mapping quantiles to imputed values.

        Raises:
            ValueError: If model is not properly set up or
                input data is invalid.
            RuntimeError: If matching or prediction fails.
        """
        from rpy2.robjects import pandas2ri

        try:
            self.logger.info(
                f"Performing matching for {len(X_test)} recipient records"
            )

            # Create a copy to avoid modifying the input
            try:
                self.logger.debug("Creating copy of test data")
                X_test_copy = X_test.copy()

                # Drop imputed variables if they exist in test data
                if any(
                    col in X_test.columns for col in self.imputed_variables
                ):
                    self.logger.debug(
                        f"Dropping imputed variables from test data: {self.imputed_variables}"
                    )
                    X_test_copy.drop(
                        self.imputed_variables,
                        axis=1,
                        inplace=True,
                        errors="ignore",
                    )
            except Exception as copy_error:
                self.logger.error(
                    f"Error preparing test data: {str(copy_error)}"
                )
                raise RuntimeError(
                    "Failed to prepare test data for matching"
                ) from copy_error

            # Perform the matching
            try:
                self.logger.info("Calling R-based hot deck matching function")
                # Call matching function with hyperparameters if available
                if self.hyperparameters:
                    fused0, fused1 = self.matching_hotdeck(
                        receiver=X_test_copy,
                        donor=self.donor_data,
                        matching_variables=self.predictors,
                        z_variables=self.imputed_variables,
                        **self.hyperparameters,
                    )
                else:
                    fused0, fused1 = self.matching_hotdeck(
                        receiver=X_test_copy,
                        donor=self.donor_data,
                        matching_variables=self.predictors,
                        z_variables=self.imputed_variables,
                    )
            except Exception as matching_error:
                self.logger.error(
                    f"Error in hot deck matching: {str(matching_error)}"
                )
                raise RuntimeError(
                    "Hot deck matching failed"
                ) from matching_error

            # Convert R objects to pandas DataFrame
            try:
                self.logger.debug("Converting R result to pandas DataFrame")
                fused0_pd = pandas2ri.rpy2py(fused0)

                # Verify imputed variables exist in the result
                missing_imputed = [
                    var
                    for var in self.imputed_variables
                    if var not in fused0_pd.columns
                ]
                if missing_imputed:
                    self.logger.error(
                        f"Imputed variables missing from matching result: {missing_imputed}"
                    )
                    raise ValueError(
                        f"Matching failed to produce these variables: {missing_imputed}"
                    )

                self.logger.info(
                    f"Matching completed, fused dataset has {len(fused0_pd)} records"
                )
            except Exception as convert_error:
                self.logger.error(
                    f"Error converting matching results: {str(convert_error)}"
                )
                raise RuntimeError(
                    "Failed to process matching results"
                ) from convert_error

            # Create output dictionary with results
            imputations: Dict[float, pd.DataFrame] = {}

            try:
                if quantiles:
                    self.logger.info(
                        f"Creating imputations for {len(quantiles)} quantiles"
                    )
                    # For each quantile, return a DataFrame with all imputed variables
                    for q in quantiles:
                        imputed_df = pd.DataFrame()
                        for variable in self.imputed_variables:
                            self.logger.debug(
                                f"Adding result for imputed variable {variable} at quantile {q}"
                            )
                            imputed_df[variable] = fused0_pd[variable]
                        imputations[q] = imputed_df
                else:
                    # If no quantiles specified, use a default one
                    q = 0.5
                    self.logger.info(
                        f"Creating imputation for default quantile {q}"
                    )
                    imputed_df = pd.DataFrame()
                    for variable in self.imputed_variables:
                        imputed_df[variable] = fused0_pd[variable]
                    imputations[q] = imputed_df

                # Verify output shapes
                for q, df in imputations.items():
                    self.logger.debug(
                        f"Imputation result for q={q}: shape={df.shape}"
                    )
                    if len(df) != len(X_test):
                        self.logger.warning(
                            f"Result shape mismatch: expected {len(X_test)} rows, got {len(df)}"
                        )

                return imputations
            except Exception as output_error:
                self.logger.error(
                    f"Error creating output imputations: {str(output_error)}"
                )
                raise RuntimeError(
                    "Failed to create output imputations"
                ) from output_error

        except ValueError as e:
            # Re-raise validation errors directly
            raise e
        except Exception as e:
            self.logger.error(f"Error during matching prediction: {str(e)}")
            raise RuntimeError(f"Failed to perform matching: {str(e)}") from e


class Matching(Imputer):
    """
    Statistical matching model for imputation using nearest neighbor distance
    hot deck method.

    This model uses R's StatMatch package through rpy2 to perform nearest
    neighbor distance hot deck matching for imputation.
    """

    def __init__(
        self,
        matching_hotdeck: MatchingHotdeckFn = nnd_hotdeck_using_rpy2,
    ) -> None:
        """Initialize the matching model.

        Args:
            matching_hotdeck: Function that performs the hot deck matching.

        Raises:
            ValueError: If matching_hotdeck is not callable
        """
        super().__init__()
        self.logger.debug("Initializing Matching imputer")

        # Validate input
        if not callable(matching_hotdeck):
            self.logger.error("matching_hotdeck must be a callable function")
            raise ValueError("matching_hotdeck must be a callable function")

        self.matching_hotdeck = matching_hotdeck
        self.donor_data: Optional[pd.DataFrame] = None

    @validate_call(config=VALIDATE_CONFIG)
    def _fit(
        self,
        X_train: pd.DataFrame,
        predictors: List[str],
        imputed_variables: List[str],
        tune_hyperparameters: bool = False,
        **matching_kwargs: Any,
    ) -> MatchingResults:
        """Fit the matching model by storing the donor data and variable names.

        Args:
            X_train: DataFrame containing the donor data.
            predictors: List of column names to use as predictors.
            imputed_variables: List of column names to impute.
            matching_kwargs: Additional keyword arguments for hyperparameter
                tuning of the matching function.

        Returns:
            The fitted model instance.

        Raises:
            ValueError: If matching cannot be set up.
        """
        try:
            self.donor_data = X_train.copy()

            if tune_hyperparameters:
                self.logger.info(
                    "Tuning hyperparameters for the matching model"
                )
                best_params = self._tune_hyperparameters(
                    data=X_train,
                    predictors=predictors,
                    imputed_variables=imputed_variables,
                )
                self.logger.info(f"Best hyperparameters: {best_params}")

                return (
                    MatchingResults(
                        matching_hotdeck=self.matching_hotdeck,
                        donor_data=self.donor_data,
                        predictors=predictors,
                        imputed_variables=imputed_variables,
                        seed=self.seed,
                        hyperparameters=best_params,
                    ),
                    best_params,
                )

            else:
                self.logger.info(
                    f"Matching model ready with {len(X_train)} donor records and "
                    f"optional parameters: {matching_kwargs}"
                )
                self.logger.info(f"Using predictors: {predictors}")
                self.logger.info(
                    f"Targeting imputed variables: {imputed_variables}"
                )

                return MatchingResults(
                    matching_hotdeck=self.matching_hotdeck,
                    donor_data=self.donor_data,
                    predictors=predictors,
                    imputed_variables=imputed_variables,
                    seed=self.seed,
                    hyperparameters=matching_kwargs,
                )
        except Exception as e:
            self.logger.error(f"Error setting up matching model: {str(e)}")
            raise ValueError(
                f"Failed to set up matching model: {str(e)}"
            ) from e

    @validate_call(config=VALIDATE_CONFIG)
    def _tune_hyperparameters(
        self,
        data: pd.DataFrame,
        predictors: List[str],
        imputed_variables: List[str],
    ) -> Dict[str, Any]:
        """Tune hyperparameters for the Matching model using Optuna.

        Args:
            X_train: DataFrame containing the training data.
            predictors: List of column names to use as predictors.
            imputed_variables: List of column names to impute.

        Returns:
            Dictionary of tuned hyperparameters.
        """
        import optuna
        from rpy2.robjects import pandas2ri
        from sklearn.model_selection import train_test_split

        # Suppress Optuna's logs during optimization
        optuna.logging.set_verbosity(optuna.logging.WARNING)

        # Create a validation split (80% train, 20% validation)
        X_train, X_test = train_test_split(
            data, test_size=0.2, random_state=self.seed
        )

        def objective(trial: optuna.Trial) -> float:
            params = {
                "dist_fun": trial.suggest_categorical(
                    "dist_fun",
                    [
                        "Manhattan",
                        "Euclidean",
                        "Mahalanobis",
                        "Gower",
                        "minimax",
                    ],
                ),
                "constrained": trial.suggest_categorical(
                    "constrained", [False, True]
                ),
                "constr_alg": trial.suggest_categorical(
                    "constr_alg", ["hungarian", "lpSolve"]
                ),
                "k": trial.suggest_int("k", 1, 10),
            }

            # Track errors for all variables
            var_errors = []

            # For each imputed variable
            for var in imputed_variables:
                # Extract target variable values
                y_test = X_test[var]
                X_test_var = X_test.copy().drop(var, axis=1)

                # Perform the matching with the current parameters
                fused0, fused1 = self.matching_hotdeck(
                    receiver=X_test_var,
                    donor=X_train,
                    matching_variables=predictors,
                    z_variables=[var],
                    **params,
                )

                # Calculate error
                y_pred = pandas2ri.rpy2py(fused0)[var]

                # Normalize error by variable's standard deviation
                std = np.std(y_test.values.flatten())
                mse = np.mean(
                    (y_pred.values.flatten() - y_test.values.flatten()) ** 2
                )
                normalized_mse = mse / (std**2) if std > 0 else mse

                var_errors.append(normalized_mse)

            # Return mean error across all variables
            return np.mean(var_errors)

        # Create and run the study
        study = optuna.create_study(
            direction="minimize",
            sampler=optuna.samplers.TPESampler(seed=self.seed),
        )

        # Suppress warnings during optimization
        import os

        os.environ["PYTHONWARNINGS"] = "ignore"

        study.optimize(objective, n_trials=30)

        best_value = study.best_value
        self.logger.info(f"Lowest average normalized MSE: {best_value}")

        best_params = study.best_params
        self.logger.info(f"Best hyperparameters found: {best_params}")

        return best_params
