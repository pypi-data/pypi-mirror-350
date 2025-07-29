#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plot Utilities Module for HumanML.

Provides functionality for creating and displaying professional plots
for machine learning model evaluation and visualization.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional, Union, Tuple
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve


class PlotUtilities:
    """
    Create and display professional plots for machine learning model evaluation and visualization.
    """
    
    def __init__(
        self,
        plots_dir: str = "plots",
        style: str = "whitegrid",
        context: str = "notebook",
        palette: str = "deep",
        font_scale: float = 1.2
    ):
        """
        Initialize the PlotUtilities.
        
        Args:
            plots_dir: Directory to save plots
            style: Seaborn style
            context: Seaborn context
            palette: Seaborn color palette
            font_scale: Font scale for plots
        """
        self.plots_dir = plots_dir
        
        # Create plots directory
        os.makedirs(self.plots_dir, exist_ok=True)
        
        # Set plot style
        sns.set_style(style)
        sns.set_context(context, font_scale=font_scale)
        sns.set_palette(palette)
        
        # Set default figure size
        plt.rcParams["figure.figsize"] = (10, 6)
        plt.rcParams["figure.dpi"] = 100
        
    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        class_names: Optional[List[str]] = None,
        normalize: bool = False,
        title: str = "Confusion Matrix",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: List of class names
            normalize: Whether to normalize the confusion matrix
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Normalize if requested
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot heatmap
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)
        
        # Set labels
        if class_names is None:
            class_names = [str(i) for i in range(cm.shape[0])]
            
        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               xticklabels=class_names,
               yticklabels=class_names,
               title=title,
               ylabel='True label',
               xlabel='Predicted label')
        
        # Rotate x tick labels and set alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
                
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_roc_curve(
        self,
        y_true: np.ndarray,
        y_score: np.ndarray,
        title: str = "ROC Curve",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot ROC curve.
        
        Args:
            y_true: True labels
            y_score: Predicted probabilities
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Compute ROC curve and ROC area
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot ROC curve
        ax.plot(fpr, tpr, lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        ax.plot([0, 1], [0, 1], 'k--', lw=2)
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(title)
        ax.legend(loc="lower right")
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_precision_recall_curve(
        self,
        y_true: np.ndarray,
        y_score: np.ndarray,
        title: str = "Precision-Recall Curve",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot precision-recall curve.
        
        Args:
            y_true: True labels
            y_score: Predicted probabilities
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Compute precision-recall curve
        precision, recall, _ = precision_recall_curve(y_true, y_score)
        
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot precision-recall curve
        ax.plot(recall, precision, lw=2)
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_ylim([0.0, 1.05])
        ax.set_xlim([0.0, 1.0])
        ax.set_title(title)
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_feature_importance(
        self,
        feature_names: List[str],
        feature_importance: np.ndarray,
        title: str = "Feature Importance",
        save_path: Optional[str] = None,
        show: bool = True,
        top_n: int = 20
    ) -> plt.Figure:
        """
        Plot feature importance.
        
        Args:
            feature_names: List of feature names
            feature_importance: Feature importance values
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            top_n: Number of top features to display
            
        Returns:
            Matplotlib figure
        """
        # Create dataframe
        df = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importance
        })
        
        # Sort by importance
        df = df.sort_values('importance', ascending=False)
        
        # Select top N features
        if len(df) > top_n:
            df = df.head(top_n)
            
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot feature importance
        sns.barplot(x='importance', y='feature', data=df, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Importance')
        ax.set_ylabel('Feature')
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_residuals(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        title: str = "Residuals",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot residuals.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Compute residuals
        residuals = y_true - y_pred
        
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot residuals
        ax.scatter(y_pred, residuals, alpha=0.5)
        ax.axhline(y=0, color='r', linestyle='-')
        ax.set_xlabel('Predicted values')
        ax.set_ylabel('Residuals')
        ax.set_title(title)
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_actual_vs_predicted(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        title: str = "Actual vs Predicted",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot actual vs predicted values.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot actual vs predicted
        ax.scatter(y_true, y_pred, alpha=0.5)
        
        # Add perfect prediction line
        min_val = min(np.min(y_true), np.min(y_pred))
        max_val = max(np.max(y_true), np.max(y_pred))
        ax.plot([min_val, max_val], [min_val, max_val], 'r--')
        
        ax.set_xlabel('Actual values')
        ax.set_ylabel('Predicted values')
        ax.set_title(title)
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_learning_curve(
        self,
        train_sizes: np.ndarray,
        train_scores: np.ndarray,
        test_scores: np.ndarray,
        title: str = "Learning Curve",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot learning curve.
        
        Args:
            train_sizes: Training set sizes
            train_scores: Training scores
            test_scores: Test scores
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot learning curve
        ax.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', label='Training score')
        ax.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', label='Cross-validation score')
        ax.fill_between(train_sizes, np.mean(train_scores, axis=1) - np.std(train_scores, axis=1),
                        np.mean(train_scores, axis=1) + np.std(train_scores, axis=1), alpha=0.1)
        ax.fill_between(train_sizes, np.mean(test_scores, axis=1) - np.std(test_scores, axis=1),
                        np.mean(test_scores, axis=1) + np.std(test_scores, axis=1), alpha=0.1)
        
        ax.set_xlabel('Training examples')
        ax.set_ylabel('Score')
        ax.set_title(title)
        ax.legend(loc='best')
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_class_distribution(
        self,
        y: pd.Series,
        title: str = "Class Distribution",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot class distribution.
        
        Args:
            y: Target series
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot class distribution
        class_counts = y.value_counts()
        sns.barplot(x=class_counts.index, y=class_counts.values, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Class')
        ax.set_ylabel('Count')
        
        # Rotate x tick labels if there are many classes
        if len(class_counts) > 5:
            plt.xticks(rotation=45, ha='right')
            
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_target_distribution(
        self,
        y: pd.Series,
        title: str = "Target Distribution",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot target distribution.
        
        Args:
            y: Target series
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot target distribution
        sns.histplot(y, kde=True, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_correlation_matrix(
        self,
        X: pd.DataFrame,
        title: str = "Correlation Matrix",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot correlation matrix.
        
        Args:
            X: Features dataframe
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Compute correlation matrix
        corr = X.corr()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Plot correlation matrix
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
        
        ax.set_title(title)
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_optimization_history(
        self,
        iterations: List[int],
        scores: List[float],
        best_scores: List[float],
        title: str = "Optimization History",
        save_path: Optional[str] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Plot optimization history.
        
        Args:
            iterations: List of iteration numbers
            scores: List of scores
            best_scores: List of best scores
            title: Plot title
            save_path: Path to save the plot
            show: Whether to display the plot
            
        Returns:
            Matplotlib figure
        """
        # Create figure
        fig, ax = plt.subplots()
        
        # Plot optimization history
        ax.plot(iterations, scores, 'o-', label='Score')
        ax.plot(iterations, best_scores, 'o-', label='Best Score')
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Score')
        ax.set_title(title)
        ax.legend(loc='best')
        
        fig.tight_layout()
        
        # Save plot if requested
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        # Show plot if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
