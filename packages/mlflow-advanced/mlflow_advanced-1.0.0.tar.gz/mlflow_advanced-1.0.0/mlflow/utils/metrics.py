import numpy as np

def calculate_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate classification accuracy.

    Args:
        y_true (np.ndarray): True labels, either as integers (shape: [n_samples]) 
                             or one-hot encoded (shape: [n_samples, n_classes]).
        y_pred (np.ndarray): Predicted labels or probabilities, either as class indices 
                             (shape: [n_samples]) or one-hot/probabilities (shape: [n_samples, n_classes]).

    Returns:
        float: Accuracy score between 0 and 1.
    """
    if y_pred.ndim > 1:
        y_pred = np.argmax(y_pred, axis=1)
    if y_true.ndim > 1:
        y_true = np.argmax(y_true, axis=1)
    
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}")
    
    return np.mean(y_true == y_pred)


def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-15) -> float:
    """
    Calculate binary cross-entropy loss.
    """
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()  # Flatten predictions first

    if y_true.ndim != 1:
        raise ValueError("y_true should be 1D array for binary cross-entropy")
    if y_pred.shape != y_true.shape:
        raise ValueError(f"Shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}")
    if not ((y_true == 0) | (y_true == 1)).all():
        raise ValueError("y_true contains values other than 0 or 1 for binary cross-entropy")
    
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return loss



def categorical_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-15) -> float:
    """
    Calculate categorical cross-entropy loss for one-hot encoded labels.

    Args:
        y_true (np.ndarray): One-hot encoded true labels, shape (n_samples, n_classes).
        y_pred (np.ndarray): Predicted probabilities, shape (n_samples, n_classes).
        epsilon (float): Small value to avoid log(0).

    Returns:
        float: Categorical cross-entropy loss.
    """
    if y_true.ndim != 2:
        raise ValueError("y_true should be 2D array for categorical cross-entropy")
    if y_pred.shape != y_true.shape:
        raise ValueError(f"Shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}")

    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    loss = -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
    return loss

def calculate_loss(y_true: np.ndarray, y_pred: np.ndarray, loss_type='binary') -> float:
    """
    Wrapper to calculate loss based on loss_type.
    
    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted labels/probabilities.
        loss_type (str): 'binary' or 'categorical'.
    
    Returns:
        float: Calculated loss.
    """
    if loss_type == 'binary':
        return binary_cross_entropy(y_true, y_pred)
    elif loss_type == 'categorical':
        return categorical_cross_entropy(y_true, y_pred)
    else:
        raise ValueError(f"Unknown loss_type: {loss_type}")
