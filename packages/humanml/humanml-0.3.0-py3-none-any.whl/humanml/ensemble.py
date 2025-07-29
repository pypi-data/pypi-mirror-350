#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ensemble Module for HumanML.

Provides ensemble learning capabilities for combining multiple models
to improve prediction performance.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.base import BaseEstimator


class WeightedEnsemble(BaseEstimator):
    """
    Weighted ensemble of models for improved prediction performance.
    """
    
    def __init__(
        self,
        models: Dict[str, BaseEstimator],
        weights: Optional[Dict[str, float]] = None,
        task_type: str = "classification"
    ):
        """
        Initialize the WeightedEnsemble.
        
        Args:
            models: Dictionary of trained models
            weights: Dictionary of model weights (if None, equal weights are used)
            task_type: Task type ('classification' or 'regression')
        """
        self.models = models
        self.weights = weights or {name: 1.0 / len(models) for name in models}
        self.task_type = task_type
        
        # Normalize weights to sum to 1
        total_weight = sum(self.weights.values())
        self.weights = {name: weight / total_weight for name, weight in self.weights.items()}
        
        # Store model names
        self.model_names = list(models.keys())
        
        # Store feature names (if available)
        self.feature_names = None
        
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'WeightedEnsemble':
        """
        Fit the ensemble (does nothing as models are already trained).
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Fitted ensemble
        """
        # Store feature names
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the ensemble.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        if self.task_type == "classification":
            # For classification, use weighted voting
            return self._predict_classification(X)
        else:
            # For regression, use weighted average
            return self._predict_regression(X)
    
    def _predict_classification(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make classification predictions using the ensemble.
        
        Args:
            X: Features
            
        Returns:
            Class predictions
        """
        # Get predictions from all models
        if all(hasattr(model, "predict_proba") for model in self.models.values()):
            # If all models support predict_proba, use probability predictions
            probas = self.predict_proba(X)
            return np.argmax(probas, axis=1)
        else:
            # Otherwise, use class predictions
            predictions = {}
            for name, model in self.models.items():
                predictions[name] = model.predict(X)
                
            # Initialize weighted predictions
            weighted_preds = np.zeros(len(X))
            
            # Combine predictions with weights
            for name, preds in predictions.items():
                weighted_preds += self.weights[name] * preds
                
            # Round to nearest class
            return np.round(weighted_preds).astype(int)
    
    def _predict_regression(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make regression predictions using the ensemble.
        
        Args:
            X: Features
            
        Returns:
            Regression predictions
        """
        # Get predictions from all models
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X)
            
        # Initialize weighted predictions
        weighted_preds = np.zeros(len(X))
        
        # Combine predictions with weights
        for name, preds in predictions.items():
            weighted_preds += self.weights[name] * preds
            
        return weighted_preds
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make probability predictions using the ensemble.
        
        Args:
            X: Features
            
        Returns:
            Probability predictions
        """
        # Check if task type is classification
        if self.task_type != "classification":
            raise ValueError("Probability predictions are only available for classification tasks.")
            
        # Check if all models support predict_proba
        if not all(hasattr(model, "predict_proba") for model in self.models.values()):
            raise ValueError("Not all models support probability predictions.")
            
        # Get probability predictions from all models
        probas = {}
        for name, model in self.models.items():
            probas[name] = model.predict_proba(X)
            
        # Initialize weighted probabilities
        n_samples = len(X)
        n_classes = probas[self.model_names[0]].shape[1]
        weighted_probas = np.zeros((n_samples, n_classes))
        
        # Combine probabilities with weights
        for name, proba in probas.items():
            weighted_probas += self.weights[name] * proba
            
        return weighted_probas
    
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """
        Get parameters for this estimator.
        
        Args:
            deep: If True, will return the parameters for this estimator and
                contained subobjects that are estimators.
                
        Returns:
            Parameter names mapped to their values
        """
        return {
            "models": self.models,
            "weights": self.weights,
            "task_type": self.task_type
        }
    
    def set_params(self, **params) -> 'WeightedEnsemble':
        """
        Set the parameters of this estimator.
        
        Args:
            **params: Estimator parameters
            
        Returns:
            Self
        """
        for key, value in params.items():
            setattr(self, key, value)
        return self


class StackingEnsemble(BaseEstimator):
    """
    Stacking ensemble of models for improved prediction performance.
    """
    
    def __init__(
        self,
        base_models: Dict[str, BaseEstimator],
        meta_model: BaseEstimator,
        task_type: str = "classification",
        use_features: bool = False,
        cv: int = 5,
        random_state: int = 42
    ):
        """
        Initialize the StackingEnsemble.
        
        Args:
            base_models: Dictionary of base models
            meta_model: Meta model for combining base model predictions
            task_type: Task type ('classification' or 'regression')
            use_features: Whether to include original features in meta model
            cv: Number of cross-validation folds for base model predictions
            random_state: Random seed for reproducibility
        """
        self.base_models = base_models
        self.meta_model = meta_model
        self.task_type = task_type
        self.use_features = use_features
        self.cv = cv
        self.random_state = random_state
        
        # Store model names
        self.base_model_names = list(base_models.keys())
        
        # Store feature names (if available)
        self.feature_names = None
        
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'StackingEnsemble':
        """
        Fit the stacking ensemble.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Fitted ensemble
        """
        # Store feature names
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            
        # Generate base model predictions using cross-validation
        base_preds = self._get_base_predictions(X, y)
        
        # Prepare meta features
        meta_features = self._prepare_meta_features(X, base_preds)
        
        # Store meta feature column names for consistent prediction
        self.meta_feature_columns = meta_features.columns.tolist()
        
        # Fit meta model
        self.meta_model.fit(meta_features, y)
        
        # Fit base models on full data
        for name, model in self.base_models.items():
            model.fit(X, y)
            
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the stacking ensemble.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        # Get base model predictions
        base_preds = {}
        for name, model in self.base_models.items():
            if self.task_type == "classification" and hasattr(model, "predict_proba"):
                # For classification, use probability predictions if available
                proba = model.predict_proba(X)
                # Store all class probabilities
                for i in range(proba.shape[1]):
                    base_preds[f"{name}_class_{i}"] = proba[:, i]
            else:
                # Otherwise, use regular predictions
                base_preds[name] = model.predict(X)
                
        # Prepare meta features
        meta_features = self._prepare_meta_features(X, base_preds)
        
        # Ensure meta features match those used during training
        if hasattr(self, 'meta_feature_columns'):
            # Add missing columns with zeros
            for col in self.meta_feature_columns:
                if col not in meta_features.columns:
                    meta_features[col] = 0.0
            
            # Reorder columns to match training order and select only needed columns
            meta_features = meta_features[self.meta_feature_columns]
        
        # Make predictions with meta model
        return self.meta_model.predict(meta_features)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make probability predictions using the stacking ensemble.
        
        Args:
            X: Features
            
        Returns:
            Probability predictions
        """
        # Check if task type is classification
        if self.task_type != "classification":
            raise ValueError("Probability predictions are only available for classification tasks.")
            
        # Check if meta model supports predict_proba
        if not hasattr(self.meta_model, "predict_proba"):
            raise ValueError("Meta model does not support probability predictions.")
            
        # Get base model predictions
        base_preds = {}
        for name, model in self.base_models.items():
            if hasattr(model, "predict_proba"):
                # For classification, use probability predictions if available
                proba = model.predict_proba(X)
                # Store all class probabilities
                for i in range(proba.shape[1]):
                    base_preds[f"{name}_class_{i}"] = proba[:, i]
            else:
                # Otherwise, use regular predictions
                base_preds[name] = model.predict(X)
                
        # Prepare meta features
        meta_features = self._prepare_meta_features(X, base_preds)
        
        # Ensure meta features match those used during training
        if hasattr(self, 'meta_feature_columns'):
            # Add missing columns with zeros
            for col in self.meta_feature_columns:
                if col not in meta_features.columns:
                    meta_features[col] = 0.0
            
            # Reorder columns to match training order and select only needed columns
            meta_features = meta_features[self.meta_feature_columns]
        
        # Make probability predictions with meta model
        return self.meta_model.predict_proba(meta_features)
    
    def _get_base_predictions(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, np.ndarray]:
        """
        Generate base model predictions using cross-validation.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Dictionary of base model predictions
        """
        from sklearn.model_selection import KFold, StratifiedKFold
        
        # Initialize predictions
        base_preds = {}
        for name in self.base_model_names:
            base_preds[name] = np.zeros(len(X))
            
        # Initialize cross-validation
        if self.task_type == "classification":
            cv = StratifiedKFold(n_splits=self.cv, shuffle=True, random_state=self.random_state)
        else:
            cv = KFold(n_splits=self.cv, shuffle=True, random_state=self.random_state)
            
        # Generate predictions for each fold
        for train_idx, val_idx in cv.split(X, y):
            # Split data
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train = y.iloc[train_idx]
            
            # Train and predict with each base model
            for name, model in self.base_models.items():
                # Clone model
                from sklearn.base import clone
                model_clone = clone(model)
                
                # Fit model
                model_clone.fit(X_train, y_train)
                
                # Make predictions
                if self.task_type == "classification" and hasattr(model_clone, "predict_proba"):
                    # For classification, use probability predictions if available
                    proba = model_clone.predict_proba(X_val)
                    # Store all class probabilities
                    for i in range(proba.shape[1]):
                        if f"{name}_class_{i}" not in base_preds:
                            base_preds[f"{name}_class_{i}"] = np.zeros(len(X))
                        base_preds[f"{name}_class_{i}"][val_idx] = proba[:, i]
                else:
                    # Otherwise, use regular predictions
                    base_preds[name][val_idx] = model_clone.predict(X_val)
                    
        return base_preds
    
    def _prepare_meta_features(self, X: pd.DataFrame, base_preds: Dict[str, np.ndarray]) -> pd.DataFrame:
        """
        Prepare meta features for meta model.
        
        Args:
            X: Original features
            base_preds: Base model predictions
            
        Returns:
            Meta features
        """
        # Convert base predictions to DataFrame with consistent column names
        meta_features = pd.DataFrame()
        
        # Add base model predictions with consistent column names
        for name, pred in base_preds.items():
            if isinstance(pred, np.ndarray):
                if pred.ndim > 1 and pred.shape[1] > 1:
                    # For multi-class probabilities
                    for i in range(pred.shape[1]):
                        meta_features[f"{name}_class_{i}"] = pred[:, i]
                else:
                    # For single predictions
                    meta_features[name] = pred.ravel()
        
        # Include original features if requested
        if self.use_features:
            # Ensure X is a DataFrame
            if not isinstance(X, pd.DataFrame):
                X = pd.DataFrame(X)
                
            # Combine base predictions with original features
            meta_features = pd.concat([meta_features, X.reset_index(drop=True)], axis=1)
            
        return meta_features
    
    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """
        Get parameters for this estimator.
        
        Args:
            deep: If True, will return the parameters for this estimator and
                contained subobjects that are estimators.
                
        Returns:
            Parameter names mapped to their values
        """
        return {
            "base_models": self.base_models,
            "meta_model": self.meta_model,
            "task_type": self.task_type,
            "use_features": self.use_features,
            "cv": self.cv,
            "random_state": self.random_state
        }
    
    def set_params(self, **params) -> 'StackingEnsemble':
        """
        Set the parameters of this estimator.
        
        Args:
            **params: Estimator parameters
            
        Returns:
            Self
        """
        for key, value in params.items():
            setattr(self, key, value)
        return self


