#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model Evaluator Module for HumanML.

Provides comprehensive model evaluation capabilities with various metrics,
confusion matrices, ROC curves, and other evaluation tools.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, mean_absolute_percentage_error
)


class ModelEvaluator:
    """
    Comprehensive model evaluator with various metrics, confusion matrices,
    ROC curves, and other evaluation tools.
    """
    
    def __init__(
        self,
        task_type: str,
        verbose: bool = True,
        plots_dir: Optional[str] = None
    ):
        """
        Initialize the ModelEvaluator.
        
        Args:
            task_type: Task type ('classification' or 'regression')
            verbose: Whether to print detailed information
            plots_dir: Directory to save plots
        """
        self.task_type = task_type
        self.verbose = verbose
        self.plots_dir = plots_dir
        
        # Initialize evaluation results
        self.evaluation_results = {}
        
    def evaluate_models(
        self,
        models: Dict[str, BaseEstimator],
        X_test: pd.DataFrame,
        y_test: pd.Series,
        X_train: Optional[pd.DataFrame] = None,
        y_train: Optional[pd.Series] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Evaluate models on test data.
        
        Args:
            models: Dictionary of models to evaluate
            X_test: Test features
            y_test: Test target
            X_train: Training features (optional, for additional metrics)
            y_train: Training target (optional, for additional metrics)
            
        Returns:
            Dictionary with evaluation results
        """
        # Initialize evaluation results
        self.evaluation_results = {
            "task_type": self.task_type,
            "models": {}
        }
        
        if self.verbose:
            print(f"Evaluating {len(models)} models...")
            
        # Evaluate each model
        for name, model in models.items():
            if self.verbose:
                print(f"Evaluating {name}...")
                
            # Initialize model evaluation results
            self.evaluation_results["models"][name] = {
                "metrics": {},
                "plots": {}
            }
            
            try:
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Evaluate based on task type
                if self.task_type == "classification":
                    # Calculate classification metrics
                    self._evaluate_classification(name, model, X_test, y_test, y_pred)
                else:
                    # Calculate regression metrics
                    self._evaluate_regression(name, model, X_test, y_test, y_pred)
                    
                # Calculate additional metrics if training data is provided
                if X_train is not None and y_train is not None:
                    # Calculate training predictions
                    y_train_pred = model.predict(X_train)
                    
                    # Calculate overfitting metrics
                    self._calculate_overfitting_metrics(
                        name, y_train, y_train_pred, y_test, y_pred
                    )
                    
                if self.verbose:
                    print(f"  • Evaluation completed for {name}")
                    
            except Exception as e:
                # Store error
                self.evaluation_results["models"][name]["error"] = str(e)
                
                if self.verbose:
                    print(f"  • Failed to evaluate {name}: {str(e)}")
                    
        return self.evaluation_results
    
    def _evaluate_classification(
        self,
        name: str,
        model: BaseEstimator,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        y_pred: np.ndarray
    ) -> None:
        """
        Evaluate classification model.
        
        Args:
            name: Model name
            model: Model to evaluate
            X_test: Test features
            y_test: Test target
            y_pred: Test predictions
        """
        # Calculate basic metrics
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, average='weighted')),
            "recall": float(recall_score(y_test, y_pred, average='weighted')),
            "f1": float(f1_score(y_test, y_pred, average='weighted'))
        }
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics["confusion_matrix"] = cm.tolist()
        
        # Calculate classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        metrics["classification_report"] = report
        
        # Calculate ROC AUC if model has predict_proba method
        if hasattr(model, "predict_proba"):
            try:
                # Get probability predictions
                y_prob = model.predict_proba(X_test)
                
                # Calculate ROC AUC for binary classification
                if len(np.unique(y_test)) == 2:
                    metrics["roc_auc"] = float(roc_auc_score(y_test, y_prob[:, 1]))
                # Calculate ROC AUC for multiclass classification
                else:
                    metrics["roc_auc"] = float(roc_auc_score(
                        pd.get_dummies(y_test), y_prob, multi_class='ovr'
                    ))
            except Exception:
                # ROC AUC calculation failed
                metrics["roc_auc"] = None
                
        # Store metrics
        self.evaluation_results["models"][name]["metrics"] = metrics
        
        # Generate plots if plots_dir is provided
        if self.plots_dir is not None:
            # Generate confusion matrix plot
            self._plot_confusion_matrix(name, cm, list(np.unique(y_test)))
            
            # Generate ROC curve if model has predict_proba method
            if hasattr(model, "predict_proba") and metrics["roc_auc"] is not None:
                self._plot_roc_curve(name, model, X_test, y_test)
                
    def _evaluate_regression(
        self,
        name: str,
        model: BaseEstimator,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        y_pred: np.ndarray
    ) -> None:
        """
        Evaluate regression model.
        
        Args:
            name: Model name
            model: Model to evaluate
            X_test: Test features
            y_test: Test target
            y_pred: Test predictions
        """
        # Calculate basic metrics
        metrics = {
            "mse": float(mean_squared_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "r2": float(r2_score(y_test, y_pred)),
            "explained_variance": float(explained_variance_score(y_test, y_pred))
        }
        
        # Calculate MAPE if no zeros in y_test
        if not np.any(y_test == 0):
            metrics["mape"] = float(mean_absolute_percentage_error(y_test, y_pred))
        
        # Store metrics
        self.evaluation_results["models"][name]["metrics"] = metrics
        
        # Generate plots if plots_dir is provided
        if self.plots_dir is not None:
            # Generate residual plot
            self._plot_residuals(name, y_test, y_pred)
            
            # Generate actual vs predicted plot
            self._plot_actual_vs_predicted(name, y_test, y_pred)
            
    def _calculate_overfitting_metrics(
        self,
        name: str,
        y_train: pd.Series,
        y_train_pred: np.ndarray,
        y_test: pd.Series,
        y_test_pred: np.ndarray
    ) -> None:
        """
        Calculate overfitting metrics.
        
        Args:
            name: Model name
            y_train: Training target
            y_train_pred: Training predictions
            y_test: Test target
            y_test_pred: Test predictions
        """
        # Calculate metrics based on task type
        if self.task_type == "classification":
            # Calculate training accuracy
            train_accuracy = accuracy_score(y_train, y_train_pred)
            
            # Calculate test accuracy
            test_accuracy = accuracy_score(y_test, y_test_pred)
            
            # Calculate overfitting ratio
            overfitting_ratio = train_accuracy / test_accuracy if test_accuracy > 0 else float('inf')
            
            # Store overfitting metrics
            self.evaluation_results["models"][name]["metrics"]["train_accuracy"] = float(train_accuracy)
            self.evaluation_results["models"][name]["metrics"]["overfitting_ratio"] = float(overfitting_ratio)
        else:
            # Calculate training R2
            train_r2 = r2_score(y_train, y_train_pred)
            
            # Calculate test R2
            test_r2 = r2_score(y_test, y_test_pred)
            
            # Calculate overfitting ratio
            overfitting_ratio = train_r2 / test_r2 if test_r2 > 0 else float('inf')
            
            # Store overfitting metrics
            self.evaluation_results["models"][name]["metrics"]["train_r2"] = float(train_r2)
            self.evaluation_results["models"][name]["metrics"]["overfitting_ratio"] = float(overfitting_ratio)
            
    def _plot_confusion_matrix(
        self,
        name: str,
        cm: np.ndarray,
        classes: List[str]
    ) -> None:
        """
        Plot confusion matrix.
        
        Args:
            name: Model name
            cm: Confusion matrix
            classes: Class labels
        """
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Plot confusion matrix
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(f'Confusion Matrix - {name}')
        plt.colorbar()
        
        # Add class labels
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)
        
        # Add text annotations
        thresh = cm.max() / 2.0
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                        horizontalalignment="center",
                        color="white" if cm[i, j] > thresh else "black")
                
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        
        # Save plot
        plt.savefig(f"{self.plots_dir}/{name}_confusion_matrix.png")
        plt.close()
        
        # Store plot path
        self.evaluation_results["models"][name]["plots"]["confusion_matrix"] = f"{self.plots_dir}/{name}_confusion_matrix.png"
        
    def _plot_roc_curve(
        self,
        name: str,
        model: BaseEstimator,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> None:
        """
        Plot ROC curve.
        
        Args:
            name: Model name
            model: Model to evaluate
            X_test: Test features
            y_test: Test target
        """
        from sklearn.metrics import roc_curve, auc
        from sklearn.preprocessing import label_binarize
        
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Get unique classes
        classes = np.unique(y_test)
        n_classes = len(classes)
        
        # Binary classification
        if n_classes == 2:
            # Get probability predictions
            y_prob = model.predict_proba(X_test)[:, 1]
            
            # Calculate ROC curve
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            
            # Plot ROC curve
            plt.plot(fpr, tpr, lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], 'k--', lw=2)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'ROC Curve - {name}')
            plt.legend(loc="lower right")
        # Multiclass classification
        else:
            # Binarize labels
            y_bin = label_binarize(y_test, classes=classes)
            
            # Get probability predictions
            y_prob = model.predict_proba(X_test)
            
            # Calculate ROC curve for each class
            fpr = {}
            tpr = {}
            roc_auc = {}
            
            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_prob[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
                
                # Plot ROC curve for each class
                plt.plot(fpr[i], tpr[i], lw=2,
                        label=f'ROC curve of class {classes[i]} (area = {roc_auc[i]:.2f})')
                
            plt.plot([0, 1], [0, 1], 'k--', lw=2)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'ROC Curve - {name}')
            plt.legend(loc="lower right")
            
        # Save plot
        plt.savefig(f"{self.plots_dir}/{name}_roc_curve.png")
        plt.close()
        
        # Store plot path
        self.evaluation_results["models"][name]["plots"]["roc_curve"] = f"{self.plots_dir}/{name}_roc_curve.png"
        
    def _plot_residuals(
        self,
        name: str,
        y_test: pd.Series,
        y_pred: np.ndarray
    ) -> None:
        """
        Plot residuals.
        
        Args:
            name: Model name
            y_test: Test target
            y_pred: Test predictions
        """
        # Calculate residuals
        residuals = y_test - y_pred
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Plot residuals
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='-')
        plt.xlabel('Predicted')
        plt.ylabel('Residuals')
        plt.title(f'Residual Plot - {name}')
        
        # Save plot
        plt.savefig(f"{self.plots_dir}/{name}_residuals.png")
        plt.close()
        
        # Store plot path
        self.evaluation_results["models"][name]["plots"]["residuals"] = f"{self.plots_dir}/{name}_residuals.png"
        
    def _plot_actual_vs_predicted(
        self,
        name: str,
        y_test: pd.Series,
        y_pred: np.ndarray
    ) -> None:
        """
        Plot actual vs predicted values.
        
        Args:
            name: Model name
            y_test: Test target
            y_pred: Test predictions
        """
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Plot actual vs predicted
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title(f'Actual vs Predicted - {name}')
        
        # Save plot
        plt.savefig(f"{self.plots_dir}/{name}_actual_vs_predicted.png")
        plt.close()
        
        # Store plot path
        self.evaluation_results["models"][name]["plots"]["actual_vs_predicted"] = f"{self.plots_dir}/{name}_actual_vs_predicted.png"
        
    def get_evaluation_results(self) -> Dict[str, Any]:
        """
        Get evaluation results.
        
        Returns:
            Dictionary with evaluation results
        """
        return self.evaluation_results


# Example Usage (for testing purposes)
if __name__ == "__main__":
    print("Running ModelEvaluator Example...")
    
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
    
    # Create and train models
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    models = {
        "random_forest": RandomForestClassifier(random_state=42),
        "gradient_boosting": GradientBoostingClassifier(random_state=42)
    }
    
    # Train models
    for name, model in models.items():
        model.fit(X_train, y_train)
    
    # Initialize model evaluator
    import os
    os.makedirs("plots", exist_ok=True)
    
    evaluator = ModelEvaluator(
        task_type="classification",
        verbose=True,
        plots_dir="plots"
    )
    
    # Evaluate models
    evaluation_results = evaluator.evaluate_models(
        models, X_test, y_test, X_train, y_train
    )
    
    # Print evaluation results
    print("\nEvaluation Results:")
    for name, results in evaluation_results["models"].items():
        print(f"\n{name}:")
        print(f"  • Accuracy: {results['metrics']['accuracy']:.4f}")
        print(f"  • Precision: {results['metrics']['precision']:.4f}")
        print(f"  • Recall: {results['metrics']['recall']:.4f}")
        print(f"  • F1: {results['metrics']['f1']:.4f}")
        if "roc_auc" in results["metrics"] and results["metrics"]["roc_auc"] is not None:
            print(f"  • ROC AUC: {results['metrics']['roc_auc']:.4f}")
        if "train_accuracy" in results["metrics"]:
            print(f"  • Train Accuracy: {results['metrics']['train_accuracy']:.4f}")
            print(f"  • Overfitting Ratio: {results['metrics']['overfitting_ratio']:.4f}")
        if "plots" in results:
            print("  • Plots:")
            for plot_name, plot_path in results["plots"].items():
                print(f"    - {plot_name}: {plot_path}")
    
    print("\nModelEvaluator example completed successfully!")
