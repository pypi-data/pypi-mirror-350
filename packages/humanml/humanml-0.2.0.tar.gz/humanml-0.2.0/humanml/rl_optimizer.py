#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reinforcement Learning Module for HumanML.

Provides reinforcement learning capabilities for model optimization,
hyperparameter tuning, and feature selection.
"""

import os
import time
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Optional, Union, Tuple, Set, Callable
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error, accuracy_score


class RLOptimizer:
    """
    Reinforcement Learning Optimizer for model optimization, hyperparameter tuning,
    and feature selection.
    """
    
    def __init__(
        self,
        task_type: str,
        optimization_target: str = "auto",
        n_iterations: int = 50,
        exploration_rate: float = 0.3,
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        verbose: bool = True,
        random_state: int = 42,
        plots_dir: Optional[str] = None,
        callback: Optional[Callable] = None
    ):
        """
        Initialize the RLOptimizer.
        
        Args:
            task_type: Task type ('classification' or 'regression')
            optimization_target: Target to optimize ('hyperparameters', 'features', 'ensemble', 'auto')
            n_iterations: Number of iterations for optimization
            exploration_rate: Exploration rate for epsilon-greedy strategy
            learning_rate: Learning rate for Q-learning
            discount_factor: Discount factor for future rewards
            verbose: Whether to print detailed information
            random_state: Random seed for reproducibility
            plots_dir: Directory to save plots
            callback: Callback function to be called after each iteration
        """
        self.task_type = task_type
        self.optimization_target = optimization_target
        self.n_iterations = n_iterations
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.verbose = verbose
        self.random_state = random_state
        self.plots_dir = plots_dir
        self.callback = callback
        
        # Set random seed
        np.random.seed(self.random_state)
        
        # Initialize optimization results
        self.optimization_results = {}
        
        # Initialize state and action spaces
        self.state_space = None
        self.action_space = None
        
        # Initialize Q-table
        self.q_table = None
        
        # Initialize best configuration
        self.best_config = None
        self.best_score = float('-inf') if self.task_type == 'classification' else float('inf')
        
        # Initialize history
        self.history = {
            'iterations': [],
            'scores': [],
            'configs': [],
            'best_scores': []
        }
        
        # Create plots directory if provided
        if self.plots_dir:
            os.makedirs(self.plots_dir, exist_ok=True)
            
    def optimize_hyperparameters(
        self,
        model_class: type,
        param_grid: Dict[str, List[Any]],
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        scoring_metric: Optional[Callable] = None
    ) -> Tuple[Dict[str, Any], BaseEstimator]:
        """
        Optimize hyperparameters using reinforcement learning.
        
        Args:
            model_class: Model class to optimize
            param_grid: Parameter grid for optimization
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            scoring_metric: Scoring metric for model evaluation
            
        Returns:
            Tuple of (best hyperparameters, best model)
        """
        # Set optimization target
        if self.optimization_target == 'auto':
            self.optimization_target = 'hyperparameters'
            
        # Initialize optimization results
        self.optimization_results = {
            'target': 'hyperparameters',
            'model_class': model_class.__name__,
            'param_grid': param_grid,
            'n_iterations': self.n_iterations,
            'best_params': None,
            'best_score': None,
            'optimization_time': None,
            'history': None
        }
        
        # Validate param_grid against model_class to ensure only valid parameters are used
        valid_param_grid = self._filter_valid_params(model_class, param_grid)
        
        if self.verbose:
            print(f"Optimizing hyperparameters with reinforcement learning...")
            print(f"  • Model: {model_class.__name__}")
            print(f"  • Parameters: {len(valid_param_grid)} parameters with {self._count_combinations(valid_param_grid)} combinations")
            print(f"  • Iterations: {self.n_iterations}")
            
        # Define state and action spaces
        self._define_hyperparameter_spaces(valid_param_grid)
        
        # Initialize Q-table
        self._initialize_q_table()
        
        # Define scoring metric
        if scoring_metric is None:
            if self.task_type == 'classification':
                scoring_metric = accuracy_score
            else:
                scoring_metric = lambda y_true, y_pred: -mean_squared_error(y_true, y_pred)
                
        # Start optimization
        start_time = time.time()
        
        for iteration in range(self.n_iterations):
            # Select action (hyperparameter configuration)
            if np.random.random() < self.exploration_rate:
                # Exploration: random configuration
                config = self._random_hyperparameter_config(valid_param_grid)
            else:
                # Exploitation: best configuration from Q-table
                config = self._best_hyperparameter_config_from_q_table(valid_param_grid)
                
            # Create and train model with selected configuration
            try:
                # Double-check that all parameters in config are valid for this model
                config = {k: v for k, v in config.items() if k in self._get_valid_params(model_class)}
                
                model = model_class(**config)
                model.fit(X_train, y_train)
                
                # Evaluate model
                y_pred = model.predict(X_val)
                score = scoring_metric(y_val, y_pred)
                
                # Update best configuration
                if self._is_better_score(score):
                    self.best_config = config.copy()
                    self.best_score = score
                    self.best_model = model
                    
                # Update Q-table
                self._update_q_table(config, score)
                
                # Update history
                self.history['iterations'].append(iteration)
                self.history['scores'].append(score)
                self.history['configs'].append(config.copy())
                self.history['best_scores'].append(self.best_score)
                
                # Print progress
                if self.verbose and (iteration + 1) % 5 == 0:
                    print(f"  • Iteration {iteration + 1}/{self.n_iterations}: Score = {score:.4f}, Best = {self.best_score:.4f}")
                    
                # Call callback if provided
                if self.callback:
                    self.callback(iteration, config, score, self.best_config, self.best_score)
            except Exception as e:
                # Log error but continue with next iteration
                if self.verbose:
                    print(f"  • Iteration {iteration + 1}/{self.n_iterations}: Error - {str(e)}")
                
        # Calculate optimization time
        optimization_time = time.time() - start_time
        
        # Store optimization results
        self.optimization_results['best_params'] = self.best_config
        self.optimization_results['best_score'] = self.best_score
        self.optimization_results['optimization_time'] = optimization_time
        self.optimization_results['history'] = {
            'iterations': self.history['iterations'],
            'scores': self.history['scores'],
            'best_scores': self.history['best_scores']
        }
        
        # Generate optimization plot
        if self.plots_dir:
            self._plot_optimization_history()
            
        if self.verbose:
            print(f"Hyperparameter optimization completed in {optimization_time:.2f} seconds")
            print(f"  • Best score: {self.best_score:.4f}")
            print(f"  • Best parameters: {self.best_config}")
            
        # Train final model with best configuration
        final_model = model_class(**self.best_config)
        final_model.fit(X_train, y_train)
            
        return self.best_config, final_model
    
    def _get_valid_params(self, model_class: type) -> Set[str]:
        """
        Get valid parameters for a model class.
        
        Args:
            model_class: Model class
            
        Returns:
            Set of valid parameter names
        """
        # Get valid parameters for the model class
        valid_params = set(inspect.signature(model_class.__init__).parameters.keys())
        # Remove 'self' from valid parameters
        valid_params.discard('self')
        
        return valid_params
    
    def _filter_valid_params(self, model_class: type, param_grid: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """
        Filter parameter grid to include only valid parameters for the model class.
        
        Args:
            model_class: Model class
            param_grid: Parameter grid
            
        Returns:
            Filtered parameter grid
        """
        # Get valid parameters for the model class
        valid_params = self._get_valid_params(model_class)
        
        # Filter parameter grid
        filtered_grid = {}
        for param, values in param_grid.items():
            if param in valid_params:
                filtered_grid[param] = values
            
        return filtered_grid
    
    def optimize_feature_selection(
        self,
        model: BaseEstimator,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        scoring_metric: Optional[Callable] = None,
        min_features: int = 1
    ) -> Tuple[List[str], BaseEstimator]:
        """
        Optimize feature selection using reinforcement learning.
        
        Args:
            model: Model to optimize
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            scoring_metric: Scoring metric for model evaluation
            min_features: Minimum number of features to select
            
        Returns:
            Tuple of (best features, best model)
        """
        # Set optimization target
        if self.optimization_target == 'auto':
            self.optimization_target = 'features'
            
        # Initialize optimization results
        self.optimization_results = {
            'target': 'features',
            'model_class': model.__class__.__name__,
            'n_features': X_train.shape[1],
            'feature_names': X_train.columns.tolist(),
            'n_iterations': self.n_iterations,
            'best_features': None,
            'best_score': None,
            'optimization_time': None,
            'history': None
        }
        
        if self.verbose:
            print(f"Optimizing feature selection with reinforcement learning...")
            print(f"  • Model: {model.__class__.__name__}")
            print(f"  • Features: {X_train.shape[1]} features")
            print(f"  • Iterations: {self.n_iterations}")
            
        # Define state and action spaces
        self._define_feature_spaces(X_train.columns)
        
        # Initialize Q-table
        self._initialize_q_table()
        
        # Define scoring metric
        if scoring_metric is None:
            if self.task_type == 'classification':
                scoring_metric = accuracy_score
            else:
                scoring_metric = lambda y_true, y_pred: -mean_squared_error(y_true, y_pred)
                
        # Start optimization
        start_time = time.time()
        
        for iteration in range(self.n_iterations):
            # Select action (feature subset)
            if np.random.random() < self.exploration_rate:
                # Exploration: random feature subset
                feature_mask = self._random_feature_mask(X_train.shape[1], min_features)
            else:
                # Exploitation: best feature subset from Q-table
                feature_mask = self._best_feature_mask_from_q_table(X_train.shape[1], min_features)
                
            # Get selected features
            selected_features = X_train.columns[feature_mask].tolist()
            
            # Train model with selected features
            model_copy = self._clone_model(model)
            model_copy.fit(X_train[selected_features], y_train)
            
            # Evaluate model
            y_pred = model_copy.predict(X_val[selected_features])
            score = scoring_metric(y_val, y_pred)
            
            # Update best configuration
            if self._is_better_score(score):
                self.best_config = feature_mask.copy()
                self.best_score = score
                self.best_model = model_copy
                self.best_features = selected_features
                
            # Update Q-table
            self._update_feature_q_table(feature_mask, score)
            
            # Update history
            self.history['iterations'].append(iteration)
            self.history['scores'].append(score)
            self.history['configs'].append(feature_mask.copy())
            self.history['best_scores'].append(self.best_score)
            
            # Print progress
            if self.verbose and (iteration + 1) % 5 == 0:
                print(f"  • Iteration {iteration + 1}/{self.n_iterations}: Score = {score:.4f}, Best = {self.best_score:.4f}")
                print(f"    Selected {len(selected_features)}/{X_train.shape[1]} features")
                
            # Call callback if provided
            if self.callback:
                self.callback(iteration, selected_features, score, self.best_features, self.best_score)
                
        # Calculate optimization time
        optimization_time = time.time() - start_time
        
        # Store optimization results
        self.optimization_results['best_features'] = self.best_features
        self.optimization_results['n_selected_features'] = len(self.best_features)
        self.optimization_results['best_score'] = self.best_score
        self.optimization_results['optimization_time'] = optimization_time
        self.optimization_results['history'] = {
            'iterations': self.history['iterations'],
            'scores': self.history['scores'],
            'best_scores': self.history['best_scores']
        }
        
        # Generate optimization plot
        if self.plots_dir:
            self._plot_optimization_history()
            
        if self.verbose:
            print(f"Feature selection optimization completed in {optimization_time:.2f} seconds")
            print(f"  • Best score: {self.best_score:.4f}")
            print(f"  • Selected {len(self.best_features)}/{X_train.shape[1]} features")
            if len(self.best_features) <= 10:
                print(f"  • Selected features: {self.best_features}")
            else:
                print(f"  • Top 10 selected features: {self.best_features[:10]}")
            
        # Train final model with best features
        final_model = self._clone_model(model)
        final_model.fit(X_train[self.best_features], y_train)
            
        return self.best_features, final_model
    
    def optimize_ensemble(
        self,
        models: Dict[str, BaseEstimator],
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        scoring_metric: Optional[Callable] = None
    ) -> Tuple[Dict[str, float], Any]:
        """
        Optimize ensemble weights using reinforcement learning.
        
        Args:
            models: Dictionary of trained models
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            scoring_metric: Scoring metric for model evaluation
            
        Returns:
            Tuple of (best weights, best ensemble model)
        """
        # Set optimization target
        if self.optimization_target == 'auto':
            self.optimization_target = 'ensemble'
            
        # Initialize optimization results
        self.optimization_results = {
            'target': 'ensemble',
            'models': list(models.keys()),
            'n_models': len(models),
            'n_iterations': self.n_iterations,
            'best_weights': None,
            'best_score': None,
            'optimization_time': None,
            'history': None
        }
        
        if self.verbose:
            print(f"Optimizing ensemble weights with reinforcement learning...")
            print(f"  • Models: {len(models)} models")
            print(f"  • Iterations: {self.n_iterations}")
            
        # Define state and action spaces
        self._define_ensemble_spaces(models)
        
        # Initialize Q-table
        self._initialize_q_table()
        
        # Define scoring metric
        if scoring_metric is None:
            if self.task_type == 'classification':
                scoring_metric = accuracy_score
            else:
                scoring_metric = lambda y_true, y_pred: -mean_squared_error(y_true, y_pred)
                
        # Start optimization
        start_time = time.time()
        
        for iteration in range(self.n_iterations):
            # Select action (ensemble weights)
            if np.random.random() < self.exploration_rate:
                # Exploration: random weights
                weights = self._random_ensemble_weights(models)
            else:
                # Exploitation: best weights from Q-table
                weights = self._best_ensemble_weights_from_q_table(models)
                
            # Make ensemble predictions
            if self.task_type == 'classification':
                # For classification, use weighted voting
                predictions = {}
                for model_name, model in models.items():
                    if weights[model_name] > 0:
                        # Get class probabilities
                        if hasattr(model, 'predict_proba'):
                            proba = model.predict_proba(X_val)
                            for i, class_idx in enumerate(model.classes_):
                                if class_idx not in predictions:
                                    predictions[class_idx] = np.zeros(len(X_val))
                                predictions[class_idx] += weights[model_name] * proba[:, i]
                        else:
                            # If model doesn't support probabilities, use hard predictions
                            preds = model.predict(X_val)
                            for i, pred in enumerate(preds):
                                if pred not in predictions:
                                    predictions[pred] = np.zeros(len(X_val))
                                predictions[pred][i] += weights[model_name]
                                
                # Get final predictions
                y_pred = np.zeros(len(X_val))
                for i in range(len(X_val)):
                    best_class = None
                    best_score = -float('inf')
                    for class_idx, scores in predictions.items():
                        if scores[i] > best_score:
                            best_score = scores[i]
                            best_class = class_idx
                    y_pred[i] = best_class
            else:
                # For regression, use weighted average
                y_pred = np.zeros(len(X_val))
                weight_sum = sum(weights.values())
                for model_name, model in models.items():
                    if weights[model_name] > 0:
                        y_pred += weights[model_name] * model.predict(X_val)
                if weight_sum > 0:
                    y_pred /= weight_sum
                    
            # Evaluate ensemble
            score = scoring_metric(y_val, y_pred)
            
            # Update best configuration
            if self._is_better_score(score):
                self.best_config = weights.copy()
                self.best_score = score
                
            # Update Q-table
            self._update_ensemble_q_table(weights, score)
            
            # Update history
            self.history['iterations'].append(iteration)
            self.history['scores'].append(score)
            self.history['configs'].append(weights.copy())
            self.history['best_scores'].append(self.best_score)
            
            # Print progress
            if self.verbose and (iteration + 1) % 5 == 0:
                print(f"  • Iteration {iteration + 1}/{self.n_iterations}: Score = {score:.4f}, Best = {self.best_score:.4f}")
                
            # Call callback if provided
            if self.callback:
                self.callback(iteration, weights, score, self.best_config, self.best_score)
                
        # Calculate optimization time
        optimization_time = time.time() - start_time
        
        # Store optimization results
        self.optimization_results['best_weights'] = self.best_config
        self.optimization_results['best_score'] = self.best_score
        self.optimization_results['optimization_time'] = optimization_time
        self.optimization_results['history'] = {
            'iterations': self.history['iterations'],
            'scores': self.history['scores'],
            'best_scores': self.history['best_scores']
        }
        
        # Generate optimization plot
        if self.plots_dir:
            self._plot_optimization_history()
            
        if self.verbose:
            print(f"Ensemble optimization completed in {optimization_time:.2f} seconds")
            print(f"  • Best score: {self.best_score:.4f}")
            print(f"  • Best weights: {self.best_config}")
            
        # Create ensemble model
        ensemble_model = EnsembleModel(
            models=models,
            weights=self.best_config,
            task_type=self.task_type
        )
            
        return self.best_config, ensemble_model
    
    def _define_hyperparameter_spaces(self, param_grid: Dict[str, List[Any]]) -> None:
        """
        Define state and action spaces for hyperparameter optimization.
        
        Args:
            param_grid: Parameter grid
        """
        # Define state space
        self.state_space = {
            'param_grid': param_grid,
            'n_params': len(param_grid),
            'param_names': list(param_grid.keys()),
            'param_values': list(param_grid.values())
        }
        
        # Define action space
        self.action_space = {
            'n_actions': self._count_combinations(param_grid),
            'actions': self._generate_all_combinations(param_grid)
        }
        
    def _define_feature_spaces(self, feature_names: List[str]) -> None:
        """
        Define state and action spaces for feature selection.
        
        Args:
            feature_names: List of feature names
        """
        # Define state space
        self.state_space = {
            'n_features': len(feature_names),
            'feature_names': feature_names
        }
        
        # Define action space
        self.action_space = {
            'n_actions': 2 ** len(feature_names),
            'actions': None  # Too many to enumerate
        }
        
    def _define_ensemble_spaces(self, models: Dict[str, BaseEstimator]) -> None:
        """
        Define state and action spaces for ensemble optimization.
        
        Args:
            models: Dictionary of models
        """
        # Define state space
        self.state_space = {
            'n_models': len(models),
            'model_names': list(models.keys())
        }
        
        # Define action space
        self.action_space = {
            'n_actions': 11 ** len(models),  # 0.0, 0.1, 0.2, ..., 1.0 for each model
            'actions': None  # Too many to enumerate
        }
        
    def _initialize_q_table(self) -> None:
        """
        Initialize Q-table.
        """
        if self.optimization_target == 'hyperparameters':
            # Initialize Q-table for hyperparameter optimization
            self.q_table = {}
            for action in self.action_space['actions']:
                action_key = self._action_to_key(action)
                self.q_table[action_key] = 0.0
        elif self.optimization_target == 'features':
            # Initialize Q-table for feature selection
            self.q_table = {}
        elif self.optimization_target == 'ensemble':
            # Initialize Q-table for ensemble optimization
            self.q_table = {}
            
    def _action_to_key(self, action: Dict[str, Any]) -> str:
        """
        Convert action to key for Q-table.
        
        Args:
            action: Action
            
        Returns:
            Key for Q-table
        """
        return str(action)
    
    def _random_hyperparameter_config(self, param_grid: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Generate random hyperparameter configuration.
        
        Args:
            param_grid: Parameter grid
            
        Returns:
            Random hyperparameter configuration
        """
        config = {}
        for param, values in param_grid.items():
            config[param] = np.random.choice(values)
        return config
    
    def _best_hyperparameter_config_from_q_table(self, param_grid: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Get best hyperparameter configuration from Q-table.
        
        Args:
            param_grid: Parameter grid
            
        Returns:
            Best hyperparameter configuration
        """
        if not self.q_table:
            return self._random_hyperparameter_config(param_grid)
            
        best_action = None
        best_q_value = float('-inf')
        
        for action_key, q_value in self.q_table.items():
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = eval(action_key)
                
        if best_action is None:
            return self._random_hyperparameter_config(param_grid)
            
        return best_action
    
    def _random_feature_mask(self, n_features: int, min_features: int) -> np.ndarray:
        """
        Generate random feature mask.
        
        Args:
            n_features: Number of features
            min_features: Minimum number of features to select
            
        Returns:
            Random feature mask
        """
        # Generate random mask
        mask = np.zeros(n_features, dtype=bool)
        
        # Ensure at least min_features are selected
        indices = np.random.choice(n_features, size=min_features, replace=False)
        mask[indices] = True
        
        # Randomly select additional features
        for i in range(n_features):
            if not mask[i] and np.random.random() < 0.5:
                mask[i] = True
                
        return mask
    
    def _best_feature_mask_from_q_table(self, n_features: int, min_features: int) -> np.ndarray:
        """
        Get best feature mask from Q-table.
        
        Args:
            n_features: Number of features
            min_features: Minimum number of features to select
            
        Returns:
            Best feature mask
        """
        if not self.q_table:
            return self._random_feature_mask(n_features, min_features)
            
        best_mask = None
        best_q_value = float('-inf')
        
        for mask_key, q_value in self.q_table.items():
            if q_value > best_q_value:
                best_q_value = q_value
                best_mask = np.array(eval(mask_key), dtype=bool)
                
        if best_mask is None or np.sum(best_mask) < min_features:
            return self._random_feature_mask(n_features, min_features)
            
        return best_mask
    
    def _random_ensemble_weights(self, models: Dict[str, BaseEstimator]) -> Dict[str, float]:
        """
        Generate random ensemble weights.
        
        Args:
            models: Dictionary of models
            
        Returns:
            Random ensemble weights
        """
        weights = {}
        for model_name in models.keys():
            weights[model_name] = np.random.choice(np.linspace(0, 1, 11))
            
        # Normalize weights
        weight_sum = sum(weights.values())
        if weight_sum > 0:
            for model_name in weights:
                weights[model_name] /= weight_sum
                
        return weights
    
    def _best_ensemble_weights_from_q_table(self, models: Dict[str, BaseEstimator]) -> Dict[str, float]:
        """
        Get best ensemble weights from Q-table.
        
        Args:
            models: Dictionary of models
            
        Returns:
            Best ensemble weights
        """
        if not self.q_table:
            return self._random_ensemble_weights(models)
            
        best_weights = None
        best_q_value = float('-inf')
        
        for weights_key, q_value in self.q_table.items():
            if q_value > best_q_value:
                best_q_value = q_value
                best_weights = eval(weights_key)
                
        if best_weights is None:
            return self._random_ensemble_weights(models)
            
        return best_weights
    
    def _update_q_table(self, config: Dict[str, Any], score: float) -> None:
        """
        Update Q-table for hyperparameter optimization.
        
        Args:
            config: Hyperparameter configuration
            score: Score
        """
        action_key = self._action_to_key(config)
        
        # Initialize Q-value if not exists
        if action_key not in self.q_table:
            self.q_table[action_key] = 0.0
            
        # Update Q-value
        old_q_value = self.q_table[action_key]
        self.q_table[action_key] = old_q_value + self.learning_rate * (score - old_q_value)
        
    def _update_feature_q_table(self, feature_mask: np.ndarray, score: float) -> None:
        """
        Update Q-table for feature selection.
        
        Args:
            feature_mask: Feature mask
            score: Score
        """
        mask_key = str(feature_mask.tolist())
        
        # Initialize Q-value if not exists
        if mask_key not in self.q_table:
            self.q_table[mask_key] = 0.0
            
        # Update Q-value
        old_q_value = self.q_table[mask_key]
        self.q_table[mask_key] = old_q_value + self.learning_rate * (score - old_q_value)
        
    def _update_ensemble_q_table(self, weights: Dict[str, float], score: float) -> None:
        """
        Update Q-table for ensemble optimization.
        
        Args:
            weights: Ensemble weights
            score: Score
        """
        weights_key = str(weights)
        
        # Initialize Q-value if not exists
        if weights_key not in self.q_table:
            self.q_table[weights_key] = 0.0
            
        # Update Q-value
        old_q_value = self.q_table[weights_key]
        self.q_table[weights_key] = old_q_value + self.learning_rate * (score - old_q_value)
        
    def _is_better_score(self, score: float) -> bool:
        """
        Check if score is better than current best score.
        
        Args:
            score: Score
            
        Returns:
            Whether score is better
        """
        if self.task_type == 'classification':
            return score > self.best_score
        else:
            return score < self.best_score
        
    def _count_combinations(self, param_grid: Dict[str, List[Any]]) -> int:
        """
        Count number of hyperparameter combinations.
        
        Args:
            param_grid: Parameter grid
            
        Returns:
            Number of combinations
        """
        n_combinations = 1
        for values in param_grid.values():
            n_combinations *= len(values)
        return n_combinations
    
    def _generate_all_combinations(self, param_grid: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """
        Generate all hyperparameter combinations.
        
        Args:
            param_grid: Parameter grid
            
        Returns:
            List of all combinations
        """
        # If too many combinations, return None
        if self._count_combinations(param_grid) > 10000:
            return None
            
        # Generate all combinations
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        combinations = []
        
        def generate_combinations(index, current_config):
            if index == len(param_names):
                combinations.append(current_config.copy())
                return
                
            for value in param_values[index]:
                current_config[param_names[index]] = value
                generate_combinations(index + 1, current_config)
                
        generate_combinations(0, {})
        return combinations
    
    def _clone_model(self, model: BaseEstimator) -> BaseEstimator:
        """
        Clone model.
        
        Args:
            model: Model to clone
            
        Returns:
            Cloned model
        """
        from sklearn.base import clone
        return clone(model)
    
    def _plot_optimization_history(self) -> None:
        """
        Plot optimization history.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.history['iterations'], self.history['scores'], 'b-', alpha=0.5, label='Score')
        plt.plot(self.history['iterations'], self.history['best_scores'], 'r-', label='Best Score')
        plt.xlabel('Iteration')
        plt.ylabel('Score')
        plt.title('Optimization History')
        plt.legend()
        plt.grid(True)
        
        # Save plot
        if self.plots_dir:
            plt.savefig(os.path.join(self.plots_dir, f"{self.optimization_target}_optimization_history.png"))
            plt.close()
            
    def get_optimization_results(self) -> Dict[str, Any]:
        """
        Get optimization results.
        
        Returns:
            Dictionary with optimization results
        """
        return self.optimization_results


