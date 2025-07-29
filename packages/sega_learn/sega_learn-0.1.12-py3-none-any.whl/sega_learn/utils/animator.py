import sys
from abc import ABC, abstractmethod

# --- Graceful Matplotlib Import ---
try:
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False
    # Define dummy classes or values for type hinting if needed,
    # but the check in __init__ will prevent their actual use.
    plt = None
    animation = None

import numpy as np

from .dataSplitting import train_test_split
from .decomposition import PCA

# Animation Class
# The goal is to create a reusable and modular animation class that can handle animations for any model and dataset.

# Requirements
#   Modularity:          The class should be reusable for different models and datasets.
#                        Should have base class and subclasses for specific models types (regression, classification, forcasting).
#   Customizability:     Allow users to customize plot elements (e.g., colors, labels, titles).
#   Ease of Use:         Provide a simple interface for creating animations.
#   Support for Metrics: Include functionality to calculate and display metrics like MSE.
#   Saving Options:      Allow saving animations in different formats (e.g., GIF, MP4).
#   Dynamic Updates:     Support dynamic updates of model parameters (e.g., window size).
#   Plot Styling:        Provide options for grid, legends, axis limits, etc.


# High-level Design
#   Base Class:         AnimationBase
#     - Common attributes and methods for all animations.
#     - Methods for setting up the plot, updating the plot, and saving the animation.
#     - Abstract methods for model-specific updates (e.g., update_model, update_plot).
#   Subclasses:         RegressionAnimation, ClassificationAnimation, ForecastingAnimation
#     - Inherit from AnimationBase and implement model-specific updates.
#     - Each subclass can have its own attributes and methods specific to the model type.


