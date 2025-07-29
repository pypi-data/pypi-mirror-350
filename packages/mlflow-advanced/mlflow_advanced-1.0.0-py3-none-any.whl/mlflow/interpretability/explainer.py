import numpy as np
from typing import Any, Dict, List, Optional, Union
import matplotlib.pyplot as plt

class SHAPExplainer:
    """
    SHAP-like explainer for model interpretability.
    
    Features:
    - Feature importance calculation
    - Local explanations
    - Visualization tools
    - Multiple explanation methods
    """
    
    def __init__(self, model: Any, X_background: np.ndarray):
        self.model = model
        self.X_background = X_background
        self.baseline = self._calculate_baseline()
    
    def _calculate_baseline(self) -> float:
        """Calculate baseline prediction (average of background)."""
        if hasattr(self.model, 'predict_proba'):
            baseline_pred = self.model.predict_proba(self.X_background)
            return np.mean(baseline_pred[:, 1])  # Assuming binary classification
        else:
            baseline_pred = self.model.predict(self.X_background)
            return np.mean(baseline_pred)
    
    def explain_instance(self, instance: np.ndarray, n_samples: int = 1000) -> Dict[str, Any]:
        """
        Explain a single prediction using sampling-based approach.
        
        Args:
            instance: Single instance to explain
            n_samples: Number of samples for approximation
            
        Returns:
            Explanation dictionary
        """
        if instance.ndim == 1:
            instance = instance.reshape(1, -1)
        
        n_features = instance.shape[1]
        feature_contributions = np.zeros(n_features)
        
        # Get prediction for the instance
        if hasattr(self.model, 'predict_proba'):
            instance_pred = self.model.predict_proba(instance)[0, 1]
        else:
            instance_pred = self.model.predict(instance)[0]
        
        # Calculate feature contributions using marginal contributions
        for i in range(n_features):
            marginal_contributions = []
            
            for _ in range(n_samples // n_features):
                # Create coalition with and without feature i
                coalition_with = np.random.choice([0, 1], size=n_features)
                coalition_without = coalition_with.copy()
                coalition_without[i] = 0
                coalition_with[i] = 1
                
                # Create samples based on coalitions
                sample_with = np.where(coalition_with, instance[0], 
                                     self.X_background[np.random.randint(len(self.X_background))])
                sample_without = np.where(coalition_without, instance[0],
                                        self.X_background[np.random.randint(len(self.X_background))])
                
                # Calculate predictions
                if hasattr(self.model, 'predict_proba'):
                    pred_with = self.model.predict_proba(sample_with.reshape(1, -1))[0, 1]
                    pred_without = self.model.predict_proba(sample_without.reshape(1, -1))[0, 1]
                else:
                    pred_with = self.model.predict(sample_with.reshape(1, -1))[0]
                    pred_without = self.model.predict(sample_without.reshape(1, -1))[0]
                
                marginal_contributions.append(pred_with - pred_without)
            
            feature_contributions[i] = np.mean(marginal_contributions)
        
        return {
            'instance_prediction': instance_pred,
            'baseline_prediction': self.baseline,
            'feature_contributions': feature_contributions,
            'feature_values': instance[0],
            'sum_contributions': np.sum(feature_contributions) + self.baseline
        }
class FeatureImportanceAnalyzer:
    """
    Advanced feature importance analysis.
    
    Features:
    - Multiple importance calculation methods
    - Statistical significance testing
    - Visualization tools
    - Feature interaction detection (future scope)
    """
    
    def __init__(self, model: Any):
        self.model = model
        self.importance_cache = {}
    
    def calculate_permutation_importance(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: Optional[List[str]] = None,
        n_repeats: int = 10,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """
        Calculate permutation feature importance.
        
        Args:
            X: Feature matrix
            y: Target labels
            feature_names: Optional list of feature names
            n_repeats: Number of repeats per feature
            random_state: Random seed
        
        Returns:
            Dictionary with importance scores and statistics
        """
        np.random.seed(random_state)
        
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(X.shape[1])]
        
        # Baseline score
        if hasattr(self.model, 'score'):
            baseline_score = self.model.score(X, y)
        else:
            baseline_pred = self.model.predict(X)
            baseline_score = np.mean(baseline_pred == y)
        
        n_features = X.shape[1]
        importance_scores = np.zeros((n_features, n_repeats))
        
        for i in range(n_features):
            for repeat in range(n_repeats):
                X_permuted = X.copy()
                permutation_idx = np.random.permutation(X.shape[0])
                X_permuted[:, i] = X[permutation_idx, i]
                
                if hasattr(self.model, 'score'):
                    permuted_score = self.model.score(X_permuted, y)
                else:
                    permuted_pred = self.model.predict(X_permuted)
                    permuted_score = np.mean(permuted_pred == y)
                
                importance_scores[i, repeat] = baseline_score - permuted_score
        
        mean_importance = np.mean(importance_scores, axis=1)
        std_importance = np.std(importance_scores, axis=1)
        
        result = {
            "feature_names": feature_names,
            "mean_importance": mean_importance,
            "std_importance": std_importance,
            "raw_scores": importance_scores
        }
        
        self.importance_cache = result
        return result

    def plot_importance(self, top_n: Optional[int] = None, figsize: tuple = (10, 6)) -> None:
        """
        Plot permutation importance using a bar chart.
        
        Args:
            top_n: Number of top features to plot (all if None)
            figsize: Size of the figure
        """
        if not self.importance_cache:
            raise ValueError("Importance not calculated. Run calculate_permutation_importance() first.")
        
        feature_names = np.array(self.importance_cache["feature_names"])
        mean_importance = self.importance_cache["mean_importance"]
        std_importance = self.importance_cache["std_importance"]
        
        # Sort by importance
        sorted_idx = np.argsort(mean_importance)[::-1]
        if top_n:
            sorted_idx = sorted_idx[:top_n]
        
        plt.figure(figsize=figsize)
        plt.barh(range(len(sorted_idx)), mean_importance[sorted_idx],
                 xerr=std_importance[sorted_idx], align='center', color='skyblue')
        plt.yticks(range(len(sorted_idx)), feature_names[sorted_idx])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance (decrease in score)")
        plt.title("Permutation Feature Importance")
        plt.tight_layout()
        plt.show()