class EnsembleModel:
    """
    Ensemble model for combining multiple models.
    """
    
    def __init__(
        self,
        models: Dict[str, BaseEstimator],
        weights: Dict[str, float],
        task_type: str
    ):
        """
        Initialize the EnsembleModel.
        
        Args:
            models: Dictionary of models
            weights: Dictionary of model weights
            task_type: Task type ('classification' or 'regression')
        """
        self.models = models
        self.weights = weights
        self.task_type = task_type
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        if self.task_type == 'classification':
            # For classification, use weighted voting
            predictions = {}
            for model_name, model in self.models.items():
                if self.weights[model_name] > 0:
                    # Get class probabilities
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba(X)
                        for i, class_idx in enumerate(model.classes_):
                            if class_idx not in predictions:
                                predictions[class_idx] = np.zeros(len(X))
                            predictions[class_idx] += self.weights[model_name] * proba[:, i]
                    else:
                        # If model doesn't support probabilities, use hard predictions
                        preds = model.predict(X)
                        for i, pred in enumerate(preds):
                            if pred not in predictions:
                                predictions[pred] = np.zeros(len(X))
                            predictions[pred][i] += self.weights[model_name]
                            
            # Get final predictions
            y_pred = np.zeros(len(X))
            for i in range(len(X)):
                best_class = None
                best_score = -float('inf')
                for class_idx, scores in predictions.items():
                    if scores[i] > best_score:
                        best_score = scores[i]
                        best_class = class_idx
                y_pred[i] = best_class
        else:
            # For regression, use weighted average
            y_pred = np.zeros(len(X))
            weight_sum = sum(self.weights.values())
            for model_name, model in self.models.items():
                if self.weights[model_name] > 0:
                    y_pred += self.weights[model_name] * model.predict(X)
            if weight_sum > 0:
                y_pred /= weight_sum
                
        return y_pred
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make probability predictions.
        
        Args:
            X: Features
            
        Returns:
            Probability predictions
        """
        if self.task_type != 'classification':
            raise ValueError("Probability predictions are only available for classification tasks.")
            
        # Get all classes
        all_classes = set()
        for model_name, model in self.models.items():
            if hasattr(model, 'classes_'):
                all_classes.update(model.classes_)
        all_classes = sorted(list(all_classes))
        
        # Initialize probabilities
        probas = np.zeros((len(X), len(all_classes)))
        
        # Compute weighted probabilities
        weight_sum = 0
        for model_name, model in self.models.items():
            if self.weights[model_name] > 0 and hasattr(model, 'predict_proba'):
                weight_sum += self.weights[model_name]
                model_proba = model.predict_proba(X)
                for i, class_idx in enumerate(model.classes_):
                    class_pos = all_classes.index(class_idx)
                    probas[:, class_pos] += self.weights[model_name] * model_proba[:, i]
                    
        # Normalize probabilities
        if weight_sum > 0:
            probas /= weight_sum
            
        return probas
    
    def score(self, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Score model.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Score
        """
        y_pred = self.predict(X)
        
        if self.task_type == 'classification':
            return accuracy_score(y, y_pred)
        else:
            return -mean_squared_error(y, y_pred)
