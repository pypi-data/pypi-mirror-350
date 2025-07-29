import sys


# Helper function to check if an object is a transformer
def _is_transformer(obj):
    return hasattr(obj, "fit") and hasattr(obj, "transform")


# Helper function to check if an object is an estimator
def _is_estimator(obj):
    return hasattr(obj, "fit") and hasattr(obj, "predict")


class Pipeline:
    """Pipeline of transforms with a final estimator.

    Sequentially apply a list of transforms and a final estimator.
    Intermediate steps of the pipeline must be 'transforms', that is, they
    must implement `fit` and `transform` methods. The final estimator only
    needs to implement `fit`.

    The purpose of the pipeline is to assemble several steps that can be
    cross-validated together while setting different parameters.

    Attributes:
        steps (list): List of (name, transform) tuples (implementing fit/transform)
            that are chained, in the order in which they are chained, with the
            last object an estimator.
        named_steps (dict): Dictionary-like object, with the following items:
            steps (list): List of (name, transform) tuples. Access the steps by name.
        _final_estimator (object): The last step in the pipeline.
    """

    def __init__(self, steps):
        """Initializes the Pipeline.

        Args:
            steps (list): List of (name, transform) tuples (implementing fit/transform)
                          that are chained, with the last step being an estimator.
        """
        self._validate_steps(steps)
        self.steps = steps
        self.named_steps = dict(steps)
        self._final_estimator = steps[-1][1]
        self._is_fitted = False

    def _validate_steps(self, steps):
        """Validate the steps list."""
        if not isinstance(steps, list):
            raise TypeError("steps must be a list.")
        if not all(isinstance(step, tuple) and len(step) == 2 for step in steps):
            raise TypeError("Each step must be a tuple (name, transformer/estimator).")

        # Conditional use of strict argument for zip()
        if sys.version_info >= (3, 10):
            names, estimators = zip(*steps, strict=False)
        else:
            names, estimators = zip(*steps)  # Python < 3.10 doesn't support 'strict'

        # Validate names
        if len(set(names)) != len(names):
            raise ValueError("Names provided for steps must be unique.")
        for name in names:
            if not isinstance(name, str):
                raise TypeError("Step names must be strings.")
            if "__" in name:
                raise ValueError("Step names cannot contain '__'.")

        # Validate transformers and estimator
        transformers = estimators[:-1]
        estimator = estimators[-1]

        for t in transformers:
            if not _is_transformer(t):
                raise TypeError(
                    f"All intermediate steps should be transformers "
                    f"(implementing fit and transform methods), "
                    f"'{type(t).__name__}' does not."
                )

        if not hasattr(estimator, "fit"):
            raise TypeError(
                "Last step of pipeline should implement fit method. "
                f"'{type(estimator).__name__}' does not."
            )

    def _iter(self, with_final=True):
        """Generate (idx, name, transformer) tuples from steps."""
        stop = len(self.steps) if with_final else len(self.steps) - 1
        for idx, (name, trans) in enumerate(self.steps[:stop]):
            yield idx, name, trans

    def _check_is_fitted(self):
        """Check if the pipeline has been fitted."""
        if not self._is_fitted:
            raise RuntimeError(
                "This Pipeline instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator."
            )

    @property
    def _final_estimator_step(self):
        """Returns the final estimator step tuple (name, estimator)."""
        return self.steps[-1]

    @property
    def final_estimator(self):
        """Returns the final estimator instance."""
        return self._final_estimator

    def get_params(self, deep=True):
        """Get parameters for this pipeline.

        Args:
            deep (bool, optional): If True, will return the parameters for this
                estimator and contained subobjects that are estimators. Defaults to True.

        Returns:
            dict: Parameter names mapped to their values.
        """
        params = {"steps": self.steps}
        if deep:
            for name, step in self.steps:
                if hasattr(step, "get_params"):
                    for key, value in step.get_params(deep=True).items():
                        params[f"{name}__{key}"] = value
        return params

    def set_params(self, **params):
        """Set the parameters of this pipeline.

        Args:
            **params: dict, Parameter names mapped to their values.

        Returns:
            self: Pipeline instance.
        """
        if "steps" in params:
            self._validate_steps(params["steps"])
            self.steps = params["steps"]
            self.named_steps = dict(self.steps)
            self._final_estimator = self.steps[-1][1]

        # Set parameters for individual steps
        # For each parameter, check if it belongs to a step and set it accordingly
        step_params = {}
        for key, value in params.items():
            if "__" in key:
                step_name, param_name = key.split("__", 1)
                if step_name not in self.named_steps:
                    raise ValueError(f"Invalid parameter {step_name} for pipeline")
                # Add to dictionary of step-specific parameters
                if step_name not in step_params:
                    step_params[step_name] = {}
                step_params[step_name][param_name] = value

        # For each step, set the parameters
        # If the step has a set_params method, use it; otherwise, set attributes directly
        for name, step_specific_params in step_params.items():
            step = self.named_steps[name]
            if hasattr(step, "set_params"):
                step.set_params(**step_specific_params)
            else:
                # Basic attribute setting as fallback
                for param_name, value in step_specific_params.items():
                    if hasattr(step, param_name):
                        setattr(step, param_name, value)
                    else:
                        raise ValueError(
                            f"Invalid parameter {param_name} for step {name}"
                        )
        return self

    def fit(self, X, y=None, **fit_params):
        """Fit the model with X and y.

        Fits all the transforms one after the other and transforms the
        data, then fits the transformed data using the final estimator.

        Args:
            X (array-like): Training data. Must fulfill input requirements of
                first step of the pipeline.
            y (array-like, optional): Training targets. Must fulfill label requirements for
                all steps of the pipeline.
            **fit_params (dict): Parameters passed to the ``fit`` method of each step,
                where each parameter name is prefixed such that parameter ``p`` for step ``s`` has key ``s__p``.

        Returns:
            self: Pipeline instance.
        """
        self._validate_steps(
            self.steps
        )  # Re-validate steps in case set_params was called

        # Filter fit_params for each step
        fit_params_steps = {name: {} for name, step in self.steps}
        for name, p in fit_params.items():
            step_name, param_name = name.split("__", 1)
            fit_params_steps[step_name][param_name] = p

        Xt = X
        for _, name, transform in self._iter(with_final=False):
            if hasattr(transform, "fit_transform"):
                # Try fit_transform with y, if TypeError, try without y
                try:
                    Xt = transform.fit_transform(Xt, y, **fit_params_steps[name])
                except TypeError:
                    Xt = transform.fit_transform(Xt, **fit_params_steps[name])

            else:
                Xt = transform.fit(Xt, y, **fit_params_steps[name]).transform(Xt)

        # Fit the final estimator
        final_estimator_name, final_estimator = self._final_estimator_step
        if final_estimator is not None:
            try:
                final_estimator.fit(Xt, y, **fit_params_steps[final_estimator_name])
            except TypeError:
                # If the final estimator does not accept y, we need to fit without it
                final_estimator.fit(Xt, **fit_params_steps[final_estimator_name])
        self._is_fitted = True
        return self

    def predict(self, X, **predict_params):
        """Apply transforms to the data, and predict with the final estimator.

        Args:
            X (array-like): Data to predict on. Must fulfill input requirements of
                first step of the pipeline.
            **predict_params (dict): Parameters to the ``predict`` call at the end.
                Note that parameters prefixed with the final estimator name are
                supported.

        Returns:
            y_pred (array-like): Predicted target values.
        """
        self._check_is_fitted()
        Xt = X
        for _, _name, transform in self._iter(with_final=False):
            Xt = transform.transform(Xt)

        # Predict with the final estimator
        return self.final_estimator.predict(Xt, **predict_params)

    def transform(self, X):
        """Apply transforms to the data. Does not use the final estimator.

        Args:
            X (array-like): Data to transform. Must fulfill input requirements of
                first step of the pipeline.

        Returns:
            Xt (array-like): Transformed data.
        """
        self._check_is_fitted()
        Xt = X
        for _, _name, transform in self._iter(with_final=False):
            Xt = transform.transform(Xt)
        return Xt

    def fit_predict(self, X, y=None, **fit_params):
        """Applies fit_predict of last step in pipeline after transforms.

        Applies fit_transforms of a pipeline to the data, followed by the
        fit_predict method of the final estimator in the pipeline. Valid
        only if the final estimator implements fit_predict.

        Args:
            X (array-like): Training data. Must fulfill input requirements of
                first step of the pipeline.
            y (array-like, optional): Training targets. Must fulfill label requirements for
                all steps of the pipeline.
            **fit_params (dict): Parameters passed to the ``fit`` method of each step.

        Returns:
            y_pred (array-like): Result of calling ``fit_predict`` on the final estimator.
        """
        self._validate_steps(self.steps)

        # Filter fit_params for each step
        fit_params_steps = {name: {} for name, step in self.steps}
        for name, p in fit_params.items():
            if "__" in name:
                step_name, param_name = name.split("__", 1)
                if step_name in self.named_steps:
                    fit_params_steps[step_name][param_name] = p

        Xt = X
        for _, name, transform in self._iter(with_final=False):
            if hasattr(transform, "fit_transform"):
                # Try fit_transform with y, if TypeError, try without y
                try:
                    Xt = transform.fit_transform(Xt, y, **fit_params_steps[name])
                except TypeError:
                    Xt = transform.fit_transform(Xt, **fit_params_steps[name])
            else:
                Xt = transform.fit(Xt, y, **fit_params_steps[name]).transform(Xt)

        # Fit and predict with the final estimator
        final_estimator_name, final_estimator = self._final_estimator_step
        if not hasattr(final_estimator, "fit_predict"):
            raise AttributeError(
                "Final estimator of the pipeline must implement fit_predict."
            )

        y_pred = final_estimator.fit_predict(
            Xt, y, **fit_params_steps[final_estimator_name]
        )
        self._is_fitted = True
        return y_pred

    def predict_proba(self, X, **predict_proba_params):
        """Apply transforms, and predict_proba of the final estimator.

        Args:
            X (array-like): Data to predict on. Must fulfill input requirements of
                first step of the pipeline.
            **predict_proba_params (dict): Parameters to the ``predict_proba`` call
                 at the end. Note that parameters prefixed with the final estimator
                 name are supported.

        Returns:
            y_proba (array-like): Predicted probabilities.
        """
        self._check_is_fitted()
        Xt = X
        for _, _name, transform in self._iter(with_final=False):
            Xt = transform.transform(Xt)

        # predict_proba with the final estimator
        if not hasattr(self.final_estimator, "predict_proba"):
            raise AttributeError(
                "Final estimator of the pipeline must implement predict_proba."
            )
        return self.final_estimator.predict_proba(Xt, **predict_proba_params)

    def score(self, X, y=None, sample_weight=None):
        """Apply transforms, estimate score of final estimator.

        Args:
            X (array-like): Data to score. Must fulfill input requirements of
                first step of the pipeline.
            y (array-like, optional): Target values.
            sample_weight (array-like, optional): Sample weights.

        Returns:
            score (float): Score of the pipeline.
        """
        self._check_is_fitted()
        Xt = X
        for _, _name, transform in self._iter(with_final=False):
            Xt = transform.transform(Xt)

        score_params = {}
        if sample_weight is not None:
            score_params["sample_weight"] = sample_weight

        if not hasattr(self.final_estimator, "score"):
            raise AttributeError(
                "Final estimator of the pipeline must implement score."
            )

        return self.final_estimator.score(Xt, y, **score_params)
