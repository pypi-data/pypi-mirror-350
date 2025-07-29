import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Union, Optional, Tuple, List

class DataPreprocessor:
    """
    Advanced data preprocessing with automatic feature detection and handling.
    
    Features:
    - Automatic data type detection
    - Missing value imputation strategies
    - Feature scaling and normalization
    - Categorical encoding
    - Outlier detection and handling
    """
    
    def __init__(self, handle_missing: str = 'mean', handle_outliers: bool = True,
                 outlier_method: str = 'iqr', scaling_method: str = 'standard'):
        self.handle_missing = handle_missing
        self.handle_outliers = handle_outliers
        self.outlier_method = outlier_method
        self.scaling_method = scaling_method
        
        # Fitted transformers
        self.scalers = {}
        self.label_encoders = {}
        self.fitted = False
    
    def _detect_outliers_iqr(self, data: np.ndarray, multiplier: float = 1.5) -> np.ndarray:
        """Detect outliers using IQR method."""
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        return (data < lower_bound) | (data > upper_bound)
    
    def _handle_missing_values(self, data: Union[pd.DataFrame, np.ndarray]) -> Union[pd.DataFrame, np.ndarray]:
        """Handle missing values based on strategy."""
        if isinstance(data, pd.DataFrame):
            if self.handle_missing == 'mean':
                return data.fillna(data.mean())
            elif self.handle_missing == 'median':
                return data.fillna(data.median())
            elif self.handle_missing == 'mode':
                return data.fillna(data.mode().iloc[0])
            elif self.handle_missing == 'drop':
                return data.dropna()
        else:
            # Handle numpy arrays
            data = data.copy()
            if self.handle_missing == 'mean':
                col_means = np.nanmean(data, axis=0)
                inds = np.where(np.isnan(data))
                data[inds] = np.take(col_means, inds[1])
            elif self.handle_missing == 'median':
                col_medians = np.nanmedian(data, axis=0)
                inds = np.where(np.isnan(data))
                data[inds] = np.take(col_medians, inds[1])
        
        return data
    
    def fit_transform(self, X: Union[pd.DataFrame, np.ndarray], 
                     y: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Fit preprocessor and transform data.
        
        Args:
            X: Features
            y: Labels (optional)
            
        Returns:
            Transformed features and labels
        """
        # Handle missing values
        X_processed = self._handle_missing_values(X.copy() if isinstance(X, pd.DataFrame) else X.copy())
        
        if isinstance(X_processed, pd.DataFrame):
            # Separate numerical and categorical columns
            numerical_cols = X_processed.select_dtypes(include=[np.number]).columns
            categorical_cols = X_processed.select_dtypes(exclude=[np.number]).columns
            
            # Process numerical columns
            if len(numerical_cols) > 0:
                numerical_data = X_processed[numerical_cols].values
                
                # Handle outliers
                if self.handle_outliers:
                    for i in range(numerical_data.shape[1]):
                        if self.outlier_method == 'iqr':
                            outliers = self._detect_outliers_iqr(numerical_data[:, i])
                            # Cap outliers at 5th and 95th percentiles
                            p5, p95 = np.percentile(numerical_data[:, i], [5, 95])
                            numerical_data[outliers, i] = np.clip(numerical_data[outliers, i], p5, p95)
                
                # Scale numerical features
                if self.scaling_method == 'standard':
                    scaler = StandardScaler()
                    numerical_data = scaler.fit_transform(numerical_data)
                    self.scalers['numerical'] = scaler
                
                X_processed[numerical_cols] = numerical_data
            
            # Process categorical columns
            if len(categorical_cols) > 0:
                for col in categorical_cols:
                    le = LabelEncoder()
                    X_processed[col] = le.fit_transform(X_processed[col].astype(str))
                    self.label_encoders[col] = le
            
            X_final = X_processed.values
        else:
            # Handle numpy array
            if self.handle_outliers:
                for i in range(X_processed.shape[1]):
                    if self.outlier_method == 'iqr':
                        outliers = self._detect_outliers_iqr(X_processed[:, i])
                        p5, p95 = np.percentile(X_processed[:, i], [5, 95])
                        X_processed[outliers, i] = np.clip(X_processed[outliers, i], p5, p95)
            
            if self.scaling_method == 'standard':
                scaler = StandardScaler()
                X_final = scaler.fit_transform(X_processed)
                self.scalers['numerical'] = scaler
            else:
                X_final = X_processed
        
        # Process labels if provided
        y_final = None
        if y is not None:
            if y.dtype == 'object' or y.dtype.kind in 'SU':  # String data
                le = LabelEncoder()
                y_final = le.fit_transform(y)
                self.label_encoders['target'] = le
            else:
                y_final = y
        
        self.fitted = True
        return X_final, y_final
    
    def transform(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Transform new data using fitted preprocessor."""
        if not self.fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Handle missing values
        X_processed = self._handle_missing_values(X.copy() if isinstance(X, pd.DataFrame) else X.copy())
        
        if isinstance(X_processed, pd.DataFrame):
            # Apply same transformations as in fit
            numerical_cols = X_processed.select_dtypes(include=[np.number]).columns
            categorical_cols = X_processed.select_dtypes(exclude=[np.number]).columns
            
            if len(numerical_cols) > 0 and 'numerical' in self.scalers:
                X_processed[numerical_cols] = self.scalers['numerical'].transform(
                    X_processed[numerical_cols].values
                )
            
            for col in categorical_cols:
                if col in self.label_encoders:
                    # Handle unseen categories
                    le = self.label_encoders[col]
                    col_data = X_processed[col].astype(str)
                    
                    # Map unseen categories to a default value
                    mask = col_data.isin(le.classes_)
                    X_processed.loc[mask, col] = le.transform(col_data[mask])
                    X_processed.loc[~mask, col] = 0  # Default for unseen categories
            
            return X_processed.values
        else:
            if 'numerical' in self.scalers:
                return self.scalers['numerical'].transform(X_processed)
            return X_processed
