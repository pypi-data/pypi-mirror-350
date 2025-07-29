import numpy as np
from scipy import stats as st


class VotingRegressor:
    """Implements a voting regressor.

    Takes a list of fitted models and their weights and returns a weighted average of the predictions.
    """

    def __init__(self, models, model_weights=None):
        """Initialize the VotingRegressor object.

        Args:
            models: list of models to be stacked
            model_weights: list of weights for each model. Default is None.
        """
        self.models = models
        self.model_weights = model_weights

    def predict(self, X):
        """Predict the target variable using the fitted models.

        Args:
            X: input features

        Returns:
            y_pred: predicted target variable
        """
        y_preds = []
        for model in self.models:
            y_pred = model.predict(X)
            y_preds.append(y_pred)

        return np.average(y_preds, axis=0, weights=self.model_weights)

    def get_params(self):
        """Get the parameters of the VotingRegressor object.

        Returns:
            params: dictionary of parameters
        """
        return {"models": self.models, "model_weights": self.model_weights}

    def show_models(self, formula=False):
        """Print the models and their weights."""
        for model, weight in zip(self.models, self.model_weights):
            if formula:
                print(
                    f"Model: {model}, Weight: {weight} \n\tFormula: {model.get_formula()}"
                )
            else:
                print(f"Model: {model}, Weight: {weight}")


class VotingClassifier:
    """Implements a hard voting classifier.

    Aggregates predictions from multiple fitted classification models based on
    majority vote (optionally weighted).
    """

    def __init__(self, estimators, weights=None):
        """Initialize the VotingClassifier object for hard voting.

        Args:
            estimators (list): A list of *fitted* classifier objects.
                               Each estimator must have a `predict` method.
            weights (array-like of shape (n_estimators,), optional): Sequence of
                weights (float or int) to weight the occurrences of predicted class
                labels during voting. Uses uniform weights if None. Defaults to None.
        """
        self.estimators = estimators
        self.weights = weights

        if not isinstance(estimators, list) or not estimators:
            raise ValueError(
                "`estimators` must be a non-empty list of fitted classifiers."
            )

        if weights is not None:
            if len(weights) != len(estimators):
                raise ValueError(
                    f"Number of estimators ({len(estimators)}) and weights ({len(weights)}) must be equal"
                )
            if not isinstance(weights, list | np.ndarray):
                raise TypeError("`weights` must be array-like or None.")
            self.weights = np.asarray(weights)  # Ensure numpy array for calculations

        # Check if all estimators have a predict method
        for est in self.estimators:
            if not hasattr(est, "predict"):
                raise TypeError(
                    f"Estimator {type(est).__name__} does not implement a predict method."
                )

        self.classes_ = (
            None  # Can be inferred during predict if needed, or assumed consistent
        )

    def predict(self, X):
        """Predict class labels for X using hard voting.

        Args:
            X (array-like of shape (n_samples, n_features)): The input samples.

        Returns:
            maj (np.ndarray of shape (n_samples,)): Predicted class labels based on majority vote.
        """
        # Get predictions from all estimators
        # Ensure predictions are numpy arrays and handle potential variations in output shape
        predictions_list = []
        for est in self.estimators:
            pred = est.predict(X)
            # Ensure it's a numpy array and flatten if necessary (e.g., if predict returns (n, 1))
            predictions_list.append(np.asarray(pred).ravel())

        # Stack predictions horizontally: rows are samples, columns are estimators
        predictions = np.vstack(predictions_list).T  # Shape: (n_samples, n_estimators)

        # Infer classes from the unique values in the predictions if not set
        if self.classes_ is None:
            self.classes_ = np.unique(predictions)

        # Find the majority vote for each sample
        if self.weights is None:
            # Simple majority vote using scipy.stats.mode
            # Note: mode returns mode and count, we only need the mode
            # 'keepdims=False' ensures output is (n_samples,)
            maj, _ = st.mode(predictions, axis=1, keepdims=False)
            # If mode returns multiple values (tie), it picks the smallest.
            # Ensure the output type is consistent (e.g., int)
            maj = maj.astype(self.classes_.dtype)

        else:
            # Weighted majority vote
            # We need to iterate sample by sample or use a more complex approach if classes are not 0,1,..
            # Assuming classes are integers that can be used for bincount
            n_samples = X.shape[0]
            maj = np.zeros(n_samples, dtype=self.classes_.dtype)  # Ensure correct dtype
            unique_classes = np.unique(predictions)  # Find unique predicted labels

            for i in range(n_samples):
                sample_preds = predictions[i, :]
                # Weighted counts for each class present in this sample's predictions
                weighted_counts = dict.fromkeys(unique_classes, 0.0)
                for k, pred_class in enumerate(sample_preds):
                    weighted_counts[pred_class] += self.weights[k]

                # Find the class with the maximum weighted count
                maj[i] = max(weighted_counts, key=weighted_counts.get)

        return maj

    def get_params(self, deep=True):
        """Get parameters for this estimator.

        Args:
            deep (bool, optional): If True, will return the parameters for this
                estimator and contained subobjects that are estimators. (Not fully implemented for deep=True yet).

        Returns:
            params (dict): Parameter names mapped to their values.
        """
        # Basic implementation
        return {"estimators": self.estimators, "weights": self.weights}

    def show_models(self):
        """Print the models and their weights."""
        if self.weights is None:
            num_estimators = len(self.estimators)
            weights = (
                [1 / num_estimators] * num_estimators if num_estimators > 0 else []
            )
        else:
            weights = self.weights

        print("VotingClassifier Models (Hard Voting):")
        if not self.estimators:
            print("  No estimators provided.")
            return

        for i, model in enumerate(self.estimators):
            # Attempt to get a meaningful name, fallback to class name
            model_name = getattr(model, "__class__", type(model)).__name__
            print(f"  - Model {i + 1}: {model_name}, Weight: {weights[i]:.3f}")


class ForecastRegressor:
    """Implements a forcast voting regressor.

    Takes a list of fitted models and their weights and returns a weighted average of the predictions.
    """

    def __init__(self, models, model_weights=None):
        """Initialize the ForecastRegressor object.

        Args:
            models: list of models to be stacked
            model_weights: list of weights for each model. Default is None.
        """
        self.models = models
        self.model_weights = model_weights

    def forecast(self, steps):
        """Forecast the target variable using the fitted models.

        Args:
            steps: number of steps to forecast

        Returns:
            y_pred: predicted target variable
        """
        y_preds = []
        for model in self.models:
            y_pred = model.forecast(steps=steps)
            y_preds.append(y_pred)

        return np.average(y_preds, axis=0, weights=self.model_weights)

    def get_params(self):
        """Get the parameters of the ForecastRegressor object.

        Returns:
            params: dictionary of parameters
        """
        return {"models": self.models, "model_weights": self.model_weights}

    def show_models(self, formula=False):
        """Print the models and their weights."""
        for model, weight in zip(self.models, self.model_weights):
            if formula:
                print(
                    f"Model: {model}, Weight: {weight} \n\tFormula: {model.get_formula()}"
                )
            else:
                print(f"Model: {model}, Weight: {weight}")
