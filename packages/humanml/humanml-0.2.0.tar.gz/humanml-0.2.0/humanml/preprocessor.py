#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Preprocessor Module for HumanML.

Provides comprehensive data preprocessing capabilities with automatic feature type detection,
missing value imputation, categorical encoding, feature scaling, and outlier handling.
"""

import time
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin


class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extract features from datetime columns.
    """
    
    def fit(self, X, y=None):
        """
        Fit transformer.
        
        Args:
            X: Features
            y: Target (optional)
            
        Returns:
            Self
        """
        return self
    
    def transform(self, X):
        """
        Transform datetime features.
        
        Args:
            X: Features
            
        Returns:
            Transformed features
        """
        X_copy = X.copy()
        
        # Convert to datetime if not already
        for column in X_copy.columns:
            if not pd.api.types.is_datetime64_dtype(X_copy[column]):
                X_copy[column] = pd.to_datetime(X_copy[column], errors='coerce')
                
        # Extract features
        result = pd.DataFrame()
        
        for column in X_copy.columns:
            result[f"{column}_year"] = X_copy[column].dt.year
            result[f"{column}_month"] = X_copy[column].dt.month
            result[f"{column}_day"] = X_copy[column].dt.day
            result[f"{column}_dayofweek"] = X_copy[column].dt.dayofweek
            result[f"{column}_dayofyear"] = X_copy[column].dt.dayofyear
            result[f"{column}_quarter"] = X_copy[column].dt.quarter
            
        return result.values


