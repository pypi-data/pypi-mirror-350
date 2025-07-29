import numpy as np
from typing import List, Any, Optional
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from concurrent.futures import ThreadPoolExecutor
import threading

class AdaptiveEnsemble(BaseEstimator, ClassifierMixin):
    """
    Advanced ensemble method that dynamically weighs models based on performance.
    
    Features:
    - Dynamic model weighting
    - Parallel training
    - Adaptive learning
    - Performance monitoring
    """
    
    def __init__(self, base_models: Optional[List] = None, n_models: int = 5, 
                 adaptation_rate: float = 0.1):
        self.base_models = base_models or [
            DecisionTreeClassifier(random_state=i) for i in range(n_models)
        ]
        self.n_models = len(self.base_models)
        self.adaptation_rate = adaptation_rate
        self.model_weights = np.ones(self.n_models) / self.n_models
        self.model_performance = np.zeros(self.n_models)
        self.lock = threading.Lock()
    
    def _train_single_model(self, args):
        """Train a single model (for parallel processing)."""
        model, X, y, model_idx = args
        try:
            model.fit(X, y)
            # Calculate performance score
            train_score = model.score(X, y)
            return model_idx, model, train_score
        except Exception as e:
            print(f"Error training model {model_idx}: {e}")
            return model_idx, model, 0.0
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train ensemble with parallel processing."""
        # Prepare arguments for parallel training
        train_args = [(self.base_models[i], X, y, i) for i in range(self.n_models)]
        
        # Train models in parallel
        with ThreadPoolExecutor(max_workers=min(4, self.n_models)) as executor:
            results = list(executor.map(self._train_single_model, train_args))
        
        # Update models and performance scores
        for model_idx, trained_model, score in results:
            self.base_models[model_idx] = trained_model
            self.model_performance[model_idx] = score
        
        # Update weights based on performance
        self._update_weights()
        return self
    
    def _update_weights(self):
        """Dynamically update model weights based on performance."""
        # Softmax weighting based on performance
        exp_performance = np.exp(self.model_performance / self.adaptation_rate)
        self.model_weights = exp_performance / np.sum(exp_performance)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities using weighted ensemble."""
        predictions = []
        
        for i, model in enumerate(self.base_models):
            try:
                if hasattr(model, 'predict_proba'):
                    pred = model.predict_proba(X)
                else:
                    # For models without predict_proba, use decision function or predict
                    pred = model.predict(X).reshape(-1, 1)
                    pred = np.column_stack([1-pred, pred])  # Binary classification assumption
                predictions.append(pred * self.model_weights[i])
            except Exception:
                # Skip problematic models
                continue
        
        if not predictions:
            raise ValueError("No valid predictions from ensemble models")
            
        return np.sum(predictions, axis=0)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the ensemble."""
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)
    
    def get_model_weights(self) -> np.ndarray:
        """Get current model weights."""
        return self.model_weights.copy()