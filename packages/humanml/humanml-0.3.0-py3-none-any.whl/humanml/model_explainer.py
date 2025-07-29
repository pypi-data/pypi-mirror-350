#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model Explainer Module for HumanML.

Provides comprehensive model explanation capabilities with feature importance,
partial dependence plots, and SHAP values.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.base import BaseEstimator
from sklearn.inspection import permutation_importance


class ModelExplainer:
    """
    Comprehensive model explainer with feature importance, partial dependence plots,
    and SHAP values.
    """
    
    def __init__(
        self,
        task_type: str,
        verbose: bool = True,
        plots_dir: Optional[str] = None
    ):
        """
        Initialize the ModelExplainer.
        
        Args:
            task_type: Task type ('classification' or 'regression')
            verbose: Whether to print detailed information
            plots_dir: Directory to save plots
        """
        self.task_type = task_type
        self.verbose = verbose
        self.plots_dir = plots_dir
        
        # Initialize explanation results
        self.explanation_results = {}
        
        # Initialize model and data
        self.model = None
        self.X_train = None
        self.feature_names = None
        
        # Create plots directory if provided
        if self.plots_dir:
            os.makedirs(self.plots_dir, exist_ok=True)
        
    def explain_model(
        self,
        model: BaseEstimator,
        model_name: str,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        feature_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Explain model.
        
        Args:
            model: Model to explain
            model_name: Name of the model
            X_test: Test features
            y_test: Test target
            feature_names: List of feature names (optional)
            
        Returns:
            Dictionary with explanation results
        """
        # Store model and data
        self.model = model
        self.X_train = X_test  # Use test data for explanations
        
        # Ensure X_test is a DataFrame
        if not isinstance(X_test, pd.DataFrame):
            if feature_names is not None:
                X_test = pd.DataFrame(X_test, columns=feature_names)
            else:
                X_test = pd.DataFrame(X_test)
        
        # Get feature names
        if feature_names is not None:
            self.feature_names = feature_names
        else:
            self.feature_names = X_test.columns.tolist()
        
        # Initialize explanation results
        self.explanation_results = {
            "task_type": self.task_type,
            "model_name": model_name,
            "feature_importance": {},
            "plots": {}
        }
        
        if self.verbose:
            print(f"Explaining model: {model_name}")
            
        # Calculate feature importance
        self._calculate_feature_importance(X_test, y_test)
        
        # Calculate SHAP values if possible
        self._calculate_shap_values(X_test)
        
        # Generate partial dependence plots if plots_dir is provided
        if self.plots_dir is not None:
            self._generate_partial_dependence_plots(X_test)
            
        return self.explanation_results
    
    def _calculate_feature_importance(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> None:
        """
        Calculate feature importance.
        
        Args:
            X_test: Test features
            y_test: Test target
        """
        # Try to get feature importance from model
        try:
            # Check if model has feature_importances_ attribute
            if hasattr(self.model, "feature_importances_"):
                # Get feature importance
                importance = self.model.feature_importances_
                
                # Store feature importance
                self.explanation_results["feature_importance"]["model"] = [
                    {"feature": feature, "importance": float(imp)}
                    for feature, imp in zip(self.feature_names, importance)
                ]
                
                # Sort feature importance
                self.explanation_results["feature_importance"]["model"].sort(
                    key=lambda x: x["importance"], reverse=True
                )
                
                if self.verbose:
                    print("Calculated feature importance from model")
                    
                # Generate feature importance plot if plots_dir is provided
                if self.plots_dir is not None:
                    self._plot_feature_importance(
                        self.explanation_results["feature_importance"]["model"],
                        "model_feature_importance"
                    )
        except Exception as e:
            if self.verbose:
                print(f"Failed to calculate feature importance from model: {str(e)}")
                
        # Calculate permutation importance
        try:
            # Calculate permutation importance
            perm_importance = permutation_importance(
                self.model, X_test, y_test, n_repeats=5, random_state=42
            )
            
            # Store permutation importance
            self.explanation_results["feature_importance"]["permutation"] = [
                {"feature": feature, "importance": float(imp)}
                for feature, imp in zip(self.feature_names, perm_importance.importances_mean)
            ]
            
            # Sort permutation importance
            self.explanation_results["feature_importance"]["permutation"].sort(
                key=lambda x: x["importance"], reverse=True
            )
            
            if self.verbose:
                print("Calculated permutation importance")
                
            # Generate permutation importance plot if plots_dir is provided
            if self.plots_dir is not None:
                self._plot_feature_importance(
                    self.explanation_results["feature_importance"]["permutation"],
                    "permutation_feature_importance"
                )
        except Exception as e:
            if self.verbose:
                print(f"Failed to calculate permutation importance: {str(e)}")
                    
    def _calculate_shap_values(self, X_test: pd.DataFrame) -> None:
        """
        Calculate SHAP values.
        
        Args:
            X_test: Test features
        """
        try:
            # Try to import shap
            import shap
            
            # Check if model is supported by shap
            try:
                # Create explainer
                explainer = shap.Explainer(self.model, X_test)
                
                # Calculate SHAP values
                sample_size = min(100, len(X_test))
                shap_values = explainer(X_test.iloc[:sample_size])  # Use subset for efficiency
                
                # Store SHAP values
                self.explanation_results["shap"] = {
                    "calculated": True
                }
                
                if self.verbose:
                    print("Calculated SHAP values")
                    
                # Generate SHAP plots if plots_dir is provided
                if self.plots_dir is not None:
                    self._plot_shap_values(explainer, shap_values, X_test.iloc[:sample_size])
            except Exception as e:
                if self.verbose:
                    print(f"Failed to calculate SHAP values: {str(e)}")
                    
                # Store SHAP values
                self.explanation_results["shap"] = {
                    "calculated": False,
                    "error": str(e)
                }
        except ImportError:
            if self.verbose:
                print("SHAP not installed. Skipping SHAP analysis.")
                
            # Store SHAP values
            self.explanation_results["shap"] = {
                "calculated": False,
                "error": "SHAP not installed"
            }
            
    def _generate_partial_dependence_plots(self, X_test: pd.DataFrame) -> None:
        """
        Generate partial dependence plots.
        
        Args:
            X_test: Test features
        """
        try:
            # Try to import sklearn.inspection
            from sklearn.inspection import plot_partial_dependence
            
            # Get top features
            if "model" in self.explanation_results["feature_importance"]:
                top_features = [
                    item["feature"]
                    for item in self.explanation_results["feature_importance"]["model"][:3]
                ]
            elif "permutation" in self.explanation_results["feature_importance"]:
                top_features = [
                    item["feature"]
                    for item in self.explanation_results["feature_importance"]["permutation"][:3]
                ]
            else:
                top_features = self.feature_names[:3]
                
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Generate partial dependence plot
            plot_partial_dependence(
                self.model, X_test, top_features, ax=ax
            )
            
            # Save plot
            plt.savefig(f"{self.plots_dir}/partial_dependence.png")
            plt.close()
            
            # Store plot path
            self.explanation_results["plots"]["partial_dependence"] = f"{self.plots_dir}/partial_dependence.png"
            
            if self.verbose:
                print("Generated partial dependence plots")
        except Exception as e:
            if self.verbose:
                print(f"Failed to generate partial dependence plots: {str(e)}")
                
    def _plot_feature_importance(
        self,
        feature_importance: List[Dict[str, Any]],
        plot_name: str
    ) -> None:
        """
        Plot feature importance.
        
        Args:
            feature_importance: Feature importance
            plot_name: Plot name
        """
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Get features and importance
        features = [item["feature"] for item in feature_importance]
        importance = [item["importance"] for item in feature_importance]
        
        # Sort by importance
        sorted_idx = np.argsort(importance)
        
        # Plot feature importance
        plt.barh(range(len(sorted_idx)), [importance[i] for i in sorted_idx])
        plt.yticks(range(len(sorted_idx)), [features[i] for i in sorted_idx])
        plt.xlabel("Feature Importance")
        plt.ylabel("Feature")
        plt.title(f"Feature Importance ({plot_name})")
        
        # Save plot
        plt.savefig(f"{self.plots_dir}/{plot_name}.png")
        plt.close()
        
        # Store plot path
        self.explanation_results["plots"][plot_name] = f"{self.plots_dir}/{plot_name}.png"
        
    def _plot_shap_values(self, explainer, shap_values, X_sample) -> None:
        """
        Plot SHAP values.
        
        Args:
            explainer: SHAP explainer
            shap_values: SHAP values
            X_sample: Sample data for SHAP plots
        """
        import shap
        
        # Create summary plot
        plt.figure()
        shap.summary_plot(shap_values, X_sample, show=False)
        plt.tight_layout()
        
        # Save plot
        plt.savefig(f"{self.plots_dir}/shap_summary.png")
        plt.close()
        
        # Store plot path
        self.explanation_results["plots"]["shap_summary"] = f"{self.plots_dir}/shap_summary.png"
        
        # Create bar plot
        plt.figure()
        shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
        plt.tight_layout()
        
        # Save plot
        plt.savefig(f"{self.plots_dir}/shap_bar.png")
        plt.close()
        
        # Store plot path
        self.explanation_results["plots"]["shap_bar"] = f"{self.plots_dir}/shap_bar.png"
        
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """
        Get feature importance.
        
        Returns:
            List of dictionaries with feature importance information
        """
        # Check if feature importance has been calculated
        if not self.explanation_results.get("feature_importance"):
            raise ValueError("Feature importance has not been calculated. Call 'explain_model' first.")
            
        # Return feature importance
        if "model" in self.explanation_results["feature_importance"]:
            return self.explanation_results["feature_importance"]["model"]
        elif "permutation" in self.explanation_results["feature_importance"]:
            return self.explanation_results["feature_importance"]["permutation"]
        else:
            return []
    
    def get_explanation_results(self) -> Dict[str, Any]:
        """
        Get explanation results.
        
        Returns:
            Dictionary with explanation results
        """
        return self.explanation_results
