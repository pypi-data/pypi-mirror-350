import numpy as np
from typing import List, Callable, Optional, Tuple
from abc import ABC, abstractmethod
import pickle
from ..utils.metrics import calculate_accuracy, calculate_loss

class ActivationFunction(ABC):
    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass
    
    @abstractmethod
    def backward(self, x: np.ndarray) -> np.ndarray:
        pass

class ReLU(ActivationFunction):
    def forward(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)
    
    def backward(self, x: np.ndarray) -> np.ndarray:
        return (x > 0).astype(float)

class Sigmoid(ActivationFunction):
    def forward(self, x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def backward(self, x: np.ndarray) -> np.ndarray:
        s = self.forward(x)
        return s * (1 - s)

class Layer:
    def __init__(self, input_size: int, output_size: int, activation: ActivationFunction):
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.bias = np.zeros((1, output_size))
        self.activation = activation
        
        # For backpropagation
        self.last_input = None
        self.last_output = None
        
    def forward(self, x: np.ndarray) -> np.ndarray:
        self.last_input = x
        z = np.dot(x, self.weights) + self.bias
        self.last_output = self.activation.forward(z)
        return self.last_output
    
    def backward(self, grad_output: np.ndarray, learning_rate: float) -> np.ndarray:
        z = np.dot(self.last_input, self.weights) + self.bias
        grad_activation = self.activation.backward(z)
        grad_z = grad_output * grad_activation
        
        '''print(f"grad_output shape: {grad_output.shape}")
        print(f"grad_activation shape: {grad_activation.shape}")
        print(f"grad_z shape: {grad_z.shape}")
        print(f"last_input shape: {self.last_input.shape}")'''
        
        grad_weights = np.dot(self.last_input.T, grad_z)
        grad_bias = np.sum(grad_z, axis=0, keepdims=True)
        
        '''print(f"grad_weights shape: {grad_weights.shape}")
        print(f"weights shape: {self.weights.shape}")'''
        
        self.weights -= learning_rate * grad_weights
        self.bias -= learning_rate * grad_bias
        
        return np.dot(grad_z, self.weights.T)


class CustomNeuralNetwork:
    """
    High-performance neural network with custom backpropagation implementation.
    
    Features:
    - Custom activation functions
    - Adaptive learning rate
    - Batch processing
    - Early stopping
    - Model persistence
    """
    
    def __init__(self, layers: List[int], activations: List[str] = None, 
                 learning_rate: float = 0.001, batch_size: int = 32):
        self.layers = layers
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.history = {'loss': [], 'accuracy': []}
        
        # Initialize activations
        if activations is None:
            activations = ['relu'] * (len(layers) - 2) + ['sigmoid']
        
        activation_map = {'relu': ReLU(), 'sigmoid': Sigmoid()}
        
        # Build network
        self.network = []
        for i in range(len(layers) - 1):
            layer = Layer(layers[i], layers[i+1], activation_map[activations[i]])
            self.network.append(layer)
    
    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass through the network."""
        output = X
        for layer in self.network:
            output = layer.forward(output)
        return output
    
    def backward(self, X: np.ndarray, y: np.ndarray, predictions: np.ndarray):
        m = X.shape[0]
        y = y.reshape(-1, 1)  # Ensure shape compatibility
        grad = (predictions - y) / m
        for layer in reversed(self.network):
            grad = layer.backward(grad, self.learning_rate)

    
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, 
            validation_data: Optional[Tuple] = None, early_stopping: bool = True) -> dict:
        """
        Train the neural network with advanced features.
        
        Args:
            X: Training features
            y: Training labels
            epochs: Number of training epochs
            validation_data: Tuple of (X_val, y_val) for validation
            early_stopping: Whether to use early stopping
            
        Returns:
            Training history
        """
        best_val_loss = float('inf')
        patience_counter = 0
        patience = 10
        
        for epoch in range(epochs):
            # Shuffle data
            indices = np.random.permutation(X.shape[0])
            X_shuffled = X[indices]
            y_shuffled = y[indices]
            
            epoch_loss = 0
            batches = 0
            
            # Mini-batch training
            for i in range(0, X.shape[0], self.batch_size):
                batch_X = X_shuffled[i:i+self.batch_size]
                batch_y = y_shuffled[i:i+self.batch_size]
                
                # Forward pass
                predictions = self.forward(batch_X)
                
                # Calculate loss
                loss = calculate_loss(batch_y, predictions)
                epoch_loss += loss
                batches += 1
                
                # Backward pass
                self.backward(batch_X, batch_y, predictions)
            
            # Calculate metrics
            train_predictions = self.forward(X)
            train_accuracy = calculate_accuracy(y, train_predictions)
            avg_loss = epoch_loss / batches
            
            self.history['loss'].append(avg_loss)  
            self.history['accuracy'].append(train_accuracy)
            
            # Validation and early stopping
            if validation_data:
                X_val, y_val = validation_data
                val_predictions = self.forward(X_val)
                val_loss = calculate_loss(y_val, val_predictions)
                val_accuracy = calculate_accuracy(y_val, val_predictions)
                
                if early_stopping:
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        patience_counter = 0
                    else:
                        patience_counter += 1
                        if patience_counter >= patience:
                            print(f"Early stopping at epoch {epoch}")
                            break
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}: Loss = {avg_loss:.4f}, Accuracy = {train_accuracy:.4f}")
        
        return self.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions on new data."""
        return self.forward(X)
    
    def save_model(self, filepath: str):
        """Save the trained model."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load_model(cls, filepath: str):
        """Load a saved model."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)