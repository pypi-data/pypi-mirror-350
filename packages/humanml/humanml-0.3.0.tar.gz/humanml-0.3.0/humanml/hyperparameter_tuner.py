#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hyperparameter Tuner Module for HumanML.

Provides functionality for tuning model hyperparameters using various strategies
such as grid search, random search, and Bayesian optimization.
"""

import time
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


class HyperparameterTuner:
    """
    Tune model hyperparameters using various strategies such as grid search,
    random search, and Bayesian optimization.
    """
    
    def __init__(
        self,
        strategy: str = "auto",
        scoring: Optional[str] = None,
        cv: int = 5,
        verbose: bool = True,
        n_jobs: int = -1,
        random_state: int = 42
    ):
        """
        Initialize the HyperparameterTuner.
        
        Args:
            strategy: Tuning strategy ('auto', 'grid', 'random', 'bayesian', 'none')
            scoring: Scoring metric for model evaluation
            cv: Number of cross-validation folds
            verbose: Whether to print detailed information
            n_jobs: Number of jobs to run in parallel
            random_state: Random seed for reproducibility
        """
        self.strategy = strategy
        self.scoring = scoring
        self.cv = cv
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.random_state = random_state
        
        # Initialize tuning results
        self.tuning_results = {}
        
    def tune_hyperparameters(
        self,
        model: BaseEstimator,
        param_grid: Dict[str, List[Any]],
        X: pd.DataFrame,
        y: pd.Series,
        n_iter: int = 10
    ) -> BaseEstimator:
        """
        Tune hyperparameters for a model.
        
        Args:
            model: Model to tune
            param_grid: Parameter grid for tuning
            X: Features
            y: Target
            n_iter: Number of iterations for random and Bayesian search
            
        Returns:
            Tuned model
        """
        # Initialize tuning results
        self.tuning_results = {
            "strategy": self.strategy,
            "scoring": self.scoring,
            "cv": self.cv,
            "param_grid": param_grid,
            "best_params": {},
            "best_score": None,
            "tuning_time": None
        }
        
        # Determine tuning strategy
        strategy = self._determine_strategy(X.shape[0])
        
        if self.verbose:
            print(f"Tuning hyperparameters with {strategy} strategy...")
            
        # Tune hyperparameters based on strategy
        start_time = time.time()
        
        if strategy == "none":
            # No tuning, just return the model
            tuned_model = model
            best_params = {}
            best_score = None
        elif strategy == "grid":
            # Grid search
            grid_search = GridSearchCV(
                model, param_grid,
                scoring=self.scoring,
                cv=self.cv,
                n_jobs=self.n_jobs,
                verbose=1 if self.verbose else 0
            )
            grid_search.fit(X, y)
            tuned_model = grid_search.best_estimator_
            best_params = grid_search.best_params_
            best_score = grid_search.best_score_
        elif strategy == "random":
            # Random search
            random_search = RandomizedSearchCV(
                model, param_grid,
                n_iter=n_iter,
                scoring=self.scoring,
                cv=self.cv,
                n_jobs=self.n_jobs,
                random_state=self.random_state,
                verbose=1 if self.verbose else 0
            )
            random_search.fit(X, y)
            tuned_model = random_search.best_estimator_
            best_params = random_search.best_params_
            best_score = random_search.best_score_
        elif strategy == "bayesian":
            # Bayesian optimization
            try:
                from skopt import BayesSearchCV
                bayes_search = BayesSearchCV(
                    model, param_grid,
                    n_iter=n_iter,
                    scoring=self.scoring,
                    cv=self.cv,
                    n_jobs=self.n_jobs,
                    random_state=self.random_state,
                    verbose=1 if self.verbose else 0
                )
                bayes_search.fit(X, y)
                tuned_model = bayes_search.best_estimator_
                best_params = bayes_search.best_params_
                best_score = bayes_search.best_score_
            except ImportError:
                if self.verbose:
                    print("  • Warning: skopt not available, falling back to random search")
                # Fall back to random search
                random_search = RandomizedSearchCV(
                    model, param_grid,
                    n_iter=n_iter,
                    scoring=self.scoring,
                    cv=self.cv,
                    n_jobs=self.n_jobs,
                    random_state=self.random_state,
                    verbose=1 if self.verbose else 0
                )
                random_search.fit(X, y)
                tuned_model = random_search.best_estimator_
                best_params = random_search.best_params_
                best_score = random_search.best_score_
        else:
            raise ValueError(f"Invalid tuning strategy: {strategy}")
            
        # Calculate tuning time
        tuning_time = time.time() - start_time
        
        # Store tuning results
        self.tuning_results["strategy"] = strategy
        self.tuning_results["best_params"] = best_params
        self.tuning_results["best_score"] = best_score
        self.tuning_results["tuning_time"] = tuning_time
        
        if self.verbose:
            print(f"  • Tuning completed in {tuning_time:.2f} seconds")
            if best_score is not None:
                print(f"  • Best score: {best_score:.4f}")
            print(f"  • Best parameters: {best_params}")
            
        return tuned_model
    
    def _determine_strategy(self, n_samples: int) -> str:
        """
        Determine tuning strategy based on dataset size and user preference.
        
        Args:
            n_samples: Number of samples in the dataset
            
        Returns:
            Tuning strategy
        """
        if self.strategy != "auto":
            return self.strategy
            
        # Determine strategy based on dataset size
        if n_samples < 1000:
            return "random"
        elif n_samples < 10000:
            return "random"
        else:
            return "bayesian"
    
    def get_tuning_results(self) -> Dict[str, Any]:
        """
        Get tuning results.
        
        Returns:
            Dictionary with tuning results
        """
        return self.tuning_results


# Example Usage (for testing purposes)
if __name__ == "__main__":
    print("Running HyperparameterTuner Example...")
    
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
    
    # Create model
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(random_state=42)
    
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # Initialize hyperparameter tuner
    tuner = HyperparameterTuner(
        strategy="random",
        scoring="accuracy",
        cv=3,
        verbose=True
    )
    
    # Tune hyperparameters
    tuned_model = tuner.tune_hyperparameters(
        model=model,
        param_grid=param_grid,
        X=X,
        y=y,
        n_iter=5
    )
    
    # Get tuning results
    results = tuner.get_tuning_results()
    
    print("\nTuning Results:")
    print(f"Strategy: {results['strategy']}")
    print(f"Best score: {results['best_score']:.4f}")
    print(f"Tuning time: {results['tuning_time']:.2f} seconds")
    print("Best parameters:")
    for param, value in results['best_params'].items():
        print(f"  • {param}: {value}")
    
    print("\nHyperparameterTuner example completed successfully!")
