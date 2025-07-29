#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Splitter Module for HumanML.

Provides functionality for splitting data into training, validation, and test sets.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple
from sklearn.model_selection import train_test_split


class DataSplitter:
    """
    Split data into training, validation, and test sets.
    """
    
    def __init__(
        self,
        test_size: float = 0.2,
        validation_size: float = 0.1,
        random_state: int = 42,
        n_splits: int = 5
    ):
        """
        Initialize the DataSplitter.
        
        Args:
            test_size: Proportion of data to use for testing
            validation_size: Proportion of training data to use for validation
            random_state: Random seed for reproducibility
            n_splits: Number of cross-validation splits
        """
        self.test_size = test_size
        self.validation_size = validation_size
        self.random_state = random_state
        self.n_splits = n_splits
        
    def split_data(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, pd.DataFrame]:
        """
        Split data into training, validation, and test sets.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Dictionary with split data
        """
        # Split data into train+val and test sets
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, 
            test_size=self.test_size, 
            random_state=self.random_state
        )
        
        # Split train+val into train and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val,
            test_size=self.validation_size / (1 - self.test_size),
            random_state=self.random_state
        )
        
        # Return split data
        return {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test
        }


# Example Usage (for testing purposes)
if __name__ == "__main__":
    print("Running DataSplitter Example...")
    
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
    
    # Create target
    y = pd.Series(np.random.randint(0, 2, n_samples), name="target")
    
    # Initialize data splitter
    splitter = DataSplitter(
        test_size=0.2,
        validation_size=0.1,
        random_state=42
    )
    
    # Split data
    split_data = splitter.split_data(X, y)
    
    # Print split data shapes
    print(f"X_train shape: {split_data['X_train'].shape}")
    print(f"X_val shape: {split_data['X_val'].shape}")
    print(f"X_test shape: {split_data['X_test'].shape}")
    print(f"y_train shape: {split_data['y_train'].shape}")
    print(f"y_val shape: {split_data['y_val'].shape}")
    print(f"y_test shape: {split_data['y_test'].shape}")
    
    print("DataSplitter example completed successfully!")
