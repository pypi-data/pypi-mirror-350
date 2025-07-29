import numpy as np


class Metrics:
    """Implements various regression and classification metrics."""

    @classmethod
    def mean_squared_error(cls, y_true, y_pred):
        """Calculates the mean squared error between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            mse: (float) - The mean squared error.
        """
        return np.mean((y_true - y_pred) ** 2)

    @classmethod
    def r_squared(cls, y_true, y_pred):
        """Calculates the R-squared score between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            r_squared: (float) - The R-squared score.
        """
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot)

    @classmethod
    def mean_absolute_error(cls, y_true, y_pred):
        """Calculates the mean absolute error between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            mae: (float) - The mean absolute error.
        """
        return np.mean(np.abs(y_true - y_pred))

    @classmethod
    def root_mean_squared_error(cls, y_true, y_pred):
        """Calculates the root mean squared error between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            rmse: (float) - The root mean squared error.
        """
        return np.sqrt(np.mean((y_true - y_pred) ** 2))

    @classmethod
    def mean_absolute_percentage_error(cls, y_true, y_pred):
        """Calculates the mean absolute percentage error between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            mape: (float) - The mean absolute percentage error as a decimal. Returns np.nan if y_true is all zeros.
        """
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        non_zero_indices = y_true != 0
        if not np.any(non_zero_indices):
            return np.nan
        return np.mean(
            np.abs(
                (y_true[non_zero_indices] - y_pred[non_zero_indices])
                / y_true[non_zero_indices]
            )
        )

    @classmethod
    def mean_percentage_error(cls, y_true, y_pred):
        """Calculates the mean percentage error between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            mpe: (float) - The mean percentage error.
        """
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        non_zero_indices = y_true != 0
        if not np.any(non_zero_indices):
            return np.nan
        return np.mean(
            (y_true[non_zero_indices] - y_pred[non_zero_indices])
            / y_true[non_zero_indices]
        )

    # Classification Metrics
    @classmethod
    def accuracy(cls, y_true, y_pred):
        """Calculates the accuracy score between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            accuracy: (float) - The accuracy score.
        """
        return np.mean(y_true == y_pred)

    @classmethod
    def precision(cls, y_true, y_pred):
        """Calculates the precision score between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            precision: (float) - The precision score.
        """
        # Ensure the arrays are numpy arrays for element-wise operations
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        if tp + fp == 0:
            return 0.0
        return tp / (tp + fp)

    @classmethod
    def recall(cls, y_true, y_pred):
        """Calculates the recall score between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            recall: (float) - The recall score.
        """
        # Ensure the arrays are numpy arrays for element-wise operations
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        tp = np.sum((y_true == 1) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        if tp + fn == 0:
            return 0.0
        return tp / (tp + fn)

    @classmethod
    def f1_score(cls, y_true, y_pred):
        """Calculates the F1 score between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            f1_score: (float) - The F1 score.
        """
        precision = cls.precision(y_true, y_pred)
        recall = cls.recall(y_true, y_pred)
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

    @classmethod
    def log_loss(cls, y_true, y_pred):
        """Calculates the log loss between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted probabilities.

        Returns:
            log_loss: (float) - The log loss.
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        # Clip y_pred to avoid log(0) and log(1)
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)

        if y_pred.ndim == 1:
            y_pred = np.vstack([1 - y_pred, y_pred]).T

        y_true_one_hot = np.eye(y_pred.shape[1])[y_true]
        return -np.mean(np.sum(y_true_one_hot * np.log(y_pred), axis=1))

    # Additional Metrics
    @classmethod
    def confusion_matrix(cls, y_true, y_pred):
        """Calculates the confusion matrix between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            cm: (np.ndarray) - The confusion matrix.
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        unique_labels = np.unique(np.concatenate((y_true, y_pred)))
        cm = np.zeros((len(unique_labels), len(unique_labels)), dtype=int)
        for i, label in enumerate(unique_labels):
            for j, pred_label in enumerate(unique_labels):
                cm[i, j] = np.sum((y_true == label) & (y_pred == pred_label))
        return cm

    @classmethod
    def show_confusion_matrix(cls, y_true, y_pred):
        """Calculates and displays the confusion matrix between the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            cm: (np.ndarray) - The confusion matrix.
        """
        cm = cls.confusion_matrix(y_true, y_pred)
        unique_labels = np.unique(np.concatenate((y_true, y_pred)))
        cm_dict = {}
        for i, label in enumerate(unique_labels):
            cm_dict[label] = {}
            for j, pred_label in enumerate(unique_labels):
                cm_dict[label][pred_label] = cm[i, j]

        for label in unique_labels:
            print(f"True Label {label} : {cm_dict[label]}")

        return cm

    @classmethod
    def classification_report(cls, y_true, y_pred):
        """Generates a classification report for the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            report: (dict) - The classification report.
        """
        unique_labels = np.unique(np.concatenate((y_true, y_pred)))
        report = {}
        for label in unique_labels:
            precision = cls.precision(y_true == label, y_pred == label)
            recall = cls.recall(y_true == label, y_pred == label)
            f1 = cls.f1_score(y_true == label, y_pred == label)
            support = np.sum(y_true == label)
            report[label] = {
                "precision": precision,
                "recall": recall,
                "f1-score": f1,
                "support": support,
            }
        return report

    @classmethod
    def show_classification_report(cls, y_true, y_pred):
        """Generates and displays a classification report for the true and predicted values.

        Args:
            y_true: (np.ndarray) - The true values.
            y_pred: (np.ndarray) - The predicted values.

        Returns:
            report: (dict) - The classification report.
        """
        report = cls.classification_report(y_true, y_pred)
        print(
            f"{'Label':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support':<10}"
        )
        for label, metrics in report.items():
            print(
                f"{label:<10} {metrics['precision']:<10.4f} {metrics['recall']:<10.4f} {metrics['f1-score']:<10.4f} {metrics['support']:<10}"
            )
        print("-" * 50)
        print(f"{'Accuracy':<32} {cls.accuracy(y_true, y_pred):<10.4f} {len(y_true)}")
