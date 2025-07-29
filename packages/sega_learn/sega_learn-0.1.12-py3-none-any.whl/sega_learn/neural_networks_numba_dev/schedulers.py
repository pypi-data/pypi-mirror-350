import numpy as np


class lr_scheduler_step:
    """
    Learning rate scheduler class for training neural networks.
    Reduces the learning rate by a factor of lr_decay every lr_decay_epoch epochs.
    Args:
        optimizer (Optimizer): The optimizer to adjust the learning rate for.
        lr_decay (float, optional): The factor to reduce the learning rate by. Defaults to 0.1.
        lr_decay_epoch (int, optional): The number of epochs to wait before decaying the learning rate. Defaults to 10
    """

    def __init__(self, optimizer, lr_decay=0.1, lr_decay_epoch=10):
        self.optimizer = optimizer
        self.lr_decay = lr_decay
        self.lr_decay_epoch = lr_decay_epoch

    def __repr__(self):
        return f"StepLR({self.optimizer}, lr_decay={self.lr_decay}, lr_decay_epoch={self.lr_decay_epoch})"

    def step(self, epoch):
        """
        Adjusts the learning rate based on the current epoch. Decays the learning rate by lr_decay every lr_decay_epoch epochs.
        Args:
            epoch (int): The current epoch number.
        Returns: None
        """
        if epoch % self.lr_decay_epoch == 0 and epoch > 0:
            self.optimizer.learning_rate *= self.lr_decay
            return f"  --Decaying learning rate stepped at epoch {epoch} from {self.optimizer.learning_rate} to {self.optimizer.learning_rate * self.lr_decay}"

    def reduce(self):
        self.optimizer.learning_rate *= self.lr_decay
        return f"  --Decaying learning rate from {self.optimizer.learning_rate} to {self.optimizer.learning_rate * self.lr_decay}"


class lr_scheduler_exp:
    """
    Learning rate scheduler class for training neural networks.
    Reduces the learning rate exponentially by lr_decay every lr_decay_epoch epochs.
    """

    def __init__(self, optimizer, lr_decay=0.1, lr_decay_epoch=10):
        self.optimizer = optimizer
        self.lr_decay = lr_decay
        self.lr_decay_epoch = lr_decay_epoch

    def __repr__(self):
        return f"ExponentialLR({self.optimizer}, lr_decay={self.lr_decay}, lr_decay_epoch={self.lr_decay_epoch})"

    def step(self, epoch):
        """
        Adjusts the learning rate based on the current epoch. Decays the learning rate by lr_decay every lr_decay_epoch epochs.
        Args:
            epoch (int): The current epoch number.
        Returns: None
        """
        if epoch % self.lr_decay_epoch == 0 and epoch > 0:
            self.optimizer.learning_rate *= np.exp(-self.lr_decay * epoch)
            return f"  --Decaying learning rate exponentially at epoch {epoch} from {self.optimizer.learning_rate} to {self.optimizer.learning_rate * np.exp(-self.lr_decay * epoch)}"

    def reduce(self):
        self.optimizer.learning_rate *= np.exp(-self.lr_decay)
        return f"  --Decaying learning rate exponentially from {self.optimizer.learning_rate} to {self.optimizer.learning_rate * np.exp(-self.lr_decay)}"


class lr_scheduler_plateau:
    """
    A custom learning rate scheduler that adjusts the learning rate based on the plateau of the loss function.
    Args:
        lr_scheduler (object): The learning rate scheduler object.
        patience (int): The number of epochs to wait for improvement before reducing the learning rate. Default is 5.
        threshold (float): The minimum improvement threshold required to update the best loss. Default is 0.01.
    Methods:
        step(loss): Updates the learning rate based on the loss value.
    """

    def __init__(self, lr_scheduler, patience=5, threshold=0.01):
        self.lr_scheduler = lr_scheduler
        self.patience = patience
        self.threshold = threshold
        self.best_loss = float("inf")
        self.wait = 0

    def __repr__(self):
        return f"PlateauLR({self.lr_scheduler}, patience={self.patience}, threshold={self.threshold})"

    def step(self, epoch, loss):
        """
        Updates the learning rate based on the loss value.
        Args:
            loss (float): The current loss value.
        """
        if loss < self.best_loss - self.threshold:
            self.best_loss = loss
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.lr_scheduler.reduce()
                self.wait = 0
                return "  --Plateau learning rate scheduler triggered, reducing learning rate"
