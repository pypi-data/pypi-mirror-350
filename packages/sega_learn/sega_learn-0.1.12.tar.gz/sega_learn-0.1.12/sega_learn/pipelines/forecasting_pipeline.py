import numpy as np

from sega_learn.utils.voting import ForecastRegressor


class ForecastingPipeline:
    """A customizable pipeline for time series forecasting.

    This pipeline allows for the integration of preprocessing steps, a forecasting model,
    and evaluation metrics to streamline the forecasting workflow.

    Attributes:
        preprocessors (list): A list of preprocessing functions or objects to transform the input data.
        model (object): A forecasting model (e.g., ARIMA, SARIMA, etc.) that implements fit and predict methods.
        evaluators (list): A list of evaluation metrics or functions to assess the model's performance.

    Methods:
        add_preprocessor(preprocessor): Add a preprocessing step to the pipeline.
        fit(X, y): Fit the model to the data after applying preprocessing steps.
        predict(X): Make predictions using the fitted model and preprocessing steps.
        evaluate(X, y): Evaluate the model using the provided evaluators.
        summary(): Print a summary of the pipeline configuration.
    """

    def __init__(self, preprocessors=None, model=None, evaluators=None):
        """Initialize the pipeline with optional preprocessors, model, and evaluators.

        Args:
            preprocessors (list, optional): List of preprocessing functions or objects.
            model (object, optional): A forecasting model (e.g., ARIMA, SARIMA, etc.).
            evaluators (list, optional): List of evaluation metrics or functions.
        """
        self.preprocessors = preprocessors or []
        self.models = model or []
        self.evaluators = evaluators or []

        # If self.models is not a list, convert it to a list
        if not isinstance(self.models, list):
            self.models = [self.models]

    def add_preprocessor(self, preprocessor):
        """Add a preprocessing step to the pipeline.

        Args:
            preprocessor (callable): A preprocessing function or object.
        """
        self.preprocessors.append(preprocessor)

    def remove_preprocessor(self, preprocessor):
        """Remove a preprocessing step from the pipeline.

        Args:
            preprocessor (callable): A preprocessing function or object to remove.
        """
        if preprocessor in self.preprocessors:
            self.preprocessors.remove(preprocessor)
        else:
            raise ValueError("Preprocessor not found in the pipeline.")

    def add_evaluator(self, evaluator):
        """Add an evaluation metric to the pipeline.

        Args:
            evaluator (callable): An evaluation metric function.
        """
        self.evaluators.append(evaluator)

    def remove_evaluator(self, evaluator):
        """Remove an evaluation metric from the pipeline.

        Args:
            evaluator (callable): An evaluation metric function to remove.
        """
        if evaluator in self.evaluators:
            self.evaluators.remove(evaluator)
        else:
            raise ValueError("Evaluator not found in the pipeline.")

    def add_model(self, model):
        """Add a forecasting model to the pipeline.

        Args:
            model (object): A forecasting model (e.g., ARIMA, SARIMA, etc.).
        """
        if isinstance(model, list):
            self.models.extend(model)
        else:
            self.models.append(model)

    def remove_model(self, model):
        """Remove a forecasting model from the pipeline.

        Args:
            model (object): A forecasting model (e.g., ARIMA, SARIMA, etc.) to remove.
        """
        if model in self.models:
            self.models.remove(model)
        else:
            raise ValueError("Model not found in the pipeline.")

    def fit(self, X, y=None):
        """Fit the model to the data.

        Args:
            X (array-like): Input features (e.g., time series data).
            y (array-like): Target values (optional). If not provided, X is used as both features and target.
        """
        if not self.models:
            raise ValueError("No model has been set in the pipeline.")

        for preprocessor in self.preprocessors:
            # Check if preprocessor is callable
            if callable(preprocessor):
                X, y = preprocessor(X, y)
            else:
                # If preprocessor is an object with fit method, call it
                if hasattr(preprocessor, "fit"):
                    # Fit may take X or X, y depending on the preprocessor
                    try:
                        X, y = preprocessor.fit(X, y)
                    except TypeError:
                        try:
                            # If it raises TypeError, assume it only takes X
                            # and returns transformed X
                            X = preprocessor.fit(X)
                        except Exception as e:
                            raise ValueError(
                                f"Preprocessor fit method failed: {e}"
                            ) from e
                else:
                    raise ValueError(
                        "Preprocessor must be callable or have a fit method."
                    )

            # If preprocessor has introduced any nans, handle them
            if any(np.isnan(X)):
                # Remove the appropriate y values as well
                if y is not None:
                    y = y[~np.isnan(X)]

                # Handle NaNs in the data, drop nans
                X = X[~np.isnan(X)]

        for model in self.models:
            # Check if model is callable
            if hasattr(model, "fit"):
                # Fit the model to the preprocessed data
                # Fit may take X or X, y depending on the model
                try:
                    model.fit(X, y)
                except TypeError:
                    try:
                        # If it raises TypeError, assume it only takes X
                        # and returns transformed X
                        model.fit(X)
                    except Exception as e:
                        raise ValueError(f"Model fit method failed: {e}") from e
            else:
                raise ValueError("Model must have a fit method.")

        # If self.models is longer than 1, use ForecastRegressor
        if len(self.models) > 1:
            self.fit_model = ForecastRegressor(models=self.models)
            # Fit the ForecastRegressor to the preprocessed data
        else:
            self.fit_model = self.models[0]

    def predict(self, X, steps=1):
        """Make predictions using the fitted model.

        Args:
            X (array-like): Input features for prediction.
            steps (int): Number of steps to forecast ahead.

        Returns:
            array-like: Predicted values.
        """
        if not self.models:
            raise ValueError("No model has been set in the pipeline.")

        for preprocessor in self.preprocessors:
            # Check if preprocessor is callable
            if callable(preprocessor):
                X = preprocessor(X)
            else:
                # Check if preprocessor is an object with transform method
                if hasattr(preprocessor, "transform"):
                    X = preprocessor.transform(X)
                else:
                    # Fit only if it has a fit method
                    if hasattr(preprocessor, "fit"):
                        try:
                            X = preprocessor.fit(X)
                        except Exception as e:
                            raise ValueError(
                                f"Preprocessor transform method failed: {e}"
                            ) from e
                    else:
                        raise ValueError(
                            "Preprocessor must be callable or have a transform method."
                        )

        if self.fit_model:
            # Check if model is callable
            if hasattr(self.fit_model, "predict"):
                # Make predictions using the fitted model
                try:
                    return self.fit_model.predict(X, steps)
                except Exception as e:
                    raise ValueError(f"Model predict method failed: {e}") from e
            else:
                # Check if model is an object with forecast method
                if hasattr(self.fit_model, "forecast"):
                    try:
                        return self.fit_model.forecast(steps)
                    except Exception as e:
                        raise ValueError(f"Model forecast method failed: {e}") from e
                else:
                    raise ValueError("Model must have a predict or forecast method.")

        raise ValueError("No model has been set in the pipeline.")

    def evaluate(self, predictions, y):
        """Evaluate the model using the provided evaluators.

        Args:
            predictions (array-like): Predicted values.
            y (array-like): True target values.

        Returns:
            dict: Dictionary of evaluation results.
        """
        if not self.evaluators:
            raise ValueError("No evaluators have been set in the pipeline.")
        if len(predictions) != len(y):
            raise ValueError("Predictions and true values must have the same length.")

        results = {}
        for evaluator in self.evaluators:
            results[evaluator.__name__] = evaluator(y, predictions)
        return results

    def summary(self):
        """Print a summary of the pipeline configuration."""
        print(" " * 12 + "--Forecasting Pipeline--")
        print("-" * 50)

        print("  Preprocessors:", end="")
        for i, preprocessor in enumerate(self.preprocessors):
            if i == 0:
                print(f" {preprocessor.__class__.__name__}")
            else:
                print(" " * 16, end="")
                print(f" {preprocessor.__class__.__name__}")

        print("  Models:", end="")
        for i, model in enumerate(self.models):
            if i == 0:
                print(" " * 7, end="")
                print(f" {model.__class__.__name__}")
            else:
                print(" " * 16, end="")
                print(f" {model.__class__.__name__}")

        print("  Evaluators:", end="")
        for i, evaluator in enumerate(self.evaluators):
            if i == 0:
                print(f"    {evaluator.__name__}")
            else:
                print(" " * 16, end="")
                print(f" {evaluator.__name__}")
        print("-" * 50)