# Example Usage (for testing purposes)
if __name__ == "__main__":
    print("Running Ensemble Example...")
    
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    # Create features
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples),
        'feature3': np.random.normal(0, 1, n_samples),
        'feature4': np.random.normal(0, 1, n_samples)
    })
    
    # Create classification target
    y = (X['feature1'] + X['feature2'] > 0).astype(int)
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create models
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    
    models = {
        'random_forest': RandomForestClassifier(random_state=42),
        'logistic_regression': LogisticRegression(random_state=42),
        'svm': SVC(probability=True, random_state=42)
    }
    
    # Train models
    for name, model in models.items():
        model.fit(X_train, y_train)
        
    # Create weighted ensemble
    weights = {
        'random_forest': 0.5,
        'logistic_regression': 0.3,
        'svm': 0.2
    }
    
    weighted_ensemble = WeightedEnsemble(
        models=models,
        weights=weights,
        task_type='classification'
    )
    
    # Create stacking ensemble
    meta_model = LogisticRegression(random_state=42)
    
    stacking_ensemble = StackingEnsemble(
        base_models=models,
        meta_model=meta_model,
        task_type='classification',
        use_features=True,
        cv=5,
        random_state=42
    )
    
    # Fit stacking ensemble
    stacking_ensemble.fit(X_train, y_train)
    
    # Make predictions
    from sklearn.metrics import accuracy_score
    
    # Individual models
    individual_scores = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        individual_scores[name] = accuracy_score(y_test, y_pred)
        
    # Weighted ensemble
    y_pred_weighted = weighted_ensemble.predict(X_test)
    weighted_score = accuracy_score(y_test, y_pred_weighted)
    
    # Stacking ensemble
    y_pred_stacking = stacking_ensemble.predict(X_test)
    stacking_score = accuracy_score(y_test, y_pred_stacking)
    
    # Print results
    print("\nAccuracy Scores:")
    for name, score in individual_scores.items():
        print(f"  • {name}: {score:.4f}")
    print(f"  • Weighted Ensemble: {weighted_score:.4f}")
    print(f"  • Stacking Ensemble: {stacking_score:.4f}")
    
    print("\nEnsemble example completed successfully!")