class Preprocessor:
    """
    Comprehensive data preprocessor with automatic feature type detection,
    missing value imputation, categorical encoding, feature scaling, and outlier handling.
    """
    
    def __init__(
        self,
        verbose: bool = True,
        random_state: int = 42,
        n_jobs: int = -1
    ):
        """
        Initialize the Preprocessor.
        
        Args:
            verbose: Whether to print detailed information
            random_state: Random seed for reproducibility
            n_jobs: Number of jobs to run in parallel
        """
        self.verbose = verbose
        self.random_state = random_state
        self.n_jobs = n_jobs
        
        # Initialize preprocessing results
        self.preprocessing_results = {}
        
        # Initialize feature types
        self.feature_types = {}
        
        # Initialize transformers
        self.transformer = None
        
    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fit preprocessor to data and transform it.
        
        Args:
            X: Features
            y: Target (optional)
            
        Returns:
            Transformed features
        """
        # Detect feature types
        self._detect_feature_types(X)
        
        # Create preprocessing pipeline
        self._create_preprocessing_pipeline()
        
        # Fit and transform data
        if self.verbose:
            print("Preprocessing data...")
            
        start_time = time.time()
        X_transformed = self.transformer.fit_transform(X)
        end_time = time.time()
        
        # Convert to DataFrame with feature names
        feature_names = self._get_feature_names_out()
        X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)
        
        # Store preprocessing results
        self.preprocessing_results = {
            "n_samples": len(X),
            "n_features_original": X.shape[1],
            "n_features_transformed": X_transformed_df.shape[1],
            "feature_types": self.feature_types,
            "feature_names_original": X.columns.tolist(),
            "feature_names_transformed": feature_names,
            "preprocessing_time": end_time - start_time
        }
        
        if self.verbose:
            print(f"Preprocessing completed in {end_time - start_time:.2f} seconds")
            print(f"Original features: {X.shape[1]}")
            print(f"Transformed features: {X_transformed_df.shape[1]}")
            
        return X_transformed_df
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data using fitted preprocessor.
        
        Args:
            X: Features
            
        Returns:
            Transformed features
        """
        # Check if preprocessor has been fitted
        if self.transformer is None:
            raise ValueError("Preprocessor has not been fitted yet. Call 'fit_transform' first.")
            
        # Transform data
        X_transformed = self.transformer.transform(X)
        
        # Convert to DataFrame with feature names
        feature_names = self._get_feature_names_out()
        X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)
        
        return X_transformed_df
    
    def _detect_feature_types(self, X: pd.DataFrame) -> None:
        """
        Detect feature types.
        
        Args:
            X: Features
        """
        if self.verbose:
            print("Detecting feature types...")
            
        # Initialize feature types
        self.feature_types = {
            "numeric": [],
            "categorical": [],
            "date": [],
            "text": [],
            "binary": [],
            "id": []
        }
        
        # Detect feature types
        for column in X.columns:
            # Check if column is numeric
            if pd.api.types.is_numeric_dtype(X[column]):
                # Check if column is binary
                if X[column].nunique() == 2:
                    self.feature_types["binary"].append(column)
                # Check if column is likely an ID
                elif X[column].nunique() == len(X) or column.lower().endswith('id'):
                    self.feature_types["id"].append(column)
                else:
                    self.feature_types["numeric"].append(column)
            # Check if column is datetime
            elif pd.api.types.is_datetime64_dtype(X[column]) or pd.to_datetime(X[column], errors='coerce').notna().all():
                self.feature_types["date"].append(column)
            # Check if column is categorical
            elif X[column].nunique() < 0.2 * len(X):
                self.feature_types["categorical"].append(column)
            # Assume column is text
            else:
                self.feature_types["text"].append(column)
                
        if self.verbose:
            print(f"Numeric features: {len(self.feature_types['numeric'])}")
            print(f"Categorical features: {len(self.feature_types['categorical'])}")
            print(f"Date features: {len(self.feature_types['date'])}")
            print(f"Text features: {len(self.feature_types['text'])}")
            print(f"Binary features: {len(self.feature_types['binary'])}")
            print(f"ID features: {len(self.feature_types['id'])}")
            
    def _create_preprocessing_pipeline(self) -> None:
        """
        Create preprocessing pipeline.
        """
        if self.verbose:
            print("Creating preprocessing pipeline...")
            
        # Create transformers
        transformers = []
        
        # Add numeric transformer
        if self.feature_types["numeric"]:
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            transformers.append(('numeric', numeric_transformer, self.feature_types["numeric"]))
            
        # Add binary transformer
        if self.feature_types["binary"]:
            binary_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('scaler', StandardScaler())
            ])
            transformers.append(('binary', binary_transformer, self.feature_types["binary"]))
            
        # Add categorical transformer
        if self.feature_types["categorical"]:
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            transformers.append(('categorical', categorical_transformer, self.feature_types["categorical"]))
            
        # Add date transformer
        if self.feature_types["date"]:
            date_transformer = Pipeline(steps=[
                ('extractor', DateFeatureExtractor()),
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            transformers.append(('date', date_transformer, self.feature_types["date"]))
            
        # Add text transformer (placeholder)
        if self.feature_types["text"]:
            # For simplicity, just use label encoding for text features
            text_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', LabelEncoder())
            ])
            transformers.append(('text', text_transformer, self.feature_types["text"]))
            
        # Create column transformer
        self.transformer = ColumnTransformer(
            transformers=transformers,
            remainder='drop'
        )
        
    def _get_feature_names_out(self) -> List[str]:
        """
        Get feature names after transformation.
        
        Returns:
            List of feature names
        """
        # Check if transformer has get_feature_names_out method (scikit-learn >= 1.0)
        if hasattr(self.transformer, 'get_feature_names_out'):
            return self.transformer.get_feature_names_out().tolist()
        
        # For older scikit-learn versions, manually construct feature names
        feature_names = []
        
        for name, _, columns in self.transformer.transformers_:
            if name == 'numeric':
                feature_names.extend(columns)
            elif name == 'binary':
                feature_names.extend(columns)
            elif name == 'categorical':
                for column in columns:
                    unique_values = self.transformer.named_transformers_[name].named_steps['encoder'].categories_[0]
                    for value in unique_values:
                        feature_names.append(f"{column}_{value}")
            elif name == 'date':
                for column in columns:
                    feature_names.extend([
                        f"{column}_year",
                        f"{column}_month",
                        f"{column}_day",
                        f"{column}_dayofweek",
                        f"{column}_dayofyear",
                        f"{column}_quarter"
                    ])
            elif name == 'text':
                feature_names.extend(columns)
                
        return feature_names
    
    def get_preprocessing_results(self) -> Dict[str, Any]:
        """
        Get preprocessing results.
        
        Returns:
            Dictionary with preprocessing results
        """
        return self.preprocessing_results


# Example Usage (for testing purposes)
if __name__ == "__main__":
    print("Running Preprocessor Example...")
    
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    # Create features
    X = pd.DataFrame({
        'numeric1': np.random.normal(0, 1, n_samples),
        'numeric2': np.random.normal(0, 1, n_samples),
        'categorical1': np.random.choice(['A', 'B', 'C'], n_samples),
        'categorical2': np.random.choice(['X', 'Y', 'Z'], n_samples),
        'binary1': np.random.choice([0, 1], n_samples),
        'date1': pd.date_range(start='2020-01-01', periods=n_samples),
        'id1': range(n_samples)
    })
    
    # Add missing values
    X.loc[np.random.choice(n_samples, 100), 'numeric1'] = np.nan
    X.loc[np.random.choice(n_samples, 100), 'categorical1'] = np.nan
    
    # Initialize preprocessor
    preprocessor = Preprocessor(verbose=True)
    
    # Fit and transform data
    X_transformed = preprocessor.fit_transform(X)
    
    # Get preprocessing results
    results = preprocessor.get_preprocessing_results()
    
    print("\nPreprocessing Results:")
    print(f"Original features: {results['n_features_original']}")
    print(f"Transformed features: {results['n_features_transformed']}")
    print(f"Preprocessing time: {results['preprocessing_time']:.2f} seconds")
    
    print("\nTransformed Data:")
    print(X_transformed.head())
    
    print("\nPreprocessor example completed successfully!")
