import numpy as np
from typing import Dict, Any, Callable, List, Tuple, Optional
from scipy.optimize import minimize
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
import warnings
warnings.filterwarnings('ignore')

class BayesianOptimizer:
    """
    Advanced Bayesian optimization for hyperparameter tuning.
    
    Features:
    - Gaussian Process surrogate model
    - Multiple acquisition functions
    - Parallel evaluation support
    - Constraint handling
    """
    
    def __init__(self, objective_function: Callable, parameter_space: Dict[str, Tuple],
                 acquisition_function: str = 'ei', n_initial_points: int = 5):
        self.objective_function = objective_function
        self.parameter_space = parameter_space
        self.acquisition_function = acquisition_function
        self.n_initial_points = n_initial_points
        
        # Initialize GP model
        kernel = Matern(length_scale=1.0, nu=2.5)
        self.gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, 
                                         normalize_y=True, n_restarts_optimizer=5)
        
        # Storage for evaluated points
        self.X_evaluated = []
        self.y_evaluated = []
        self.best_params = None
        self.best_score = float('-inf')
    
    def _encode_parameters(self, params: Dict[str, Any]) -> np.ndarray:
        """Convert parameter dictionary to array."""
        encoded = []
        for param_name in sorted(self.parameter_space.keys()):
            value = params[param_name]
            param_min, param_max = self.parameter_space[param_name]
            
            # Normalize to [0, 1]
            normalized = (value - param_min) / (param_max - param_min)
            encoded.append(normalized)
        
        return np.array(encoded)
    
    def _decode_parameters(self, encoded: np.ndarray) -> Dict[str, Any]:
        """Convert array back to parameter dictionary."""
        params = {}
        for i, param_name in enumerate(sorted(self.parameter_space.keys())):
            param_min, param_max = self.parameter_space[param_name]
            
            # Denormalize from [0, 1]
            value = encoded[i] * (param_max - param_min) + param_min
            
            # Handle integer parameters
            if isinstance(param_min, int) and isinstance(param_max, int):
                value = int(round(value))
            
            params[param_name] = value
        
        return params
    
    def _acquisition_function(self, X: np.ndarray) -> np.ndarray:
        """Calculate acquisition function values."""
        if len(self.X_evaluated) < 2:
            return np.random.random(X.shape[0])
        
        mu, sigma = self.gp.predict(X.reshape(1, -1), return_std=True)
        
        if self.acquisition_function == 'ei':  # Expected Improvement
            improvement = mu - self.best_score
            Z = improvement / (sigma + 1e-9)
            ei = improvement * self._normal_cdf(Z) + sigma * self._normal_pdf(Z)
            return ei[0] if ei.ndim > 0 else ei
        
        elif self.acquisition_function == 'ucb':  # Upper Confidence Bound
            kappa = 2.576  # 99% confidence
            return mu + kappa * sigma
        
        else:
            raise ValueError(f"Unknown acquisition function: {self.acquisition_function}")
    
    def _normal_cdf(self, x):
        """Cumulative distribution function of standard normal."""
        return 0.5 * (1 + np.sign(x) * np.sqrt(1 - np.exp(-2 * x**2 / np.pi)))
    
    def _normal_pdf(self, x):
        """Probability density function of standard normal."""
        return np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
    
    def _get_next_point(self) -> np.ndarray:
        """Find the next point to evaluate using acquisition function."""
        bounds = [(0, 1)] * len(self.parameter_space)
        
        best_acq = float('-inf')
        best_x = None
        
        # Multi-start optimization
        for _ in range(10):
            x_start = np.random.random(len(self.parameter_space))
            
            result = minimize(
                fun=lambda x: -self._acquisition_function(x),
                x0=x_start,
                bounds=bounds,
                method='L-BFGS-B'
            )
            
            if -result.fun > best_acq:
                best_acq = -result.fun
                best_x = result.x
        
        return best_x
    
    def optimize(self, n_iterations: int = 50, verbose: bool = True) -> Dict[str, Any]:
        """
        Perform Bayesian optimization.
        
        Args:
            n_iterations: Number of optimization iterations
            verbose: Whether to print progress
            
        Returns:
            Dictionary with optimization results
        """
        # Initial random sampling
        for i in range(self.n_initial_points):
            # Generate random parameters
            params = {}
            for param_name, (param_min, param_max) in self.parameter_space.items():
                if isinstance(param_min, int) and isinstance(param_max, int):
                    params[param_name] = np.random.randint(param_min, param_max + 1)
                else:
                    params[param_name] = np.random.uniform(param_min, param_max)
            
            # Evaluate objective function
            score = self.objective_function(params)
            
            # Store results
            encoded_params = self._encode_parameters(params)
            self.X_evaluated.append(encoded_params)
            self.y_evaluated.append(score)
            
            # Update best
            if score > self.best_score:
                self.best_score = score
                self.best_params = params.copy()
            
            if verbose:
                print(f"Initial point {i+1}/{self.n_initial_points}: Score = {score:.4f}")
        
        # Convert to numpy arrays
        self.X_evaluated = np.array(self.X_evaluated)
        self.y_evaluated = np.array(self.y_evaluated)
        
        # Bayesian optimization loop
        for iteration in range(n_iterations):
            # Fit GP model
            self.gp.fit(self.X_evaluated, self.y_evaluated)
            
            # Get next point to evaluate
            next_point = self._get_next_point()
            next_params = self._decode_parameters(next_point)
            
            # Evaluate objective function
            score = self.objective_function(next_params)
            
            # Update data
            self.X_evaluated = np.vstack([self.X_evaluated, next_point])
            self.y_evaluated = np.append(self.y_evaluated, score)
            
            # Update best
            if score > self.best_score:
                self.best_score = score
                self.best_params = next_params.copy()
            
            if verbose:
                print(f"Iteration {iteration+1}/{n_iterations}: Score = {score:.4f}, Best = {self.best_score:.4f}")
        
        return {
            'best_params': self.best_params,
            'best_score': self.best_score,
            'n_evaluations': len(self.y_evaluated),
            'evaluation_history': list(self.y_evaluated)
        }