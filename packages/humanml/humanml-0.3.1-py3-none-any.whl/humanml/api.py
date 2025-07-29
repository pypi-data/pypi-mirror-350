#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API Module for HumanML.

Provides the main HumanML class for machine learning workflow automation.
"""

import os
import time
import json
import pickle
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Optional, Union, Tuple, Set, Callable
from sklearn.base import BaseEstimator

from .data_preprocessor import DataPreprocessor
from .data_splitter import DataSplitter
from .model_selector import ModelSelector
from .model_trainer import ModelTrainer
from .model_evaluator import ModelEvaluator
from .model_explainer import ModelExplainer
from .model_exporter import ModelExporter
from .auto_logger import AutoLogger
from .report_generator import ReportGenerator
from .plot_utilities import PlotUtilities


class HumanML:
    """
    HumanML - A Human-Centered Machine Learning Library.
    
    Provides a comprehensive machine learning workflow with a focus on
    human-centered design, adaptivity, and professional outputs.
    """
    
    def __init__(
        self,
        task_type: str = "auto",
        output_dir: str = "output",
        test_size: float = 0.2,
        validation_size: float = 0.2,
        random_state: int = 42,
        n_jobs: int = -1,
        verbose: bool = False,
        models: Optional[List[str]] = None,
        hyperparameter_tuning: str = "auto",
        cross_validation: int = 5,
        callbacks: Optional[Dict[str, Callable]] = None,
        preference: str = "" # Added preference argument
    ):
        """
        Initialize the HumanML instance.
        
        Args:
            task_type: Task type ('classification', 'regression', or 'auto')
            output_dir: Directory to save outputs
            test_size: Test set size
            validation_size: Validation set size
            random_state: Random seed
            n_jobs: Number of jobs for parallel processing
            verbose: Whether to print detailed information
            models: List of models to include (None for all)
            hyperparameter_tuning: Hyperparameter tuning method ('grid', 'random', 'bayesian', 'rl', or 'auto')
            cross_validation: Number of cross-validation folds
            callbacks: Dictionary of callback functions
            preference: User preference string (used for specific configurations)
        """
        self.task_type = task_type
        self.output_dir = output_dir
        self.test_size = test_size
        self.validation_size = validation_size
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.models = models
        self.hyperparameter_tuning = hyperparameter_tuning
        self.cross_validation = cross_validation
        self.callbacks = callbacks if callbacks is not None else {}
        self.preference = preference # Store preference
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create plots directory
        self.plots_dir = os.path.join(self.output_dir, "plots")
        os.makedirs(self.plots_dir, exist_ok=True)
        
        # Create models directory
        self.models_dir = os.path.join(self.output_dir, "models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Create logs directory
        self.logs_dir = os.path.join(self.output_dir, "logs")
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Initialize session ID
        self.session_id = f"humanml_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # Initialize logger
        self.logger = AutoLogger(
            session_id=self.session_id,
            logs_dir=self.logs_dir,
            verbose=self.verbose
        )
        
        # Initialize results
        self.results = {
            "session_id": self.session_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "library_version": "0.3.0",
            "task_type": self.task_type,
            "data": {
                "original": {},
                "split": {}
            },
            "preprocessing": {},
            "models": {
                "selection": {},
                "trained": {},
                "best": {}
            },
            "evaluation": {},
            "explanation": {},
            "export": {}
        }
        
        # Initialize best model
        self.best_model = None
        self.best_model_name = None
        
        self.plot_utils = PlotUtilities(plots_dir=self.plots_dir)
        
        # Initialize components
        self.preprocessor = None
        self.data_splitter = None
        self.model_selector = None
        self.model_trainer = None
        self.model_evaluator = None
        self.model_explainer = None
        self.model_exporter = None
        self.report_generator = None
        
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'HumanML':
        """
        Fit the HumanML pipeline to the data.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Self
        """
        try:
            # Start timer
            start_time = time.time()
            
            # Determine task type if auto
            if self.task_type == "auto":
                self._determine_task_type(y)
                
            # Analyze data
            self._analyze_data_and_print_header(X, y)
            
            # Step 1: Data preprocessing and feature engineering
            print("Step 1: Data preprocessing and feature engineering (1/5)")
            print("--------------------------------------------------------")
            self._analyze_data(X, y)
            X_processed = self._preprocess_data(X, y)
            split_data = self._split_data(X_processed, y)
            
            # Step 2: Model selection and hyperparameter tuning
            print("Step 2: Model selection and hyperparameter tuning (2/5)")
            print("-------------------------------------------------------")
            self.logger.log_step_start("model_selection")
            selected_models = self._select_models(split_data["X_train"], split_data["y_train"])
            self.logger.log_step_end("model_selection")
            
            # Step 3: Model training and evaluation
            print("Step 3: Model training and evaluation (3/5)")
            print("-------------------------------------------")
            self.logger.log_step_start("model_training")
            trained_models = self.model_trainer.train_models(
                selected_models,
                split_data["X_train"],
                split_data["y_train"],
                split_data["X_val"],
                split_data["y_val"]
            )
            
            # Store training results
            self.results["models"]["trained"] = self.model_trainer.get_training_results()
            
            # Evaluate models
            evaluation_results = self._evaluate_models(trained_models, split_data)
            
            # Select best model
            self.best_model_name, self.best_model = self._select_best_model(trained_models, evaluation_results)
            
            # Store best model in results
            self.results["models"]["best"] = {
                "name": self.best_model_name,
                "model_type": type(self.best_model).__name__,
                "metrics": evaluation_results["models"][self.best_model_name]["metrics"] if self.best_model_name in evaluation_results["models"] else {}
            }
            
            self.logger.log_step_end("model_training")
            
            # Step 4: Model explanation and visualization
            print("Step 4: Model explanation and visualization (4/5)")
            print("------------------------------------------------")
            self.logger.log_step_start("model_explanation")
            explanation_results = self._explain_model(self.best_model, self.best_model_name, split_data)
            self.logger.log_step_end("model_explanation")
            
            # Step 5: Report generation and model export
            print("Step 5: Report generation and model export (5/5)")
            print("-----------------------------------------------")
            self.logger.log_step_start("report_generation")
            
            # # Export best model (moved to export_model method)
            # model_path = self._export_model(self.best_model, self.best_model_name)

            # # Generate report (moved to generate_report method)
            # report_path = self._generate_report()
            
            self.logger.log_step_end("report_generation")
            
            # Calculate total time
            total_time = time.time() - start_time
            self.results["total_time"] = total_time
            
            # Print footer
            self._print_footer()
            
            # Call on_complete callback if provided
            if 'on_complete' in self.callbacks:
                self.callbacks['on_complete'](self)
                
            return self
        except Exception as e:
            self.logger.log_error(f"Step 'fit' failed after {time.time() - start_time:.2f} seconds: {str(e)}")
            print(f"✗ Error in fit method: {str(e)}")
            raise
            
    def predict(self, X: Union[pd.DataFrame, List, np.ndarray]) -> np.ndarray:
        """
        Make predictions with the best model.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")
            
        # Preprocess data if preprocessor is available
        if self.preprocessor is not None:
            X = self.preprocessor.transform(X)
            
        # Make predictions
        return self.best_model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make probability predictions with the best model.
        
        Args:
            X: Features
            
        Returns:
            Probability predictions
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")
            
        if self.task_type != "classification":
            raise ValueError("Probability predictions are only available for classification tasks.")
            
        if not hasattr(self.best_model, "predict_proba"):
            raise ValueError(f"Model '{self.best_model_name}' does not support probability predictions.")
            
        # Preprocess data if preprocessor is available
        if self.preprocessor is not None:
            X = self.preprocessor.transform(X)
            
        # Make probability predictions
        return self.best_model.predict_proba(X)
    
    def score(self, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Score the best model.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Score
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")
            
        # Preprocess data if preprocessor is available
        if self.preprocessor is not None:
            X = self.preprocessor.transform(X)
            
        # Score model
        return self.best_model.score(X, y)
    
    def plot(self, plot_type: str = "all", show: bool = True) -> Union[str, Dict[str, str]]:
        """
        Generate and display plots for the best model.

        Args:
            plot_type: Type of plot to generate. Options include:
                - 'all': Generate all relevant plots for the task type.
                - 'feature_importance': Plot feature importance.
                - 'confusion_matrix': Plot confusion matrix (classification only).
                - 'roc_curve': Plot ROC curve (classification only).
                - 'precision_recall_curve': Plot Precision-Recall curve (classification only).
                - 'residuals': Plot residuals (regression only).
                - 'actual_vs_predicted': Plot actual vs predicted values (regression only).
                - 'class_distribution': Plot class distribution of the target variable (classification only).
                - 'target_distribution': Plot distribution of the target variable (regression only).
                - 'correlation_matrix': Plot correlation matrix of features.
            show: Whether to display the plots interactively. Defaults to True.

        Returns:
            If plot_type is 'all', returns a dictionary of plot paths.
            Otherwise, returns the path to the generated plot file.
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")

        # Ensure evaluation results are available
        if not self.results.get("evaluation") or not self.results["evaluation"].get("models", {}).get(self.best_model_name):
             # Re-evaluate if necessary (or raise error)
             # For simplicity, let's assume fit() populated evaluation results correctly.
             # If not, we might need to call _evaluate_models here, but that requires split_data.
             # Let's retrieve split_data if it exists.
             split_data = self.results.get("data", {}).get("split_data_ref") # Need to store this in fit
             if not split_data:
                 raise ValueError("Evaluation results and split data are missing. Cannot generate plots.")
             # Re-run evaluation for the best model if needed - this adds complexity, let's assume results exist for now.
             # self._evaluate_models({self.best_model_name: self.best_model}, split_data)
             pass # Assuming results exist

        # Retrieve necessary data
        # Need to ensure split_data (X_test, y_test) is stored during fit or accessible
        # Let's modify _split_data to store a reference
        split_data = self.results.get("data", {}).get("split_data_ref")
        if not split_data:
             raise ValueError("Split data reference not found in results. Cannot generate plots.")
        X_test = split_data["X_test"]
        y_test = split_data["y_test"]
        X_train = split_data["X_train"] # For correlation matrix
        y_train = split_data["y_train"] # For distribution plots

        # Get predictions (might need re-prediction if not stored)
        y_pred = self.best_model.predict(X_test)
        y_prob = None
        if self.task_type == "classification" and hasattr(self.best_model, "predict_proba"):
            try:
                y_prob = self.best_model.predict_proba(X_test)
            except Exception as e:
                self.logger.log_warning(f"Could not get probability predictions for {self.best_model_name}: {e}")

        plot_paths = {}
        supported_plots = []

        # Define plots based on task type
        if self.task_type == "classification":
            supported_plots = [
                "feature_importance", "confusion_matrix", "roc_curve",
                "precision_recall_curve", "class_distribution", "correlation_matrix"
            ]
        elif self.task_type == "regression":
            supported_plots = [
                "feature_importance", "residuals", "actual_vs_predicted",
                "target_distribution", "correlation_matrix"
            ]

        plots_to_generate = supported_plots if plot_type == "all" else [plot_type]

        for p_type in plots_to_generate:
            if p_type not in supported_plots and plot_type != "all":
                 raise ValueError(f"Unsupported plot type '{p_type}' for task '{self.task_type}'. Supported: {supported_plots}")
            if p_type not in supported_plots:
                continue # Skip plots not relevant for this task type when plot_type='all'

            save_path = os.path.join(self.plots_dir, f"{self.best_model_name}_{p_type}.png")
            plot_title = f"{p_type.replace('_', ' ').title()} ({self.best_model_name})"

            try:
                if p_type == "feature_importance":
                    if "explanation" in self.results and "feature_importance" in self.results["explanation"]:
                        importance_data = self.results["explanation"]["feature_importance"].get("model") or \
                                          self.results["explanation"]["feature_importance"].get("permutation")
                        if importance_data:
                            features = [item["feature"] for item in importance_data]
                            importance = [item["importance"] for item in importance_data]
                            self.plot_utils.plot_feature_importance(features, importance, title=plot_title, save_path=save_path, show=show)
                            plot_paths[p_type] = save_path
                        else:
                            self.logger.log_warning("Feature importance data not found.")
                    else:
                        self.logger.log_warning("Explanation results for feature importance not found.")

                elif p_type == "confusion_matrix" and self.task_type == "classification":
                    class_names = list(map(str, np.unique(y_test)))
                    self.plot_utils.plot_confusion_matrix(y_test, y_pred, class_names=class_names, title=plot_title, save_path=save_path, show=show)
                    plot_paths[p_type] = save_path

                elif p_type == "roc_curve" and self.task_type == "classification":
                    if y_prob is not None:
                        # Use probability of positive class for binary or handle multiclass inside plot_utils
                        score = y_prob[:, 1] if len(y_prob.shape) > 1 and y_prob.shape[1] == 2 else y_prob
                        self.plot_utils.plot_roc_curve(y_test, score, title=plot_title, save_path=save_path, show=show)
                        plot_paths[p_type] = save_path
                    else:
                        self.logger.log_warning("ROC curve requires probability predictions.")

                elif p_type == "precision_recall_curve" and self.task_type == "classification":
                    if y_prob is not None:
                        score = y_prob[:, 1] if len(y_prob.shape) > 1 and y_prob.shape[1] == 2 else y_prob
                        self.plot_utils.plot_precision_recall_curve(y_test, score, title=plot_title, save_path=save_path, show=show)
                        plot_paths[p_type] = save_path
                    else:
                        self.logger.log_warning("Precision-Recall curve requires probability predictions.")

                elif p_type == "residuals" and self.task_type == "regression":
                    self.plot_utils.plot_residuals(y_test, y_pred, title=plot_title, save_path=save_path, show=show)
                    plot_paths[p_type] = save_path

                elif p_type == "actual_vs_predicted" and self.task_type == "regression":
                    self.plot_utils.plot_actual_vs_predicted(y_test, y_pred, title=plot_title, save_path=save_path, show=show)
                    plot_paths[p_type] = save_path

                elif p_type == "class_distribution" and self.task_type == "classification":
                    self.plot_utils.plot_class_distribution(y_train, title="Training Set Class Distribution", save_path=save_path, show=show)
                    plot_paths[p_type] = save_path

                elif p_type == "target_distribution" and self.task_type == "regression":
                    self.plot_utils.plot_target_distribution(y_train, title="Training Set Target Distribution", save_path=save_path, show=show)
                    plot_paths[p_type] = save_path

                elif p_type == "correlation_matrix":
                     # Use original features before preprocessing if possible, otherwise use training features
                     # Need to store original X or handle this better.
                     # Using X_train for now.
                     numeric_cols = X_train.select_dtypes(include=np.number).columns
                     if not numeric_cols.empty:
                         self.plot_utils.plot_correlation_matrix(X_train[numeric_cols], title="Training Set Feature Correlation", save_path=save_path, show=show)
                         plot_paths[p_type] = save_path
                     else:
                         self.logger.log_warning("No numeric features found in training data for correlation matrix.")

            except Exception as e:
                self.logger.log_error(f"Failed to generate plot '{p_type}': {e}")

        if plot_type == "all":
            return plot_paths
        elif plot_type in plot_paths:
            return plot_paths[plot_type]
        else:
            # This case occurs if the requested plot_type failed or was not applicable
            self.logger.log_warning(f"Plot '{plot_type}' could not be generated.")
            return ""
    
    def export_model(self, path: str) -> str:
        """
        Export model to file.
        
        Args:
            path: Path to save model
            
        Returns:
            Path to exported model
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        # Export model
        with open(path, "wb") as f:
            pickle.dump(self.best_model, f)
            
        return path
    
    def generate_report(self, path: Optional[str] = None) -> str:
        """
        Generate report.
        
        Args:
            path: Path to save report
            
        Returns:
            Path to generated report
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")
            
        # Initialize report generator
        self.report_generator = ReportGenerator(
            output_dir=os.path.dirname(os.path.abspath(path)) if path else os.path.join(self.output_dir, "reports")
        )
        
        # Update results with best model information
        self.results["models"]["best"] = {
            "name": self.best_model_name,
            "model_type": type(self.best_model).__name__,
            "metrics": self.results["evaluation"]["models"][self.best_model_name]["metrics"] if self.best_model_name in self.results["evaluation"]["models"] else {}
        }
        
        # Generate report
        report_paths = self.report_generator.generate_report(
            results=self.results,
            report_name=os.path.basename(path).split(".")[0] if path else None
        )
        
        # Return PDF report path
        return report_paths.get("pdf", "")
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get results.
        
        Returns:
            Dictionary with results
        """
        return self.results
        
    def get_best_model(self) -> Tuple[BaseEstimator, str]:
        """
        Get the best model and its name.
        
        Returns:
            Tuple containing the best model and its name
        """
        if self.best_model is None:
            raise ValueError("No model has been trained. Call 'fit' first.")
            
        return self.best_model, self.best_model_name
    
    def _determine_task_type(self, y: pd.Series) -> None:
        """
        Determine task type based on target variable.
        
        Args:
            y: Target
        """
        # Check if target is categorical
        if y.dtype == "object" or y.dtype == "category" or len(y.unique()) <= 10:
            self.task_type = "classification"
        else:
            self.task_type = "regression"
            
        # Update task type in results
        self.results["task_type"] = self.task_type
        
    def _analyze_data_and_print_header(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Analyze data and print header.
        
        Args:
            X: Features
            y: Target
        """
        # Get feature types
        numeric_features = X.select_dtypes(include=["int", "float"]).columns.tolist()
        categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()
        datetime_features = X.select_dtypes(include=["datetime"]).columns.tolist()
        other_features = [col for col in X.columns if col not in numeric_features + categorical_features + datetime_features]
        
        # Get missing values
        missing_values = X.isna().sum().sum()
        missing_percentage = missing_values / (X.shape[0] * X.shape[1]) * 100
        
        # Get class distribution for classification
        if self.task_type == "classification":
            n_classes = len(y.unique())
            class_distribution = y.value_counts().to_dict()
        else:
            n_classes = None
            class_distribution = None
            target_min = float(y.min())
            target_max = float(y.max())
            target_mean = float(y.mean())
            target_std = float(y.std())
            
        # Store data information
        self.results["data"]["original"] = {
            "n_samples": len(X),
            "n_features": X.shape[1],
            "feature_names": X.columns.tolist(),
            "feature_types": {
                "numeric": numeric_features,
                "categorical": categorical_features,
                "datetime": datetime_features,
                "other": other_features
            },
            "missing_values": {
                "count": int(missing_values),
                "percentage": float(missing_percentage)
            },
            "task_type": self.task_type
        }
        
        if self.task_type == "classification":
            self.results["data"]["original"]["classification"] = {
                "n_classes": n_classes,
                "class_distribution": class_distribution
            }
        else: # Regression
            self.results["data"]["original"]["regression"] = {
                "target_min": target_min,
                "target_max": target_max,
                "target_mean": target_mean,
                "target_std": target_std
            }
            
        # Print header
        print("=" * 80)
        print("Starting HumanML Machine Learning Pipeline")
        print("=" * 80)
        print("Dataset Information:")
        print(f"  • Number of samples: {len(X)}")
        print(f"  • Number of features: {X.shape[1]}")
        print(f"  • Feature types: Numeric: {len(numeric_features)}, Categorical: {len(categorical_features)}, Datetime: {len(datetime_features)}, Other: {len(other_features)}")
        print(f"  • Missing values: {missing_values} ({missing_percentage:.2f}%)")
        print(f"  • Task type: {self.task_type.capitalize()}")
        
        if self.task_type == "classification":
            print(f"  • Number of classes: {n_classes}")
            print(f"  • Class distribution: {', '.join([f'{k}: {v}' for k, v in class_distribution.items()])}")
            
        print("-" * 80)
        print("Pipeline will execute the following steps:")
        print("  Step 1: Data preprocessing and feature engineering")
        print("  Step 2: Model selection and hyperparameter tuning")
        print("  Step 3: Model training and evaluation")
        print("  Step 4: Model explanation and visualization")
        print("  Step 5: Report generation and model export")
        print("-" * 80)
        print(f"Output directory: {self.output_dir}")
        print("=" * 80)
        
    def _print_footer(self) -> None:
        """
        Print footer.
        """
        print("\n" + "=" * 80)
        print("HumanML Pipeline Completed")
        print("=" * 80)
        print(f"Best model: {self.best_model_name}")
        
        if self.task_type == "classification":
            print(f"Accuracy: {self.results['evaluation']['models'][self.best_model_name]['metrics']['accuracy']:.4f}")
        else:
            print(f"R2 Score: {self.results['evaluation']['models'][self.best_model_name]['metrics']['r2']:.4f}")
            print(f"RMSE: {self.results['evaluation']['models'][self.best_model_name]['metrics']['rmse']:.4f}")
            
        print("=" * 80)
        print("\nNext steps:")
        print("  • Use .predict() method to make predictions with the best model")
        print("  • Use .plot() method to generate visualizations")
        print("  • Use .export_model() method to export the model to a different location")
        print("  • Use .generate_report() method to generate a new report")
        print("=" * 80)
        
    def _analyze_data(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Analyze data.
        
        Args:
            X: Features
            y: Target
        """
        self.logger.log_step_start("data_analysis")
        
        # Log data information
        self.logger.log_info(f"Number of samples: {len(X)}")
        self.logger.log_info(f"Number of features: {X.shape[1]}")
        
        # Log metrics
        self.logger.log_metric("n_samples", len(X))
        self.logger.log_metric("n_features", X.shape[1])
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Data Analysis", 1)
            
        self.logger.log_step_end("data_analysis")
        
    def _preprocess_data(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """
        Preprocess data.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Preprocessed features
        """
        self.logger.log_step_start("data_preprocessing")
        
        # Initialize preprocessor
        self.preprocessor = DataPreprocessor(
            task_type=self.task_type,
            verbose=False,  # Set to False to suppress detailed logs
            random_state=self.random_state,
            n_jobs=self.n_jobs
        )
        
        # Initialize data splitter
        self.data_splitter = DataSplitter(
            test_size=self.test_size,
            validation_size=self.validation_size,
            random_state=self.random_state
        )
        
        # Fit and transform data
        X_processed = self.preprocessor.fit_transform(X, y)
        
        # Store preprocessing results
        self.results["preprocessing"] = self.preprocessor.get_preprocessing_results()
        
        # Log preprocessing results
        self.logger.log_info(f"Preprocessed data shape: {X_processed.shape}")
        self.logger.log_metric("n_features_after_preprocessing", X_processed.shape[1])
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Data Preprocessing", 2)
            
        self.logger.log_step_end("data_preprocessing")
            
        return X_processed
    
    def _split_data(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, pd.DataFrame]:
        """
        Split data into train, validation, and test sets.
        
        Args:
            X: Features
            y: Target
            
        Returns:
            Dictionary with split data
        """
        self.logger.log_step_start("data_splitting")
        
        # Split data
        split_data = self.data_splitter.split_data(X, y)
        
        # Store split information
        self.results["data"]["split"] = {
            "test_size": self.test_size,
            "validation_size": self.validation_size,
            "train_samples": len(split_data["X_train"]),
            "validation_samples": len(split_data["X_val"]),
            "test_samples": len(split_data["X_test"])
        }
        # Store reference to split data for later use (e.g., plotting)
        self.results["data"]["split_data_ref"] = split_data
        
        # Log split information
        self.logger.log_info(f"Train set: {self.results['data']['split']['train_samples']} samples")
        self.logger.log_info(f"Validation set: {self.results['data']['split']['validation_samples']} samples")
        self.logger.log_info(f"Test set: {self.results['data']['split']['test_samples']} samples")
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Data Splitting", 3)
            
        self.logger.log_step_end("data_splitting")
            
        return split_data
    
    def _select_models(self, X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, Any]:
        """
        Select models based on task type and preference.
        
        Args:
            X_train: Training features
            y_train: Training target
            
        Returns:
            Dictionary of selected models
        """
        # Initialize model selector
        self.model_selector = ModelSelector(
            preference=self.preference,  # Use balanced preference by default
            included_models=self.models,  # Pass included models if specified
            verbose=False,  # Set to False to suppress detailed logs
            n_jobs=self.n_jobs,
            random_state=self.random_state
        )
        
        # Initialize model trainer
        self.model_trainer = ModelTrainer(
            task_type=self.task_type,
            hyperparameter_tuning=self.hyperparameter_tuning,
            cross_validation=self.cross_validation,
            verbose=False,  # Set to False to suppress detailed logs
            n_jobs=self.n_jobs,
            random_state=self.random_state
        )
        
        # Select models
        selected_models = self.model_selector.select_models(X_train, y_train, self.task_type)
        
        # Store selection results
        self.results["models"]["selection"] = self.model_selector.get_selection_results()
        
        # Log selection results
        self.logger.log_info(f"Selected {len(selected_models)} models")
        for name in selected_models.keys():
            self.logger.log_info(f"  • {name}")
            
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Model Selection", 4)
            
        return selected_models
    
    def _evaluate_models(self, trained_models: Dict[str, Any], split_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Evaluate trained models.
        
        Args:
            trained_models: Dictionary of trained models
            split_data: Dictionary with split data
            
        Returns:
            Dictionary with evaluation results
        """
        # Initialize model evaluator
        self.model_evaluator = ModelEvaluator(
            task_type=self.task_type,
            verbose=False,  # Set to False to suppress detailed logs
            plots_dir=None # Plots generated on demand by .plot()
        )
        
        # Evaluate models
        evaluation_results = self.model_evaluator.evaluate_models(
            trained_models,
            split_data["X_test"],
            split_data["y_test"],
            split_data["X_train"],
            split_data["y_train"]
        )
        
        # Store evaluation results
        self.results["evaluation"] = evaluation_results
        
        # Log evaluation results
        self.logger.log_info(f"Evaluated {len(trained_models)} models")
        for name, results in evaluation_results["models"].items():
            if "metrics" in results:
                if self.task_type == "classification":
                    self.logger.log_info(f"  • {name}: Accuracy = {results['metrics'].get('accuracy', 'N/A')}")
                else:
                    self.logger.log_info(f"  • {name}: R2 = {results['metrics'].get('r2', 'N/A')}")
                    
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Model Evaluation", 6)
                    
        return evaluation_results
    
    def _select_best_model(self, trained_models: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Tuple[str, Any]:
        """
        Select best model based on evaluation results.
        
        Args:
            trained_models: Dictionary of trained models
            evaluation_results: Dictionary with evaluation results
            
        Returns:
            Tuple of (best model name, best model)
        """
        # Initialize best model
        best_model_name = None
        best_model = None
        best_score = float('-inf')
        
        # Select best model based on task type
        if self.task_type == "classification":
            # Select model with highest accuracy
            for name, results in evaluation_results["models"].items():
                if "metrics" in results and "accuracy" in results["metrics"]:
                    if results["metrics"]["accuracy"] > best_score:
                        best_score = results["metrics"]["accuracy"]
                        best_model_name = name
                        best_model = trained_models[name]
        else:
            # Select model with highest R2
            for name, results in evaluation_results["models"].items():
                if "metrics" in results and "r2" in results["metrics"]:
                    if results["metrics"]["r2"] > best_score:
                        best_score = results["metrics"]["r2"]
                        best_model_name = name
                        best_model = trained_models[name]
                        
        # Store best model information
        self.results["models"]["best"] = {
            "name": best_model_name,
            "score": float(best_score)
        }
        
        # Log best model
        self.logger.log_info(f"Best model: {best_model_name} with score {best_score:.4f}")
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Best Model Selection", 7)
                        
        return best_model_name, best_model
    
    def _explain_model(self, model: Any, model_name: str, split_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Explain model.
        
        Args:
            model: Model to explain
            model_name: Model name
            split_data: Dictionary with split data
            
        Returns:
            Dictionary with explanation results
        """
        # Initialize model explainer
        self.model_explainer = ModelExplainer(
            task_type=self.task_type,
            verbose=False,  # Set to False to suppress detailed logs
            plots_dir=None # Plots generated on demand by .plot()
        )
        
        # Explain model
        explanation_results = self.model_explainer.explain_model(
            model,
            model_name,
            split_data["X_test"],
            split_data["y_test"],
            self.results["data"]["original"]["feature_names"]
        )
        
        # Store explanation results
        self.results["explanation"] = explanation_results
        
        # Log explanation results
        self.logger.log_info(f"Explained model {model_name}")
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Model Explanation", 8)
                        
        return explanation_results
    
    def _generate_report(self) -> str:
        """
        Generate report.
        
        Returns:
            Path to generated report
        """
        # Initialize report generator
        self.report_generator = ReportGenerator(
            output_dir=os.path.join(self.output_dir, "reports")
        )
        
        # Generate report
        report_paths = self.report_generator.generate_report(
            results=self.results
        )
        
        # Store report path
        self.results["export"]["report"] = report_paths
        
        # Log report generation
        self.logger.log_info(f"Generated report: {report_paths}")
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Report Generation", 9)
                        
        return report_paths.get("pdf", "")
    
    def _export_model(self, model: Any, model_name: str) -> str:
        """
        Export model.
        
        Args:
            model: Model to export
            model_name: Model name
            
        Returns:
            Path to exported model
        """
        # Initialize model exporter
        self.model_exporter = ModelExporter(
            output_dir=self.models_dir,
            verbose=False  # Set to False to suppress detailed logs
        )
        
        # Export model
        model_path = self.model_exporter.export_model(
            model=model,
            model_name=model_name
        )
        
        # Store model path
        self.results["export"]["model"] = model_path
        
        # Log model export
        self.logger.log_info(f"Exported model: {model_path}")
        
        # Call on_step_end callback if provided
        if 'on_step_end' in self.callbacks:
            self.callbacks['on_step_end'](self, "Model Export", 10)
                        
        return model_path
