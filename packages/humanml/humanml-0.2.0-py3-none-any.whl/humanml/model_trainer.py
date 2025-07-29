#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model Trainer Module for HumanML.

Provides functionality for training machine learning models with hyperparameter tuning
and cross-validation.
"""

import time
import inspect
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple, Set, Callable
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.base import BaseEstimator
from sklearn.metrics import make_scorer, accuracy_score, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

# Import RL optimizer
from .rl_optimizer import RLOptimizer


class ModelTrainer:
    """
    Train machine learning models with hyperparameter tuning and cross-validation.
    """
    
    def __init__(
        self,
        task_type: str,
        hyperparameter_tuning: str = "auto",
        cross_validation: int = 5,
        verbose: bool = True,
        n_jobs: int = -1,
        random_state: int = 42
    ):
        """
        Initialize the ModelTrainer.
        
        Args:
            task_type: Task type ('classification' or 'regression')
            hyperparameter_tuning: Hyperparameter tuning strategy ('auto', 'grid', 'random', 'bayesian', 'rl', 'none')
            cross_validation: Number of cross-validation folds
            verbose: Whether to print detailed information
            n_jobs: Number of jobs to run in parallel
            random_state: Random seed for reproducibility
        """
        self.task_type = task_type
        self.hyperparameter_tuning = hyperparameter_tuning
        self.cross_validation = cross_validation
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.random_state = random_state
        
        # Initialize training results
        self.training_results = {
            "models": {},
            "best_model": None
        }
        
        # Initialize best model
        self.best_model = None
        self.best_model_name = None
        self.best_score = float('-inf')
        
    def train_models(
        self,
        models: Dict[str, Any],
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        rl_optimizer: Optional[RLOptimizer] = None
    ) -> Dict[str, Any]:
        """
        Train models with hyperparameter tuning and cross-validation.
        
        Args:
            models: Dictionary of models to train
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            rl_optimizer: Optional RL optimizer for hyperparameter tuning
            
        Returns:
            Dictionary of trained models
        """
        # Initialize trained models dictionary
        trained_models = {}
        
        # Initialize training results
        self.training_results = {
            "models": {},
            "best_model": None
        }
        
        # Reset best model
        self.best_model = None
        self.best_model_name = None
        self.best_score = float('-inf') if self.task_type == 'classification' else float('-inf')
        
        # Define scoring metric
        if self.task_type == 'classification':
            scoring = 'accuracy'
        else:
            scoring = 'r2'
            
        # Train each model
        for model_name, model_class in models.items():
            # Initialize training results for this model
            self.training_results["models"][model_name] = {
                "status": "pending",
                "training_time": None,
                "cv_scores": None,
                "validation_score": None,
                "hyperparameters": None
            }
            
            try:
                # Start training timer
                start_time = time.time()
                
                # Get model-specific hyperparameter grid
                param_grid = self._get_model_specific_param_grid(model_class)
                
                # Train model with hyperparameter tuning
                if self.hyperparameter_tuning == 'none':
                    # Train model without hyperparameter tuning
                    model = model_class()
                    model.fit(X_train, y_train)
                    
                    # Evaluate model with cross-validation
                    cv_scores = cross_val_score(
                        model,
                        X_train,
                        y_train,
                        cv=self.cross_validation,
                        scoring=scoring,
                        n_jobs=self.n_jobs
                    )
                    
                    # Evaluate model on validation set
                    if self.task_type == 'classification':
                        val_score = accuracy_score(y_val, model.predict(X_val))
                    else:
                        val_score = r2_score(y_val, model.predict(X_val))
                        
                    # Store results
                    self.training_results["models"][model_name]["hyperparameters"] = model.get_params()
                    
                elif self.hyperparameter_tuning == 'grid':
                    # Train model with grid search
                    grid_search = GridSearchCV(
                        model_class(),
                        param_grid,
                        cv=self.cross_validation,
                        scoring=scoring,
                        n_jobs=self.n_jobs,
                        verbose=0 if not self.verbose else 1
                    )
                    grid_search.fit(X_train, y_train)
                    
                    # Get best model
                    model = grid_search.best_estimator_
                    
                    # Get cross-validation scores
                    cv_scores = grid_search.cv_results_['mean_test_score']
                    
                    # Evaluate model on validation set
                    if self.task_type == 'classification':
                        val_score = accuracy_score(y_val, model.predict(X_val))
                    else:
                        val_score = r2_score(y_val, model.predict(X_val))
                        
                    # Store results
                    self.training_results["models"][model_name]["hyperparameters"] = grid_search.best_params_
                    
                elif self.hyperparameter_tuning == 'random':
                    # Train model with random search
                    random_search = RandomizedSearchCV(
                        model_class(),
                        param_grid,
                        n_iter=10,
                        cv=self.cross_validation,
                        scoring=scoring,
                        n_jobs=self.n_jobs,
                        random_state=self.random_state,
                        verbose=0 if not self.verbose else 1
                    )
                    random_search.fit(X_train, y_train)
                    
                    # Get best model
                    model = random_search.best_estimator_
                    
                    # Get cross-validation scores
                    cv_scores = random_search.cv_results_['mean_test_score']
                    
                    # Evaluate model on validation set
                    if self.task_type == 'classification':
                        val_score = accuracy_score(y_val, model.predict(X_val))
                    else:
                        val_score = r2_score(y_val, model.predict(X_val))
                        
                    # Store results
                    self.training_results["models"][model_name]["hyperparameters"] = random_search.best_params_
                    
                elif self.hyperparameter_tuning == 'rl' or (self.hyperparameter_tuning == 'auto' and rl_optimizer is not None):
                    # Train model with reinforcement learning
                    if rl_optimizer is None:
                        # Create RL optimizer if not provided
                        rl_optimizer = RLOptimizer(
                            task_type=self.task_type,
                            optimization_target="hyperparameters",
                            n_iterations=30,
                            verbose=self.verbose,
                            random_state=self.random_state
                        )
                        
                    # Optimize hyperparameters with RL
                    best_params, model = rl_optimizer.optimize_hyperparameters(
                        model_class=model_class,
                        param_grid=param_grid,
                        X_train=X_train,
                        y_train=y_train,
                        X_val=X_val,
                        y_val=y_val
                    )
                    
                    # Get cross-validation scores
                    cv_scores = cross_val_score(
                        model,
                        X_train,
                        y_train,
                        cv=self.cross_validation,
                        scoring=scoring,
                        n_jobs=self.n_jobs
                    )
                    
                    # Evaluate model on validation set
                    if self.task_type == 'classification':
                        val_score = accuracy_score(y_val, model.predict(X_val))
                    else:
                        val_score = r2_score(y_val, model.predict(X_val))
                        
                    # Store results
                    self.training_results["models"][model_name]["hyperparameters"] = best_params
                    self.training_results["models"][model_name]["rl_optimization"] = rl_optimizer.optimization_results
                    
                else:  # Default to auto
                    # Choose tuning strategy based on dataset size
                    if len(X_train) < 1000:
                        # Use grid search for small datasets
                        grid_search = GridSearchCV(
                            model_class(),
                            param_grid,
                            cv=self.cross_validation,
                            scoring=scoring,
                            n_jobs=self.n_jobs,
                            verbose=0 if not self.verbose else 1
                        )
                        grid_search.fit(X_train, y_train)
                        
                        # Get best model
                        model = grid_search.best_estimator_
                        
                        # Get cross-validation scores
                        cv_scores = grid_search.cv_results_['mean_test_score']
                        
                        # Evaluate model on validation set
                        if self.task_type == 'classification':
                            val_score = accuracy_score(y_val, model.predict(X_val))
                        else:
                            val_score = r2_score(y_val, model.predict(X_val))
                            
                        # Store results
                        self.training_results["models"][model_name]["hyperparameters"] = grid_search.best_params_
                        
                    else:
                        # Use random search for larger datasets
                        random_search = RandomizedSearchCV(
                            model_class(),
                            param_grid,
                            n_iter=10,
                            cv=self.cross_validation,
                            scoring=scoring,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                            verbose=0 if not self.verbose else 1
                        )
                        random_search.fit(X_train, y_train)
                        
                        # Get best model
                        model = random_search.best_estimator_
                        
                        # Get cross-validation scores
                        cv_scores = random_search.cv_results_['mean_test_score']
                        
                        # Evaluate model on validation set
                        if self.task_type == 'classification':
                            val_score = accuracy_score(y_val, model.predict(X_val))
                        else:
                            val_score = r2_score(y_val, model.predict(X_val))
                            
                        # Store results
                        self.training_results["models"][model_name]["hyperparameters"] = random_search.best_params_
                
                # Calculate training time
                training_time = time.time() - start_time
                
                # Store trained model
                trained_models[model_name] = model
                
                # Store training results
                self.training_results["models"][model_name]["status"] = "success"
                self.training_results["models"][model_name]["training_time"] = training_time
                self.training_results["models"][model_name]["cv_scores"] = {
                    "mean": float(np.mean(cv_scores)),
                    "std": float(np.std(cv_scores)),
                    "scores": [float(score) for score in cv_scores]
                }
                self.training_results["models"][model_name]["validation_score"] = float(val_score)
                
                # Update best model if this model is better
                if val_score > self.best_score:
                    self.best_score = val_score
                    self.best_model = model
                    self.best_model_name = model_name
                    
                # Print training results
                if self.verbose:
                    print(f"  • {model_name}: {val_score:.4f} (CV: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f})")
                    
            except Exception as e:
                # Store error
                self.training_results["models"][model_name]["status"] = "error"
                self.training_results["models"][model_name]["error"] = str(e)
                
                # Print error
                if self.verbose:
                    print(f"  • {model_name}: Error - {str(e)}")
                    
        # Store best model
        if self.best_model is not None:
            self.training_results["best_model"] = {
                "name": self.best_model_name,
                "score": float(self.best_score)
            }
            
        return trained_models
    
    def _get_model_specific_param_grid(self, model_class: type) -> Dict[str, List[Any]]:
        """
        Get model-specific hyperparameter grid.
        
        Args:
            model_class: Model class
            
        Returns:
            Model-specific hyperparameter grid
        """
        # Define model-specific parameter grids to prevent parameter leakage
        if model_class == LogisticRegression:
            return {
                'C': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                'penalty': ['l2'],
                'solver': ['lbfgs', 'liblinear'],
                'max_iter': [1000]
            }
        elif model_class == LinearRegression:
            return {
                'fit_intercept': [True, False],
                'normalize': [True, False]
            }
        elif model_class == Ridge:
            return {
                'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                'fit_intercept': [True, False],
                'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
            }
        elif model_class == Lasso:
            return {
                'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                'fit_intercept': [True, False],
                'max_iter': [1000]
            }
        elif model_class == ElasticNet:
            return {
                'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9],
                'fit_intercept': [True, False],
                'max_iter': [1000]
            }
        elif model_class == DecisionTreeClassifier:
            return {
                'criterion': ['gini', 'entropy'],
                'max_depth': [None, 5, 10, 15, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif model_class == DecisionTreeRegressor:
            return {
                'criterion': ['mse', 'friedman_mse', 'mae'],
                'max_depth': [None, 5, 10, 15, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif model_class == RandomForestClassifier:
            return {
                'n_estimators': [50, 100, 200],
                'criterion': ['gini', 'entropy'],
                'max_depth': [None, 5, 10, 15, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif model_class == RandomForestRegressor:
            return {
                'n_estimators': [50, 100, 200],
                'criterion': ['mse', 'mae'],
                'max_depth': [None, 5, 10, 15, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif model_class == GradientBoostingClassifier:
            return {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'subsample': [0.8, 0.9, 1.0]
            }
        elif model_class == GradientBoostingRegressor:
            return {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'subsample': [0.8, 0.9, 1.0],
                'loss': ['ls', 'lad', 'huber', 'quantile']
            }
        elif model_class == SVC:
            return {
                'C': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1.0],
                'probability': [True]
            }
        elif model_class == SVR:
            return {
                'C': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1.0],
                'epsilon': [0.01, 0.1, 0.2]
            }
        elif model_class == KNeighborsClassifier:
            # Strict parameter grid for KNeighborsClassifier to prevent parameter leakage
            return {
                'n_neighbors': [3, 5, 7, 9, 11],
                'weights': ['uniform', 'distance'],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                'p': [1, 2]
            }
        elif model_class == KNeighborsRegressor:
            # Strict parameter grid for KNeighborsRegressor to prevent parameter leakage
            return {
                'n_neighbors': [3, 5, 7, 9, 11],
                'weights': ['uniform', 'distance'],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                'p': [1, 2]
            }
        else:
            # Default empty grid for unknown models
            return {}
    
    def get_training_results(self) -> Dict[str, Any]:
        """
        Get training results.
        
        Returns:
            Dictionary with training results
        """
        return self.training_results
    
    def get_best_model(self) -> Tuple[str, Any]:
        """
        Get best model.
        
        Returns:
            Tuple of (best model name, best model)
        """
        return self.best_model_name, self.best_model
