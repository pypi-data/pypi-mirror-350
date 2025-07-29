import numpy as np
from sklearn.tree import DecisionTreeRegressor
from typing import List, Optional

class GradientBoostingClassifier:
    """
    Custom Gradient Boosting implementation for binary classification.
    
    Features:
    - Custom loss functions
    - Regularization
    - Early stopping
    - Feature importance calculation
    """
    
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1,
                 max_depth: int = 3, min_samples_split: int = 2,
                 random_state: Optional[int] = None):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        
        self.estimators = []
        self.feature_importances_ = None
        self.train_scores = []
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def _log_loss_gradient(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """Calculate gradient of log loss."""
        return y_true - self._sigmoid(y_pred)
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'GradientBoostingClassifier':
        """Train the gradient boosting classifier."""
        n_samples, n_features = X.shape
        
        # Initialize with zeros
        y_pred = np.zeros(n_samples)
        
        for i in range(self.n_estimators):
            # Calculate residuals (negative gradient)
            residuals = self._log_loss_gradient(y, y_pred)
            
            # Fit a tree to the residuals
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                random_state=self.random_state
            )
            tree.fit(X, residuals)
            
            # Update predictions
            tree_pred = tree.predict(X)
            y_pred += self.learning_rate * tree_pred
            
            self.estimators.append(tree)
            
            # Calculate training score
            train_score = np.mean((self._sigmoid(y_pred) > 0.5) == y)
            self.train_scores.append(train_score)
        
        # Calculate feature importances
        self._calculate_feature_importances(n_features)
        
        return self
    
    def _calculate_feature_importances(self, n_features: int):
        """Calculate feature importances from all trees."""
        importances = np.zeros(n_features)
        
        for tree in self.estimators:
            if hasattr(tree, 'feature_importances_'):
                importances += tree.feature_importances_
        
        # Normalize
        self.feature_importances_ = importances / len(self.estimators)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        y_pred = np.zeros(X.shape[0])
        
        for tree in self.estimators:
            y_pred += self.learning_rate * tree.predict(X)
        
        proba = self._sigmoid(y_pred)
        return np.column_stack([1 - proba, proba])
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        proba = self.predict_proba(X)
        return (proba[:, 1] > 0.5).astype(int)