class AnimationBase(ABC):
    """Base class for creating animations of machine learning models."""

    def __init__(
        self,
        model,
        train_series,
        test_series,
        dynamic_parameter=None,
        static_parameters=None,
        keep_previous=None,
        **kwargs,
    ):
        """Initialize the animation base class.

        Args:
            model: The forecasting model or any machine learning model.
            train_series: Training time series data.
            test_series: Testing time series data.
            dynamic_parameter: The parameter to update dynamically (e.g., 'window', 'alpha', 'beta').
            static_parameters: Static parameters for the model.
                Should be a dictionary with parameter names as keys and their values.
            keep_previous: Whether to keep all previous lines with reduced opacity.
            **kwargs: Additional customization options (e.g., colors, line styles).
        """
        # --- Check for Matplotlib availability ---
        if not _MATPLOTLIB_AVAILABLE:
            raise ImportError(
                "Matplotlib is required for the Animation features but is not installed. "
                "Please install it using 'pip install matplotlib'."
            )

        # Input validation
        if train_series is None or test_series is None:
            raise ValueError("train_series and test_series must be provided.")
        if dynamic_parameter is None:
            raise ValueError("dynamic_parameter must be provided.")
        if not isinstance(static_parameters, (dict, type(None))):
            raise ValueError("static_parameters must be a dictionary or None.")
        if not isinstance(keep_previous, bool):
            raise ValueError("keep_previous must be a boolean.")

        self.model = model
        self.train_data = train_series
        self.test_data = test_series
        self.dynamic_parameter = dynamic_parameter  # Parameter to update dynamically
        self.static_parameters = (
            static_parameters if static_parameters is not None else {}
        )
        self.keep_previous = keep_previous
        self.kwargs = kwargs

        # Optional metric function (e.g., MSE)
        self.metric_fn = kwargs.get("metric_fn")
        # If self.metric_fn is not a list, convert it to a list
        if self.metric_fn and not isinstance(self.metric_fn, list):
            self.metric_fn = [self.metric_fn]

        # Plot elements
        self.fig, self.ax = None, None
        self.lines = {}
        self.title = None

    def setup_plot(
        self, title, xlabel, ylabel, legend_loc="upper left", grid=True, figsize=(12, 6)
    ):
        """Set up the plot for the animation.

        Args:
            title: Title of the plot.
            xlabel: Label for the x-axis.
            ylabel: Label for the y-axis.
            legend_loc: Location of the legend.
            grid: Whether to show grid lines.
            figsize: Size of the figure.
        """
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if legend_loc is not None:
            # self.ax.legend(loc=legend_loc)
            # Will call legend() in update_plot() to update the legend
            self.add_legend = True
        else:
            self.add_legend = False
        self.ax.grid(grid)
        plt.tight_layout()

    @abstractmethod
    def update_model(self, frame):
        """Abstract method to update the model for a given frame. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def update_plot(self, frame):
        """Abstract method to update the plot for a given frame.Must be implemented by subclasses."""
        pass

    def animate(self, frames, interval=150, blit=True, repeat=False):
        """Create the animation.

        Args:
            frames: Range of frames (e.g., window sizes).
            interval: Delay between frames in milliseconds.
            blit: Whether to use blitting for faster rendering.
            repeat: Whether to repeat the animation.
        """

        def _update(frame):
            self.update_model(frame)
            return self.update_plot(frame)

        self.ani = animation.FuncAnimation(
            self.fig,
            _update,
            frames=frames,
            interval=interval,
            blit=blit,
            repeat=repeat,
        )

        return self.ani

    def save(self, filename, writer="pillow", fps=5, dpi=100):
        """Save the animation to a file.

        Args:
            filename: Path to save the animation.
            writer: Writer to use (e.g., 'pillow' for GIF).
            fps: Frames per second.
            dpi: Dots per inch for the saved figure.
        """
        if not hasattr(self, "ani"):
            raise RuntimeError("Animation has not been created. Call `animate` first.")
        # print(f"Saving animation to {filename} (this may take a while)...")
        # progress_callback = lambda i, n: print(f"Saving frame {i+1}/{n}", end='\r')

        try:
            self.ani.save(filename, writer=writer, fps=fps, dpi=dpi)
            sys.stdout.write("\033[K")  # Clear the line
            print(f"Animation saved successfully to {filename}.")
        except Exception as e:
            sys.stdout.write("\033[K")  # Clear the line on error too
            print(f"\nError saving animation: {e}")

    def show(self):
        """Display the animation."""
        if not hasattr(self, "ani") or self.ani is None:
            raise RuntimeError("Animation has not been created. Call `animate` first.")
        if self.fig is None:
            raise RuntimeError("Plot has not been set up. Call `setup_plot` first.")

        try:
            plt.show()
            print("Animation displayed.")
        except Exception as e:
            print(f"Error showing animation: {e}")
            # Attempt to close the figure if it exists, in case plt.show failed partially
            if self.fig:
                plt.close(self.fig)


class ForcastingAnimation(AnimationBase):
    """Class for creating animations of forecasting models."""

    def __init__(
        self,
        model,
        train_series,
        test_series,
        forecast_steps,
        dynamic_parameter=None,
        static_parameters=None,
        keep_previous=False,
        max_previous=None,
        **kwargs,
    ):
        """Initialize the forecasting animation class.

        Args:
            model: The forecasting model.
            train_series: Training time series data.
            test_series: Testing time series data.
            forecast_steps: Number of steps to forecast.
            dynamic_parameter: The parameter to update dynamically (e.g., 'window', 'alpha', 'beta').
            static_parameters: Static parameters for the model.
                Should be a dictionary with parameter names as keys and their values.
            keep_previous: Whether to keep all previous lines with reduced opacity.
            max_previous: Maximum number of previous lines to keep.
            **kwargs: Additional customization options (e.g., colors, line styles).
        """
        super().__init__(
            model,
            train_series,
            test_series,
            dynamic_parameter,
            static_parameters,
            keep_previous,
            **kwargs,
        )
        self.forecast_steps = forecast_steps
        if self.keep_previous:
            self.previous_forecast_lines = []  # List to store previous forecast lines
            self.previous_fitted_lines = []  # List to store previous fitted lines
            self.max_previous = max_previous

        # Initialize plot elements
        self.train_indices = range(len(train_series))
        self.forecast_indices = range(
            len(train_series), len(train_series) + forecast_steps
        )
        self.fitted_line = None
        self.forecast_line = None

    def setup_plot(
        self, title, xlabel, ylabel, legend_loc="upper left", grid=True, figsize=(12, 6)
    ):
        """Set up the plot for forecasting animation."""
        super().setup_plot(title, xlabel, ylabel, legend_loc, grid, figsize)

        # Plot static elements
        self.ax.plot(
            self.train_indices, self.train_data, label="Training Data", color="blue"
        )
        self.ax.axvline(
            x=len(self.train_data),
            color="black",
            linestyle="--",
            label="Forecast Start",
        )

        # Create placeholders for dynamic lines, with higher zorder
        (self.fitted_line,) = self.ax.plot(
            [], [], label="Fitted Values", color="green", zorder=3
        )
        (self.forecast_line,) = self.ax.plot(
            [], [], label="Forecast", linestyle="--", color="red", zorder=3
        )

        # Auto-adjust y-limits based on the training data range
        min_y = min(self.train_data) - 0.5 * (
            max(self.train_data) - min(self.train_data)
        )
        max_y = max(self.train_data) + 0.5 * (
            max(self.train_data) - min(self.train_data)
        )
        self.ax.set_ylim(min_y, max_y)

        if self.add_legend:
            # Add legend to the plot
            self.ax.legend(loc=legend_loc)

    def update_model(self, frame):
        """Update the model for the current frame.

        Args:
            frame: The current frame (e.g., parameter value).
        """
        # Dynamically update the model with the current frame and include static parameters
        self.model_instance = self.model(
            **{self.dynamic_parameter: frame}, **self.static_parameters
        )
        self.fitted_values = self.model_instance.fit(self.train_data)
        self.forecast_values = self.model_instance.forecast(steps=self.forecast_steps)

    def update_plot(self, frame):
        """Update the plot for the current frame.

        Args:
            frame: The current frame (e.g., parameter value).
        """
        # --- Handle Previous Lines ---
        if self.keep_previous and self.forecast_line and self.fitted_line:
            # Limit the number of previous lines to avoid clutter
            if self.max_previous:
                while len(self.previous_forecast_lines) > self.max_previous:
                    # Remove the oldest line, pop is inplace
                    self.previous_forecast_lines.pop(0)

                while len(self.previous_fitted_lines) > self.max_previous:
                    self.previous_fitted_lines.pop(0)

            # For all previous forecast lines, set alpha from 0.1 to 0.5 based on the number of lines
            self.previous_forecast_lines.append(self.forecast_line)
            for i, line in enumerate(self.previous_forecast_lines):
                line.set_alpha(0.1 + (0.4 / len(self.previous_forecast_lines)) * i)
                line.set_color("lightcoral")

            # For all previous fitted lines, set alpha from 0.1 to 0.5 based on the number of lines
            self.previous_fitted_lines.append(self.fitted_line)
            for i, line in enumerate(self.previous_fitted_lines):
                line.set_alpha(0.1 + (0.4 / len(self.previous_fitted_lines)) * i)
                line.set_color("lightgreen")

            # Add a new fitted line
            (self.fitted_line,) = self.ax.plot(
                [], [], label="Fitted Values", color="green"
            )

        # Update the dynamic lines with the latest fitted and forecasted values
        self.fitted_line.set_data(self.train_indices, self.fitted_values)
        self.forecast_line.set_data(self.forecast_indices, self.forecast_values)

        # Update the title with the current frame and optional metric
        if self.metric_fn:
            if len(self.metric_fn) == 1:
                # If only one metric function is provided, use it directly
                metric_value = self.metric_fn[0](self.test_data, self.forecast_values)

                # Trim values
                metric_value = round(metric_value, 4)
                frame = round(frame, 2)

                self.ax.set_title(
                    f"Forecast ({self.dynamic_parameter}={frame}) - {self.metric_fn[0].__name__.capitalize()}: {metric_value:.4f}"
                )
                print(
                    f"{self.dynamic_parameter}: {frame}, {self.metric_fn[0].__name__.capitalize()}: {metric_value:.4f}",
                    end="\r",
                )

            else:
                # If multiple metric functions are provided, calculate and display each one
                metrics = [
                    metric_fn(self.test_data, self.forecast_values)
                    for metric_fn in self.metric_fn
                ]
                frame = round(frame, 2)

                self.ax.set_title(
                    f"Forecast ({self.dynamic_parameter}={frame}) - {', '.join([f'{fn.__name__.capitalize()}: {metric:.4f}' for fn, metric in zip(self.metric_fn, metrics)])}"
                )
                print(
                    f"{self.dynamic_parameter}: {frame}, {', '.join([f'{fn.__name__.capitalize()}: {metric:.4f}' for fn, metric in zip(self.metric_fn, metrics)])}",
                    end="\r",
                )

        else:
            self.ax.set_title(f"Forecast ({self.dynamic_parameter}={frame})")
            print(f"{self.dynamic_parameter}: {frame}", end="\r")

        # if attribute 'previous_forecast_lines' exists, return it
        if hasattr(self, "previous_forecast_lines"):
            return [self.fitted_line, self.forecast_line] + self.previous_forecast_lines
        else:
            return [self.fitted_line, self.forecast_line]


class RegressionAnimation(AnimationBase):
    """Class for creating animations of regression models."""

    def __init__(
        self,
        model,
        X,
        y,
        test_size=0.3,
        dynamic_parameter=None,
        static_parameters=None,
        keep_previous=False,
        max_previous=None,
        pca_components=1,
        **kwargs,
    ):
        """Initialize the regression animation class.

        Args:
            model: The regression model.
            X: Feature matrix (input data).
            y: Target vector (output data).
            test_size: Proportion of the dataset to include in the test split.
            dynamic_parameter: The parameter to update dynamically (e.g., 'alpha', 'beta').
            static_parameters: Additional static parameters for the model.
                Should be a dictionary with parameter names as keys and their values.
            keep_previous: Whether to keep all previous lines with reduced opacity.
            max_previous: Maximum number of previous lines to keep.
            pca_components: Number of components to use for PCA.
            **kwargs: Additional customization options (e.g., colors, line styles).
        """
        # Input validation
        if X is None or y is None:
            raise ValueError("X and y must be provided.")
        if test_size > 1 or test_size < 0:
            raise ValueError("test_size must be between 0 and 1.")
        if not isinstance(dynamic_parameter, str):
            raise ValueError("dynamic_parameter must be a string.")
        if not isinstance(static_parameters, (dict, type(None))):
            raise ValueError("static_parameters must be a dictionary or None.")
        if not isinstance(keep_previous, bool):
            raise ValueError("keep_previous must be a boolean.")
        if not isinstance(max_previous, (int, type(None))):
            raise ValueError("max_previous must be an integer or None.")
        if not isinstance(pca_components, (int, type(None))) or pca_components < 1:
            raise ValueError("pca_components must be an integer greater than 0.")

        if keep_previous:
            self.max_previous = max_previous

        # Perform PCA if needed before splitting and passing to base
        self.needs_pca = X.shape[1] > 1
        self.pca_instance = None
        if self.needs_pca:
            print(
                f"Input has {X.shape[1]} features. Applying PCA with n_components={pca_components}."
            )
            self.pca_instance = PCA(n_components=pca_components)
            X_transformed = self.pca_instance.fit_transform(X)
            if pca_components == 1:
                X_transformed = X_transformed.reshape(
                    -1, 1
                )  # Ensure 2D array even for 1 component
        else:
            X_transformed = X  # Use original X if no PCA needed

        # Ensure X is 2D
        if X_transformed.ndim == 1:
            X_transformed = X_transformed.reshape(-1, 1)

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X_transformed, y, test_size=test_size, random_state=42
        )
        super().__init__(
            model,
            (X_train, y_train),
            (X_test, y_test),
            dynamic_parameter,
            static_parameters,
            keep_previous,
            **kwargs,
        )

        # Split training and testing data into features and target
        self.X_train, self.y_train = X_train, y_train
        self.X_test, self.y_test = X_test, y_test

        # Initialize plot elements
        self.scatter_points = None
        self.scatter_points_test = None
        self.predicted_line = None

        if self.keep_previous:
            self.previous_predicted_lines = []  # List to store previous predicted lines

    def setup_plot(
        self, title, xlabel, ylabel, legend_loc="upper left", grid=True, figsize=(12, 6)
    ):
        """Set up the plot for regression animation."""
        # Use generic "Feature" label if PCA was applied
        if self.needs_pca and self.pca_instance.n_components == 1:
            effective_xlabel = f"{xlabel} (PCA Component 1)"
        elif self.X_train.shape[1] == 1:
            effective_xlabel = xlabel  # Use original if only 1 feature initially
        else:
            effective_xlabel = "Feature 1"  # Fallback for unexpected cases
            print("Warning: Plotting only the first feature for regression line.")

        super().setup_plot(title, effective_xlabel, ylabel, legend_loc, grid, figsize)

        # Plot static elements (scatter points for training data)
        self.scatter_points = self.ax.scatter(
            self.X_train[:, 0],
            self.y_train,
            label="Training Data",
            color="blue",
            zorder=3,
        )
        # Plot test data points wiht different marker
        self.scatter_points_test = self.ax.scatter(
            self.X_test[:, 0],
            self.y_test,
            label="Test Data",
            color="blue",
            marker="x",
            zorder=3,
        )

        # Create a placeholder for the predicted regression line
        (self.predicted_line,) = self.ax.plot(
            [], [], label="Regression Line", color="red", zorder=3
        )

        if self.add_legend:
            # Add legend to the plot
            self.ax.legend(loc=legend_loc)

    def update_model(self, frame):
        """Update the regression model for the current frame.

        Args:
            frame: The current frame (e.g., parameter value).
        """
        # Dynamically update the model with the current frame and include static parameters
        self.model_instance = self.model(
            **{self.dynamic_parameter: frame}, **self.static_parameters
        )
        self.model_instance.fit(self.X_train, self.y_train)
        # Sort X_test for plotting the line correctly
        sort_indices = np.argsort(self.X_test[:, 0])
        self.X_test_sorted = self.X_test[sort_indices]
        self.predicted_values = self.model_instance.predict(self.X_test_sorted)

    def update_plot(self, frame):
        """Update the plot for the current frame.

        Args:
            frame: The current frame (e.g., parameter value).
        """
        # --- Handle Previous Lines ---
        if self.keep_previous and self.predicted_line:
            # Limit the number of previous lines to avoid clutter (optional)
            if self.max_previous:
                while len(self.previous_predicted_lines) > self.max_previous:
                    # Remove the oldest line, pop is inplace
                    self.previous_predicted_lines.pop(0)

            # For all previous predicted lines, set alpha from 0.1 to 0.5 based on the number of lines
            self.previous_predicted_lines.append(self.predicted_line)
            for i, line in enumerate(self.previous_predicted_lines):
                line.set_alpha(0.1 + (0.4 / len(self.previous_predicted_lines)) * i)
                line.set_color("lightcoral")

            # Add a new predicted line
            (self.predicted_line,) = self.ax.plot(
                [], [], label="Regression Line", color="red"
            )

        # Update the regression line with the predicted values
        self.predicted_line.set_data(self.X_test_sorted[:, 0], self.predicted_values)

        # Update the title with the current frame and optional metrics
        if self.metric_fn:
            # Calculate metrics using the *original* test set order predictions
            y_pred_test_original_order = self.model_instance.predict(self.X_test)
            if len(self.metric_fn) == 1:
                # If only one metric function is provided, use it directly
                metric_value = self.metric_fn[0](
                    self.y_test, y_pred_test_original_order
                )
                metric_value = round(metric_value, 4)
                frame = round(frame, 2)

                self.ax.set_title(
                    f"Regression ({self.dynamic_parameter}={frame}) - {self.metric_fn[0].__name__.capitalize()}: {metric_value:.4f}"
                )
                print(
                    f"{self.dynamic_parameter}: {frame}, {self.metric_fn[0].__name__.capitalize()}: {metric_value:.4f}",
                    end="\r",
                )
            else:
                # If multiple metric functions are provided, calculate and display each one
                metrics = [
                    metric_fn(self.y_test, y_pred_test_original_order)
                    for metric_fn in self.metric_fn
                ]
                frame = round(frame, 2)

                self.ax.set_title(
                    f"Regression ({self.dynamic_parameter}={frame}) - {', '.join([f'{fn.__name__.capitalize()}: {metric:.4f}' for fn, metric in zip(self.metric_fn, metrics)])}"
                )
                print(
                    f"{self.dynamic_parameter}: {frame}, {', '.join([f'{fn.__name__.capitalize()}: {metric:.4f}' for fn, metric in zip(self.metric_fn, metrics)])}",
                    end="\r",
                )
        else:
            self.ax.set_title(f"Regression ({self.dynamic_parameter}={frame})")
            print(f"{self.dynamic_parameter}: {frame}", end="\r")

        return (self.predicted_line,)


class ClassificationAnimation(AnimationBase):
    """Class for creating animations of classification models."""

    def __init__(
        self,
        model,
        X,
        y,
        test_size=0.3,
        dynamic_parameter=None,
        static_parameters=None,
        keep_previous=False,
        scaler=None,
        pca_components=2,
        plot_step=0.02,
        **kwargs,
    ):
        """Initialize the classification animation class.

        Args:
            model: The classification model.
            X: Feature matrix (input data).
            y: Target vector (output data).
            test_size: Proportion of the dataset to include in the test split.
            dynamic_parameter: The parameter to update dynamically (e.g., 'alpha', 'beta').
            static_parameters: Additional static parameters for the model.
                Should be a dictionary with parameter names as keys and their values.
            keep_previous: Whether to keep all previous lines with reduced opacity.
            scaler: Optional scaler for preprocessing the data.
            pca_components: Number of components to use for PCA.
            plot_step: Resolution of the decision boundary mesh.
            **kwargs: Additional customization options (e.g., colors, line styles).
        """
        # Input validation
        if X is None or y is None:
            raise ValueError("X and y must be provided.")
        if test_size > 1 or test_size < 0:
            raise ValueError("test_size must be between 0 and 1.")
        if not isinstance(dynamic_parameter, str):
            raise ValueError("dynamic_parameter must be a string.")
        if not isinstance(static_parameters, (dict, type(None))):
            raise ValueError("static_parameters must be a dictionary or None.")
        if not isinstance(keep_previous, bool):
            raise ValueError("keep_previous must be a boolean.")
        if not isinstance(pca_components, (int, type(None))) or pca_components < 1:
            raise ValueError("pca_components must be an integer greater than 0.")
        if not isinstance(plot_step, float):
            raise ValueError("plot_step must be a float.")

        self.scaler_instance = scaler
        self.pca_instance = None
        self.needs_pca = False

        if self.scaler_instance is not None:
            print("Applying scaler...")
            X = self.scaler_instance.fit_transform(X)

        if X.shape[1] > 2:
            self.needs_pca = True
            print(
                f"Input has {X.shape[1]} features. Applying PCA with n_components={pca_components}."
            )
            if pca_components != 2:
                print(
                    "Warning: Classification animation requires 2 components for plotting. Forcing pca_components=2."
                )
                pca_components = 2
            self.pca_instance = PCA(n_components=pca_components)
            X_transformed = self.pca_instance.fit_transform(X)
        elif X.shape[1] < 2:
            raise ValueError(
                "Classification animation requires at least 2 features or PCA to 2 components."
            )
        else:
            X_transformed = X  # Use original X if 2 features

        X_train, X_test, y_train, y_test = train_test_split(
            X_transformed, y, test_size=test_size, random_state=42
        )
        super().__init__(
            model,
            (X_train, y_train),
            (X_test, y_test),
            dynamic_parameter,
            static_parameters,
            keep_previous,
            **kwargs,
        )

        self.X_train, self.y_train = X_train, y_train
        self.X_test, self.y_test = X_test, y_test

        # Create mesh grid for decision boundary based on *all* transformed data
        x_min, x_max = X_transformed[:, 0].min() - 0.5, X_transformed[:, 0].max()
        y_min, y_max = X_transformed[:, 1].min() - 0.5, X_transformed[:, 1].max()
        self.xx, self.yy = np.meshgrid(
            np.arange(x_min, x_max, plot_step),
            np.arange(y_min, y_max, plot_step),
        )

        # Store unique classes and assign colors
        self.unique_classes = np.unique(y)
        cmap = plt.cm.coolwarm  # Default colormap
        self.colors = cmap(np.linspace(0, 1, len(self.unique_classes)))

        self.scatter_train_dict = {}
        self.scatter_test_dict = {}

        if self.keep_previous:
            self.previous_decision_lines = []  # Store previous decision boundaries

    def setup_plot(
        self, title, xlabel, ylabel, legend_loc="upper left", grid=True, figsize=(12, 6)
    ):
        """Set up the plot for classification animation."""
        # Adjust labels if PCA was used
        effective_xlabel = f"{xlabel} (PCA Comp 1)" if self.needs_pca else xlabel
        effective_ylabel = f"{ylabel} (PCA Comp 2)" if self.needs_pca else ylabel

        super().setup_plot(
            title, effective_xlabel, effective_ylabel, legend_loc, grid, figsize
        )

        # Plot training data points, colored by class
        for i, class_value in enumerate(self.unique_classes):
            class_mask = self.y_train == class_value
            scatter = self.ax.scatter(
                self.X_train[class_mask, 0],
                self.X_train[class_mask, 1],
                color=self.colors[i],
                label=f"Train Class {class_value}",
                edgecolors="k",
                alpha=0.7,
                zorder=2,
            )
            self.scatter_train_dict[class_value] = scatter

        # Plot test data points (optional)
        for i, class_value in enumerate(self.unique_classes):
            class_mask = self.y_test == class_value
            scatter = self.ax.scatter(
                self.X_test[class_mask, 0],
                self.X_test[class_mask, 1],
                color=self.colors[i],
                label=f"Test Class {class_value}",
                marker="x",  # Different marker for test points
                alpha=0.7,
                zorder=2,
            )
            self.scatter_test_dict[class_value] = scatter

        # Set plot limits based on meshgrid
        self.ax.set_xlim(self.xx.min(), self.xx.max())
        self.ax.set_ylim(self.yy.min(), self.yy.max())

        if self.add_legend:
            self.ax.legend(loc=legend_loc)

    def update_model(self, frame):
        """Update the classification model for the current frame.

        Args:
            frame: The current frame (e.g., parameter value).
        """
        # Dynamically update the model with the current frame and include static parameters
        self.model_instance = self.model(
            **{self.dynamic_parameter: frame}, **self.static_parameters
        )
        self.model_instance.fit(self.X_train, self.y_train)

    def update_plot(self, frame):
        """Update the plot for the current frame.

        Args:
            frame: The current frame (e.g., parameter value).
        """
        # Clear the previous decision boundary if it exists
        if hasattr(self, "decision_boundary") and self.decision_boundary:
            for collection in self.decision_boundary.collections:
                collection.remove()

        # Clear the previous decision boundary lines if they exist
        if hasattr(self, "decision_boundary_lines") and self.decision_boundary_lines:
            if self.keep_previous:
                # For all previous decision boundaries, set alpha from 0.1 to 0.5 based on the number of lines
                self.previous_decision_lines.append(self.decision_boundary_lines)
                for i, collection in enumerate(self.previous_decision_lines):
                    collection.set_alpha(
                        0.1 + (0.4 / len(self.previous_decision_lines)) * i
                    )
                    collection.set_color("black")
            else:
                # Remove previous decision boundary lines
                for collection in self.decision_boundary_lines.collections:
                    collection.remove()

        # Predict on the mesh grid
        mesh_points = np.c_[self.xx.ravel(), self.yy.ravel()]
        try:
            # Some models might output probabilities, some classes. Handle both?
            # Assuming .predict gives class labels directly here.
            Z = self.model_instance.predict(mesh_points)
        except AttributeError:
            # Handle models with predict_proba if predict isn't available
            try:
                Z_proba = self.model_instance.predict_proba(mesh_points)
                Z = np.argmax(Z_proba, axis=1)  # Get class with highest probability
                # Need to map back to original class labels if they weren't 0, 1, ...
                if not np.array_equal(
                    self.model_instance.classes_, np.arange(len(self.unique_classes))
                ):
                    Z = self.model_instance.classes_[Z]
            except AttributeError:
                raise AttributeError(
                    f"{self.model.__name__} needs a 'predict' or 'predict_proba' method returning class labels."
                ) from None
        Z = Z.reshape(self.xx.shape)

        # Plot the current decision boundary contourf (filled regions)
        self.decision_boundary = self.ax.contourf(
            self.xx,
            self.yy,
            Z,
            alpha=0.25,
            cmap=plt.cm.coolwarm,  # Use consistent colormap
            levels=np.arange(len(self.unique_classes) + 1)
            - 0.5,  # Center levels between classes
            zorder=1,  # Behind data points
        )

        # If only two classes, plot the decision boundary lines
        if len(np.unique(self.y_train)) == 2:
            # Plot decision boundary lines
            self.decision_boundary_lines = self.ax.contour(
                self.xx,
                self.yy,
                Z,
                levels=[0.5],
                linewidths=1,
                colors="black",
            )

        # Update the title with the current frame and optional metrics
        if self.metric_fn:
            if len(self.metric_fn) == 1:
                # If only one metric function is provided, use it directly
                metric_value = self.metric_fn[0](
                    self.y_test, self.model_instance.predict(self.X_test)
                )
                metric_value = round(metric_value, 4)
                frame = round(frame, 2)

                self.ax.set_title(
                    f"Classification ({self.dynamic_parameter}={frame}) - {self.metric_fn[0].__name__.capitalize()}: {metric_value:.4f}"
                )
                print(
                    f"{self.dynamic_parameter}: {frame}, {self.metric_fn[0].__name__.capitalize()}: {metric_value:.4f}",
                    end="\r",
                )
            else:
                # If multiple metric functions are provided, calculate and display each one
                metrics = [
                    metric_fn(self.y_test, self.model_instance.predict(self.X_test))
                    for metric_fn in self.metric_fn
                ]
                frame = round(frame, 2)

                self.ax.set_title(
                    f"Classification ({self.dynamic_parameter}={frame}) - {', '.join([f'{fn.__name__.capitalize()}: {metric:.4f}' for fn, metric in zip(self.metric_fn, metrics)])}"
                )
                print(
                    f"{self.dynamic_parameter}: {frame}, {', '.join([f'{fn.__name__.capitalize()}: {metric:.4f}' for fn, metric in zip(self.metric_fn, metrics)])}",
                    end="\r",
                )
        else:
            self.ax.set_title(f"Classification ({self.dynamic_parameter}={frame})")
            print(f"{self.dynamic_parameter}: {frame}", end="\r")

        if len(np.unique(self.y_train)) == 2:
            return (
                self.decision_boundary,
                self.decision_boundary_lines,
            )
        else:
            return (self.decision_boundary,)
