#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model Selector Module for HumanML.

Provides functionality for selecting appropriate machine learning models based on
dataset characteristics and user preferences.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor


class ModelSelector:
    """
    Select appropriate machine learning models based on dataset characteristics and user preferences.
    """
    
    def __init__(
        self,
        preference: str = "balanced",
        excluded_models: Optional[List[str]] = None,
        included_models: Optional[List[str]] = None,
        verbose: bool = True,
        n_jobs: int = -1,
        random_state: int = 42
    ):
        """
        Initialize the ModelSelector.
        
        Args:
            preference: Model selection preference ('accuracy', 'speed', 'interpretability', 'balanced')
            excluded_models: List of model names to exclude
            included_models: List of model names to include (overrides excluded_models)
            verbose: Whether to print detailed information
            n_jobs: Number of jobs to run in parallel
            random_state: Random seed for reproducibility
        """
        self.preference = preference
        self.excluded_models = excluded_models or []
        self.included_models = included_models or []
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.random_state = random_state
        
        # Initialize selection results
        self.selection_results = {}
        
        # Define model categories
        self.model_categories = {
            "linear": ["LogisticRegression", "LinearRegression", "Ridge", "Lasso", "ElasticNet"],
            "tree": ["DecisionTree"],
            "ensemble": ["RandomForest", "GradientBoosting"],
            "svm": ["SVM"],
            "knn": ["KNN"]
        }
        
        # Define model characteristics
        self.model_characteristics = {
            "LogisticRegression": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "high",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "classification"
            },
            "DecisionTreeClassifier": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "medium",
                "scalability": "medium",
                "handles_missing": True,
                "handles_categorical": True,
                "handles_imbalance": False,
                "task_type": "classification"
            },
            "DecisionTreeRegressor": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "medium",
                "scalability": "medium",
                "handles_missing": True,
                "handles_categorical": True,
                "handles_imbalance": False,
                "task_type": "regression"
            },
            "RandomForestClassifier": {
                "speed": "medium",
                "interpretability": "medium",
                "accuracy": "high",
                "complexity": "medium",
                "scalability": "high",
                "handles_missing": True,
                "handles_categorical": True,
                "handles_imbalance": True,
                "task_type": "classification"
            },
            "RandomForestRegressor": {
                "speed": "medium",
                "interpretability": "medium",
                "accuracy": "high",
                "complexity": "medium",
                "scalability": "high",
                "handles_missing": True,
                "handles_categorical": True,
                "handles_imbalance": True,
                "task_type": "regression"
            },
            "GradientBoostingClassifier": {
                "speed": "slow",
                "interpretability": "low",
                "accuracy": "high",
                "complexity": "high",
                "scalability": "medium",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": True,
                "task_type": "classification"
            },
            "GradientBoostingRegressor": {
                "speed": "slow",
                "interpretability": "low",
                "accuracy": "high",
                "complexity": "high",
                "scalability": "medium",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": True,
                "task_type": "regression"
            },
            "SVC": {
                "speed": "slow",
                "interpretability": "low",
                "accuracy": "high",
                "complexity": "high",
                "scalability": "low",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "classification"
            },
            "SVR": {
                "speed": "slow",
                "interpretability": "low",
                "accuracy": "high",
                "complexity": "high",
                "scalability": "low",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "regression"
            },
            "KNeighborsClassifier": {
                "speed": "medium",
                "interpretability": "medium",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "low",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "classification"
            },
            "KNeighborsRegressor": {
                "speed": "medium",
                "interpretability": "medium",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "low",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "regression"
            },
            "LinearRegression": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "high",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "regression"
            },
            "Ridge": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "high",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "regression"
            },
            "Lasso": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "high",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "regression"
            },
            "ElasticNet": {
                "speed": "fast",
                "interpretability": "high",
                "accuracy": "medium",
                "complexity": "low",
                "scalability": "high",
                "handles_missing": False,
                "handles_categorical": False,
                "handles_imbalance": False,
                "task_type": "regression"
            }
        }
        
        # Map model names to their class names for lookup
        self.model_name_to_class = {
            "LogisticRegression": "LogisticRegression",
            "LinearRegression": "LinearRegression",
            "Ridge": "Ridge",
            "Lasso": "Lasso",
            "ElasticNet": "ElasticNet",
            "DecisionTreeClassifier": "DecisionTreeClassifier",
            "DecisionTreeRegressor": "DecisionTreeRegressor",
            "RandomForestClassifier": "RandomForestClassifier",
            "RandomForestRegressor": "RandomForestRegressor",
            "GradientBoostingClassifier": "GradientBoostingClassifier",
            "GradientBoostingRegressor": "GradientBoostingRegressor",
            "SVC": "SVC",
            "SVR": "SVR",
            "KNeighborsClassifier": "KNeighborsClassifier",
            "KNeighborsRegressor": "KNeighborsRegressor"
        }
        
    def select_models(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        task_type: str
    ) -> Dict[str, Any]:
        """
        Select models based on dataset characteristics and user preferences.
        
        Args:
            X: Features
            y: Target
            task_type: Task type ('classification' or 'regression')
            
        Returns:
            Dictionary of selected models
        """
        # Validate task type
        if task_type not in ["classification", "regression"]:
            raise ValueError(f"Invalid task type: {task_type}. Must be 'classification' or 'regression'.")
            
        # Analyze dataset
        dataset_characteristics = self._analyze_dataset(X, y, task_type)
        
        # Get available models for task type
        available_models = self._get_available_models(task_type)
        
        # Filter models based on dataset characteristics
        filtered_models = self._filter_models(available_models, dataset_characteristics)
        
        # Rank models based on preference
        ranked_models = self._rank_models(filtered_models, dataset_characteristics)
        
        # Select top models
        selected_models = self._select_top_models(ranked_models, dataset_characteristics)
        
        # Ensure at least one model is selected
        if not selected_models:
            selected_models = self._ensure_default_models(task_type)
            
        # Store selection results
        self.selection_results = {
            "dataset_characteristics": dataset_characteristics,
            "available_models": list(available_models.keys()),
            "filtered_models": list(filtered_models.keys()),
            "ranked_models": {name: rank for name, rank in ranked_models},
            "selected_models": list(selected_models.keys()),
            "task_type": task_type  # Store task type for reference
        }
        
        return selected_models
    
    def _analyze_dataset(self, X: pd.DataFrame, y: pd.Series, task_type: str) -> Dict[str, Any]:
        """
        Analyze dataset characteristics.
        
        Args:
            X: Features
            y: Target
            task_type: Task type ('classification' or 'regression')
            
        Returns:
            Dictionary with dataset characteristics
        """
        # Get basic dataset characteristics
        n_samples = len(X)
        n_features = X.shape[1]
        n_categorical = sum(pd.api.types.is_categorical_dtype(X[col]) or X[col].dtype == 'object' for col in X.columns)
        n_numeric = sum(pd.api.types.is_numeric_dtype(X[col]) for col in X.columns)
        n_missing = X.isna().sum().sum()
        missing_ratio = n_missing / (n_samples * n_features) if n_samples * n_features > 0 else 0
        
        # Get additional characteristics based on task type
        if task_type == 'classification':
            n_classes = y.nunique()
            class_distribution = y.value_counts().to_dict()
            class_imbalance = max(class_distribution.values()) / min(class_distribution.values()) if len(class_distribution) > 1 else 1
            is_imbalanced = class_imbalance > 5  # Consider imbalanced if ratio > 5
            
            # Store classification-specific characteristics
            characteristics = {
                "n_samples": n_samples,
                "n_features": n_features,
                "n_categorical": n_categorical,
                "n_numeric": n_numeric,
                "n_missing": n_missing,
                "missing_ratio": missing_ratio,
                "n_classes": n_classes,
                "class_distribution": class_distribution,
                "class_imbalance": class_imbalance,
                "is_imbalanced": is_imbalanced,
                "is_multiclass": n_classes > 2,
                "is_binary": n_classes == 2,
                "task_type": task_type  # Store task type for reference
            }
        else:
            # Regression-specific characteristics
            target_min = float(y.min())
            target_max = float(y.max())
            target_mean = float(y.mean())
            target_std = float(y.std())
            target_skew = float(y.skew()) if hasattr(y, 'skew') else 0
            
            # Store regression-specific characteristics
            characteristics = {
                "n_samples": n_samples,
                "n_features": n_features,
                "n_categorical": n_categorical,
                "n_numeric": n_numeric,
                "n_missing": n_missing,
                "missing_ratio": missing_ratio,
                "target_min": target_min,
                "target_max": target_max,
                "target_mean": target_mean,
                "target_std": target_std,
                "target_skew": target_skew,
                "target_range": target_max - target_min,
                "task_type": task_type  # Store task type for reference
            }
            
        # Determine dataset size category
        if n_samples < 100:
            characteristics["size_category"] = "very_small"
        elif n_samples < 1000:
            characteristics["size_category"] = "small"
        elif n_samples < 10000:
            characteristics["size_category"] = "medium"
        elif n_samples < 100000:
            characteristics["size_category"] = "large"
        else:
            characteristics["size_category"] = "very_large"
            
        # Determine feature complexity
        if n_features < 10:
            characteristics["feature_complexity"] = "low"
        elif n_features < 50:
            characteristics["feature_complexity"] = "medium"
        elif n_features < 100:
            characteristics["feature_complexity"] = "high"
        else:
            characteristics["feature_complexity"] = "very_high"
            
        # Check for feature correlations
        if n_numeric > 1:
            try:
                numeric_cols = X.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 1:
                    correlation_matrix = X[numeric_cols].corr().abs()
                    np.fill_diagonal(correlation_matrix.values, 0)
                    max_correlation = correlation_matrix.max().max()
                    characteristics["max_correlation"] = float(max_correlation)
                    characteristics["has_high_correlation"] = max_correlation > 0.8
                else:
                    characteristics["max_correlation"] = 0
                    characteristics["has_high_correlation"] = False
            except Exception:
                characteristics["max_correlation"] = 0
                characteristics["has_high_correlation"] = False
        else:
            characteristics["max_correlation"] = 0
            characteristics["has_high_correlation"] = False
            
        return characteristics
    
    def _get_available_models(self, task_type: str) -> Dict[str, Any]:
        """
        Get available models for task type.
        
        Args:
            task_type: Task type ('classification' or 'regression')
            
        Returns:
            Dictionary of available models
        """
        # Validate task type
        if task_type not in ["classification", "regression"]:
            raise ValueError(f"Invalid task type: {task_type}. Must be 'classification' or 'regression'.")
            
        # Get models specific to task type
        if task_type == 'classification':
            available_models = {
                "LogisticRegression": LogisticRegression,
                "DecisionTreeClassifier": DecisionTreeClassifier,
                "RandomForestClassifier": RandomForestClassifier,
                "GradientBoostingClassifier": GradientBoostingClassifier,
                "SVC": SVC,
                "KNeighborsClassifier": KNeighborsClassifier
            }
        else:  # regression
            available_models = {
                "LinearRegression": LinearRegression,
                "DecisionTreeRegressor": DecisionTreeRegressor,
                "RandomForestRegressor": RandomForestRegressor,
                "GradientBoostingRegressor": GradientBoostingRegressor,
                "Ridge": Ridge,
                "Lasso": Lasso,
                "ElasticNet": ElasticNet,
                "SVR": SVR,
                "KNeighborsRegressor": KNeighborsRegressor
            }
            
        # Filter models based on included/excluded lists
        if self.included_models:
            # Convert included_models to actual class names if they're in simplified form
            processed_included = []
            for model_name in self.included_models:
                if model_name in available_models:
                    # Already in correct format
                    processed_included.append(model_name)
                elif model_name == "DecisionTree":
                    # Add appropriate variant based on task type
                    if task_type == "classification":
                        processed_included.append("DecisionTreeClassifier")
                    else:
                        processed_included.append("DecisionTreeRegressor")
                elif model_name == "RandomForest":
                    # Add appropriate variant based on task type
                    if task_type == "classification":
                        processed_included.append("RandomForestClassifier")
                    else:
                        processed_included.append("RandomForestRegressor")
                elif model_name == "GradientBoosting":
                    # Add appropriate variant based on task type
                    if task_type == "classification":
                        processed_included.append("GradientBoostingClassifier")
                    else:
                        processed_included.append("GradientBoostingRegressor")
                elif model_name == "SVM":
                    # Add appropriate variant based on task type
                    if task_type == "classification":
                        processed_included.append("SVC")
                    else:
                        processed_included.append("SVR")
                elif model_name == "KNN":
                    # Add appropriate variant based on task type
                    if task_type == "classification":
                        processed_included.append("KNeighborsClassifier")
                    else:
                        processed_included.append("KNeighborsRegressor")
                    
            # Filter available models based on processed included list
            available_models = {name: model for name, model in available_models.items() if name in processed_included}
        else:
            # Process excluded models similarly
            processed_excluded = []
            for model_name in self.excluded_models:
                if model_name in available_models:
                    processed_excluded.append(model_name)
                elif model_name == "DecisionTree":
                    if task_type == "classification":
                        processed_excluded.append("DecisionTreeClassifier")
                    else:
                        processed_excluded.append("DecisionTreeRegressor")
                elif model_name == "RandomForest":
                    if task_type == "classification":
                        processed_excluded.append("RandomForestClassifier")
                    else:
                        processed_excluded.append("RandomForestRegressor")
                elif model_name == "GradientBoosting":
                    if task_type == "classification":
                        processed_excluded.append("GradientBoostingClassifier")
                    else:
                        processed_excluded.append("GradientBoostingRegressor")
                elif model_name == "SVM":
                    if task_type == "classification":
                        processed_excluded.append("SVC")
                    else:
                        processed_excluded.append("SVR")
                elif model_name == "KNN":
                    if task_type == "classification":
                        processed_excluded.append("KNeighborsClassifier")
                    else:
                        processed_excluded.append("KNeighborsRegressor")
                    
            # Filter available models based on processed excluded list
            available_models = {name: model for name, model in available_models.items() if name not in processed_excluded}
            
        return available_models
    
    def _filter_models(self, available_models: Dict[str, Any], dataset_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter models based on dataset characteristics.
        
        Args:
            available_models: Dictionary of available models
            dataset_characteristics: Dictionary with dataset characteristics
            
        Returns:
            Dictionary of filtered models
        """
        # Initialize filtered models
        filtered_models = {}
        
        # Get task type
        task_type = dataset_characteristics["task_type"]
        
        # Filter models based on dataset characteristics
        for name, model_class in available_models.items():
            # Check if model is suitable for dataset
            is_suitable = True
            
            # Check if model is suitable for dataset size
            if dataset_characteristics["size_category"] == "very_large" and name in ["SVC", "SVR", "KNeighborsClassifier", "KNeighborsRegressor"]:
                is_suitable = False
                
            # Check if model is suitable for feature complexity
            if dataset_characteristics["feature_complexity"] == "very_high" and name in ["SVC", "SVR"]:
                is_suitable = False
                
            # Check if model is suitable for missing values
            if dataset_characteristics["missing_ratio"] > 0 and not self.model_characteristics.get(name, {}).get("handles_missing", False):
                # Model doesn't handle missing values, but we'll still include it
                # as preprocessing can handle missing values
                pass
                
            # Check if model is suitable for imbalanced data
            if task_type == "classification" and dataset_characteristics.get("is_imbalanced", False) and not self.model_characteristics.get(name, {}).get("handles_imbalance", False):
                # Model doesn't handle imbalanced data well, but we'll still include it
                # as preprocessing can handle imbalanced data
                pass
                
            # Add model to filtered models if suitable
            if is_suitable:
                filtered_models[name] = model_class
                
        # If no models are suitable, return all available models
        if not filtered_models:
            return available_models
            
        return filtered_models
    
    def _rank_models(self, filtered_models: Dict[str, Any], dataset_characteristics: Dict[str, Any]) -> List[Tuple[str, float]]:
        """
        Rank models based on preference and dataset characteristics.
        
        Args:
            filtered_models: Dictionary of filtered models
            dataset_characteristics: Dictionary with dataset characteristics
            
        Returns:
            List of tuples (model_name, rank)
        """
        # Initialize ranks
        ranks = {}
        
        # Get task type
        task_type = dataset_characteristics["task_type"]
        
        # Rank models based on preference
        for name in filtered_models.keys():
            # Initialize rank
            rank = 0
            
            # Get model characteristics
            model_chars = self.model_characteristics.get(name, {})
            
            # Rank based on preference
            if self.preference == "accuracy":
                if model_chars.get("accuracy") == "high":
                    rank += 3
                elif model_chars.get("accuracy") == "medium":
                    rank += 2
                else:
                    rank += 1
            elif self.preference == "speed":
                if model_chars.get("speed") == "fast":
                    rank += 3
                elif model_chars.get("speed") == "medium":
                    rank += 2
                else:
                    rank += 1
            elif self.preference == "interpretability":
                if model_chars.get("interpretability") == "high":
                    rank += 3
                elif model_chars.get("interpretability") == "medium":
                    rank += 2
                else:
                    rank += 1
            else:  # balanced
                # Combine accuracy, speed, and interpretability
                if model_chars.get("accuracy") == "high":
                    rank += 2
                elif model_chars.get("accuracy") == "medium":
                    rank += 1
                    
                if model_chars.get("speed") == "fast":
                    rank += 1
                    
                if model_chars.get("interpretability") == "high":
                    rank += 1
                    
            # Additional ranking based on dataset characteristics
            if dataset_characteristics["size_category"] in ["large", "very_large"]:
                if model_chars.get("scalability") == "high":
                    rank += 1
                    
            if task_type == "classification" and dataset_characteristics.get("is_imbalanced", False):
                if model_chars.get("handles_imbalance", False):
                    rank += 1
                    
            if dataset_characteristics["missing_ratio"] > 0:
                if model_chars.get("handles_missing", False):
                    rank += 1
                    
            # Store rank
            ranks[name] = rank
            
        # Sort models by rank (descending)
        ranked_models = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
        
        return ranked_models
    
    def _select_top_models(self, ranked_models: List[Tuple[str, float]], dataset_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select top models based on ranks.
        
        Args:
            ranked_models: List of tuples (model_name, rank)
            dataset_characteristics: Dictionary with dataset characteristics
            
        Returns:
            Dictionary of selected models
        """
        # Get task type
        task_type = dataset_characteristics["task_type"]
        
        # Determine number of models to select
        if dataset_characteristics["size_category"] in ["very_small", "small"]:
            n_models = min(3, len(ranked_models))
        elif dataset_characteristics["size_category"] == "medium":
            n_models = min(4, len(ranked_models))
        else:
            n_models = min(5, len(ranked_models))
            
        # Select top models - return class types, not instances
        selected_models = {}
        for name, _ in ranked_models[:n_models]:
            if name in ["LogisticRegression", "LinearRegression", "Ridge", "Lasso", "ElasticNet", 
                       "DecisionTreeClassifier", "DecisionTreeRegressor", 
                       "RandomForestClassifier", "RandomForestRegressor",
                       "GradientBoostingClassifier", "GradientBoostingRegressor",
                       "SVC", "SVR", "KNeighborsClassifier", "KNeighborsRegressor"]:
                # Get the class from the name
                if task_type == "classification":
                    if name == "LogisticRegression":
                        selected_models[name] = LogisticRegression
                    elif name == "DecisionTreeClassifier":
                        selected_models[name] = DecisionTreeClassifier
                    elif name == "RandomForestClassifier":
                        selected_models[name] = RandomForestClassifier
                    elif name == "GradientBoostingClassifier":
                        selected_models[name] = GradientBoostingClassifier
                    elif name == "SVC":
                        selected_models[name] = SVC
                    elif name == "KNeighborsClassifier":
                        selected_models[name] = KNeighborsClassifier
                else:  # regression
                    if name == "LinearRegression":
                        selected_models[name] = LinearRegression
                    elif name == "DecisionTreeRegressor":
                        selected_models[name] = DecisionTreeRegressor
                    elif name == "RandomForestRegressor":
                        selected_models[name] = RandomForestRegressor
                    elif name == "GradientBoostingRegressor":
                        selected_models[name] = GradientBoostingRegressor
                    elif name == "Ridge":
                        selected_models[name] = Ridge
                    elif name == "Lasso":
                        selected_models[name] = Lasso
                    elif name == "ElasticNet":
                        selected_models[name] = ElasticNet
                    elif name == "SVR":
                        selected_models[name] = SVR
                    elif name == "KNeighborsRegressor":
                        selected_models[name] = KNeighborsRegressor
                    
        return selected_models
    
    def _ensure_default_models(self, task_type: str) -> Dict[str, Any]:
        """
        Ensure at least one model is selected by providing default models.
        
        Args:
            task_type: Task type ('classification' or 'regression')
            
        Returns:
            Dictionary of default models
        """
        # Initialize default models
        default_models = {}
        
        # Add default models based on task type - return class types, not instances
        if task_type == "classification":
            default_models["LogisticRegression"] = LogisticRegression
            default_models["RandomForestClassifier"] = RandomForestClassifier
            default_models["GradientBoostingClassifier"] = GradientBoostingClassifier
        else:  # regression
            default_models["LinearRegression"] = LinearRegression
            default_models["RandomForestRegressor"] = RandomForestRegressor
            default_models["GradientBoostingRegressor"] = GradientBoostingRegressor
            
        return default_models
    
    def get_selection_results(self) -> Dict[str, Any]:
        """
        Get selection results.
        
        Returns:
            Dictionary with selection results
        """
        return self.selection_results
