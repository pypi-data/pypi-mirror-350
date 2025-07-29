"""
MLFlow - Advanced Machine Learning Library

A high-performance machine learning library featuring:
- Custom neural network implementations
- Advanced ensemble methods
- Automatic hyperparameter optimization
- Model interpretability tools
- Production-ready utilities
"""

__version__ = "1.0.0"
__author__ = "Jatin Hans"

from .models import (
    CustomNeuralNetwork,
    AdaptiveEnsemble,
    GradientBoostingClassifier,
)
from .optimization import BayesianOptimizer, GeneticAlgorithm
from .utils import ModelValidator, DataPreprocessor, PerformanceProfiler
from .interpretability import SHAPExplainer, FeatureImportanceAnalyzer

__all__ = [
    "CustomNeuralNetwork",
    "AdaptiveEnsemble", 
    "GradientBoostingClassifier",
    "BayesianOptimizer",
    "GeneticAlgorithm",
    "ModelValidator",
    "DataPreprocessor",
    "PerformanceProfiler",
    "SHAPExplainer",
    "FeatureImportanceAnalyzer",
]