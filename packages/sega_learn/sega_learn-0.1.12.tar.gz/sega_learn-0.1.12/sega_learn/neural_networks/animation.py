class TrainingAnimator:
    """A utility class to create and manage training animations.

    This class provides callback functions that can be used during model training.
    """

    def __init__(self, figure_size=(18, 10), dpi=100):
        """Initialize the animator with given figure size and DPI.

        Args:
            figure_size: (tuple) - Size of the figure (width, height)
            dpi: (int) - DPI for rendering
        """
        try:
            import matplotlib.pyplot as plt  # noqa: F401
            import numpy as np  # noqa: F401
            from matplotlib.animation import FFMpegWriter, PillowWriter  # noqa: F401
        except ImportError:
            raise ImportError(
                "Matplotlib is required for animation. Please install matplotlib first."
            ) from None

        self.figure_size = figure_size
        self.dpi = dpi
        self.fig = None
        self.axes = None
        self.lines = {}
        self.metrics = {}
        self.writer = None
        self.frame_count = 0
        self.metric_to_ax = {}  # New dictionary to map metrics to axes

    def initialize(self, metrics_to_track, has_validation=False):
        """Initialize the animation with specified metrics.

        Args:
            metrics_to_track: (list) - List of metrics to track
            has_validation: (bool) - Whether validation metrics are available
        """
        import matplotlib.pyplot as plt
        import numpy as np

        # Initialize empty metrics storage
        self.metrics = {metric: [] for metric in metrics_to_track}
        if has_validation:
            self.metrics.update(
                {
                    f"val_{metric}": []
                    for metric in metrics_to_track
                    if metric != "learning_rate"
                }
            )

        # Create figure and axes based on number of metrics
        n_metrics = len(metrics_to_track)
        rows = max(1, (n_metrics + 2) // 3)  # Up to 3 plots per row
        cols = min(n_metrics, 3)

        # Adjust figure size based on number of metrics
        self.fig, self.axes = plt.subplots(rows, cols, figsize=self.figure_size)
        if rows == 1 and cols == 1:
            self.axes = np.array([[self.axes]])
        elif rows == 1 or cols == 1:
            self.axes = np.array([self.axes]).reshape(rows, cols)

        # Map metrics to axes
        for i, metric in enumerate(metrics_to_track):
            row, col = i // 3, i % 3
            ax = self.axes[row, col]
            self.metric_to_ax[metric] = ax  # Add mapping to dictionary

            # Train line
            (self.lines[metric],) = ax.plot([], [], "b-", label=f"Train {metric}")

            # Validation line if needed
            if has_validation and metric != "learning_rate":
                (self.lines[f"val_{metric}"],) = ax.plot(
                    [], [], "r-", label=f"Val {metric}"
                )

            ax.set_title(metric)
            ax.set_xlabel("Epoch")
            ax.set_ylabel("Value")
            ax.legend()
            ax.grid(True)

        self.fig.tight_layout()

        # For blitting - store the background
        self.bg_cache = None

    def update_metrics(self, epoch_metrics, validation=False):
        """Update the stored metrics with new values.

        Args:
            epoch_metrics (dict): Dictionary containing metric values
            validation (bool): Whether these are validation metrics
        """
        for metric, value in epoch_metrics.items():
            key = f"val_{metric}" if validation else metric
            if key in self.metrics:
                self.metrics[key].append(value)

    def animate_training_metrics(
        self,
        interval=200,
        blit=True,
        save_path=None,
        save_format="mp4",
        fps=10,
        dpi=300,
    ):
        """Create an animation of the training metrics.

        Args:
            interval: (int) - Delay between frames in milliseconds
            blit: (bool) - Whether to use blitting for efficient animation
            save_path: (str - optional): Path to save the animation
            save_format: (str) - Format to save animation ('mp4', 'gif', etc.)
            fps: (int) - Frames per second for the saved video
            dpi: (int) - DPI for the saved animation

        Returns:
            animation.FuncAnimation: Animation object
        """
        import numpy as np
        from matplotlib.animation import FuncAnimation

        if self.fig is None:
            raise ValueError("Animation not initialized. Call initialize() first.")

        # Maximum epochs based on available data
        max_epochs = len(next(iter(self.metrics.values())))
        x_data = np.arange(1, max_epochs + 1)

        # Set axis limits
        for i, metric in enumerate(
            [m for m in self.metrics if not m.startswith("val_")]
        ):
            row, col = i // 3, i % 3
            ax = self.axes[row, col]

            # Calculate y limits with some padding
            metric_vals = self.metrics[metric]
            val_metric = f"val_{metric}"
            if val_metric in self.metrics:
                all_vals = metric_vals + self.metrics[val_metric]
                min_val = min(all_vals)
                max_val = max(all_vals)
            else:
                min_val = min(metric_vals)
                max_val = max(metric_vals)

            padding = (max_val - min_val) * 0.1 if max_val > min_val else 0.1
            ax.set_xlim(0, max_epochs + 1)
            ax.set_ylim(min_val - padding, max_val + padding)

        # Initialization function for animation
        def init():
            artists = []
            for _metric, line in self.lines.items():
                line.set_data([], [])
                artists.append(line)
            return artists

        # Update function for animation
        def update(frame):
            artists = []
            current_epoch = frame + 1  # Frame is 0-indexed, epochs are 1-indexed

            for metric, line in self.lines.items():
                if current_epoch <= len(self.metrics[metric]):
                    x = x_data[:current_epoch]
                    y = self.metrics[metric][:current_epoch]
                    line.set_data(x, y)
                artists.append(line)

            return artists

        # Create animation
        self.anim = FuncAnimation(
            self.fig,
            update,
            frames=max_epochs,
            init_func=init,
            blit=blit,
            interval=interval,
        )

        # Save animation if path is provided
        if save_path:
            if save_format == "mp4":
                try:
                    from matplotlib.animation import FFMpegWriter
                except Exception as _e:
                    raise ImportError(
                        "FFmpeg writer not available. Install ffmpeg or use a different writer."
                    ) from None
                writer = FFMpegWriter(
                    fps=fps, metadata={"artist": "TrainingAnimator"}, bitrate=1800
                )
                self.anim.save(save_path, writer=writer, dpi=dpi)
            elif save_format == "gif":
                try:
                    from matplotlib.animation import PillowWriter
                except Exception as _e:
                    raise ImportError(
                        "Pillow writer not available. Install Pillow or use a different writer."
                    ) from None
                writer = PillowWriter(fps=fps)
                self.anim.save(save_path, writer=writer, dpi=dpi)
            else:
                raise ValueError(f"Unsupported save format: {save_format}")
            print(f"Animation saved to {save_path}")

        return self.anim

    def setup_training_video(self, filepath, fps=10, dpi=None):
        """Set up a video writer to capture training progress in real-time.

        Args:
            filepath: (str) - Path to save the video
            fps: (int) - Frames per second
            dpi: (int, optional) - DPI for rendering
        """
        try:
            import os

            from matplotlib.animation import FFMpegWriter

            if self.fig is None:
                raise ValueError("Animation not initialized. Call initialize() first.")

            # Ensure the directory exists
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Try to create the writer with explicit path to ffmpeg if needed
            try:
                # First attempt with default settings
                self.writer = FFMpegWriter(
                    fps=fps,
                    metadata={
                        "title": "Model Training Progress",
                        "artist": "TrainingAnimator",
                    },
                    bitrate=1800,
                )

                # Setup the writer
                self.writer.setup(self.fig, filepath, dpi=dpi or self.dpi)

            except FileNotFoundError:
                # If FFmpeg file not found, use an alternative approach
                print("FFmpeg not found in system PATH. Trying alternative method...")

                # Use PillowWriter as a fallback
                from matplotlib.animation import PillowWriter

                self.writer = PillowWriter(
                    fps=fps,
                    metadata={
                        "title": "Model Training Progress",
                        "artist": "TrainingAnimator",
                    },
                )

                # Change extension to .gif if it was .mp4
                if filepath.lower().endswith(".mp4"):
                    filepath = filepath[:-4] + ".gif"
                    print(f"Changed output format to GIF: {filepath}")

                # Setup the PillowWriter
                self.writer.setup(self.fig, filepath, dpi=dpi or self.dpi)

            self.frame_count = 0

            # Draw the initial empty plot and capture the background for blitting
            self.fig.canvas.draw()
            self.bg_cache = self.fig.canvas.copy_from_bbox(self.fig.bbox)

            print(
                f"Animation writer successfully set up. Output will be saved to: {filepath}"
            )
        except Exception as e:
            self.writer = None
            print(f"Error setting up animation writer: {str(e)}")
            print(
                "Animation capture disabled. Training will continue without animation."
            )
            raise

    def add_training_frame(self):
        """Add a frame to the training video."""
        import matplotlib.pyplot as plt

        if self.writer is None:
            raise ValueError(
                "Video writer not initialized. Call setup_training_video() first."
            )

        # Update line data for each metric
        for metric, line in self.lines.items():
            if len(self.metrics[metric]) > 0:
                x = range(1, len(self.metrics[metric]) + 1)
                y = self.metrics[metric]
                line.set_data(x, y)

        # Update axis limits for all axes
        for ax_row in self.axes:
            for ax in ax_row:
                ax.relim()  # Recalculate data limits based on current line data
                ax.autoscale_view()  # Adjust view limits to fit the data

        # Redraw the entire canvas to reflect changes
        self.fig.canvas.draw()
        plt.pause(0.001)

        # Capture the frame for video
        self.writer.grab_frame()
        self.frame_count += 1

    def finish_training_video(self, print_message=True):
        """Finish and save the training video."""
        if self.writer is None:
            raise ValueError(
                "Video writer not initialized. Call setup_training_video() first."
            )

        self.writer.finish()
        if print_message:
            print(f"Training video saved with {self.frame_count} frames.")
        self.writer = None
        self.frame_count = 0
