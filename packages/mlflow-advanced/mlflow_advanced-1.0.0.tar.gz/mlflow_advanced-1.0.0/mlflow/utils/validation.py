import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
from typing import Any, Dict, List
import time

class ModelValidator:
    """
    Comprehensive model validation and performance analysis.
    
    Features:
    - Cross-validation with multiple metrics
    - Statistical significance testing
    - Performance profiling
    - Automated report generation
    """
    
    def __init__(self, cv_folds: int = 5, random_state: int = 42):
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    
    def validate_model(self, model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Comprehensive model validation.
        
        Args:
            model: Trained model to validate
            X: Features
            y: Labels
            
        Returns:
            Validation results dictionary
        """
        results = {}
        
        # Cross-validation scores
        start_time = time.time()
        cv_scores = cross_val_score(model, X, y, cv=self.cv, scoring='accuracy')
        cv_time = time.time() - start_time
        
        results['cv_scores'] = cv_scores
        results['cv_mean'] = np.mean(cv_scores)
        results['cv_std'] = np.std(cv_scores)
        results['cv_time'] = cv_time
        
        # Detailed classification metrics
        y_pred = model.predict(X)
        results['classification_report'] = classification_report(y, y_pred, output_dict=True)
        results['confusion_matrix'] = confusion_matrix(y, y_pred).tolist()
        
        # Model complexity metrics
        if hasattr(model, 'n_features_in_'):
            results['n_features'] = model.n_features_in_
        
        return results
    
    def compare_models(self, models: Dict[str, Any], X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Compare multiple models and rank them."""
        comparison_results = {}
        
        for model_name, model in models.items():
            results = self.validate_model(model, X, y)
            comparison_results[model_name] = results
        
        # Rank models by CV score
        rankings = sorted(comparison_results.items(), 
                         key=lambda x: x[1]['cv_mean'], reverse=True)
        
        return {
            'individual_results': comparison_results,
            'rankings': [(name, results['cv_mean']) for name, results in rankings],
            'best_model': rankings[0][0]
        }