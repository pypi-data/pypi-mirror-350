#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report Generator Module for HumanML.

Provides functionality for generating comprehensive reports of machine learning
experiments, including model performance, feature importance, and visualizations.
"""

import os
import json
import time
import datetime
from typing import Dict, Any, List, Optional, Union, Tuple, Set
import matplotlib.pyplot as plt
from fpdf import FPDF


class ReportGenerator:
    """
    Generate comprehensive reports of machine learning experiments.
    """
    
    def __init__(
        self,
        output_dir: str = "reports",
        formats: List[str] = ["pdf"],
        verbose: bool = True
    ):
        """
        Initialize the ReportGenerator.
        
        Args:
            output_dir: Directory to save reports
            formats: List of report formats to generate
            verbose: Whether to print detailed information
        """
        self.output_dir = output_dir
        self.formats = formats
        self.verbose = verbose
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize report results
        self.report_results = {}
        
    def generate_report(
        self,
        results: Dict[str, Any],
        report_name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate report from results.
        
        Args:
            results: Dictionary with results
            report_name: Name of the report (default: timestamp)
            
        Returns:
            Dictionary with report paths
        """
        # Generate report name if not provided
        if report_name is None:
            report_name = f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        if self.verbose:
            print(f"Generating report '{report_name}'...")
            
        # Initialize report paths
        report_paths = {}
        
        # Generate reports in specified formats
        for format_name in self.formats:
            if format_name == "pdf":
                report_path = self._generate_pdf_report(results, report_name)
                report_paths["pdf"] = report_path
            else:
                if self.verbose:
                    print(f"  - Unsupported format: {format_name}")
                    
        # Store report results
        self.report_results = {
            "report_name": report_name,
            "generation_time": time.time(),
            "formats": report_paths
        }
        
        if self.verbose:
            print(f"Report '{report_name}' generated successfully")
            for format_name, path in report_paths.items():
                print(f"  - {format_name}: {path}")
                
        return report_paths
    
    def _generate_pdf_report(self, results: Dict[str, Any], report_name: str) -> str:
        """
        Generate PDF report using FPDF2.
        
        Args:
            results: Dictionary with results
            report_name: Name of the report
            
        Returns:
            Path to the generated report
        """
        # Create file path
        file_path = os.path.join(self.output_dir, f"{report_name}.pdf")
        
        # Create PDF with Unicode support
        pdf = FPDF()
        # Add a Unicode font
        pdf.add_page()
        
        # Set font to Unicode-compatible font
        pdf.set_font("Arial", "", 16)
        
        # Add title
        pdf.cell(0, 10, "HumanML Machine Learning Report", 0, 1, "C")
        pdf.ln(5)
        
        # Add generation date
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.ln(5)
        
        # Add session information
        pdf.set_font("Arial", "", 14)
        pdf.cell(0, 10, "Session Information", 0, 1)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Session ID: {results.get('session_id', 'N/A')}", 0, 1)
        pdf.cell(0, 10, f"Timestamp: {results.get('timestamp', 'N/A')}", 0, 1)
        pdf.cell(0, 10, f"Total Time: {results.get('total_time', 'N/A')} seconds", 0, 1)
        pdf.ln(5)
        
        # Add data information
        pdf.set_font("Arial", "", 14)
        pdf.cell(0, 10, "Data Information", 0, 1)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Number of Samples: {results.get('data', {}).get('n_samples', 'N/A')}", 0, 1)
        pdf.cell(0, 10, f"Number of Features: {results.get('data', {}).get('original', {}).get('n_features', 'N/A')}", 0, 1)
        pdf.cell(0, 10, f"Task Type: {results.get('data', {}).get('original', {}).get('task_type', 'N/A')}", 0, 1)

        # Add task-specific information
        if results.get('data', {}).get('original', {}).get('task_type') == 'classification':
            pdf.cell(0, 10, f"Number of Classes: {results.get('data', {}).get('original', {}).get('classification', {}).get('n_classes', 'N/A')}", 0, 1)
            
            # Add class distribution
            class_dist = results.get('data', {}).get('original', {}).get('classification', {}).get('class_distribution', {})
            if class_dist:
                pdf.cell(0, 10, "Class Distribution:", 0, 1)
                for class_name, count in class_dist.items():
                    pdf.cell(0, 10, f"  - {class_name}: {count}", 0, 1)
        elif results.get('data', {}).get('original', {}).get('task_type') == 'regression':
            regr_stats = results.get('data', {}).get('original', {}).get('regression', {})
            pdf.cell(0, 10, f"Target Range: [{regr_stats.get('target_min', 'N/A')}, {regr_stats.get('target_max', 'N/A')}]", 0, 1)
            pdf.cell(0, 10, f"Target Mean: {regr_stats.get('target_mean', 'N/A')}", 0, 1)
            pdf.cell(0, 10, f"Target Std: {regr_stats.get('target_std', 'N/A')}", 0, 1)
            
        pdf.ln(5)
        
        # Add models section if available
        if 'models' in results:
            pdf.set_font("Arial", "", 14)
            pdf.cell(0, 10, "Models", 0, 1)
            pdf.ln(2)
            
            # Add best model information
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, "Best Model", 0, 1)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 10)
            best_model_name = results.get('models', {}).get('best', {}).get('name', 'N/A')
            best_model_score = results.get('models', {}).get('best', {}).get('score', 'N/A')
            pdf.cell(0, 10, f"Name: {best_model_name}", 0, 1)
            pdf.cell(0, 10, f"Score: {best_model_score}", 0, 1)
            pdf.ln(5)
            
            # Add all models information
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, "All Models", 0, 1)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 10)
            trained_models = results.get('models', {}).get('trained', {}).get('models', {})
            if trained_models:
                for model_name, model_results in trained_models.items():
                    if isinstance(model_results, dict) and model_results.get('status') == 'success':
                        pdf.cell(0, 10, f"Model: {model_name}", 0, 1)
                        pdf.cell(0, 10, f"  - Status: {model_results.get('status', 'N/A')}", 0, 1)
                        pdf.cell(0, 10, f"  - Training Time: {model_results.get('training_time', 'N/A')} seconds", 0, 1)
                        pdf.cell(0, 10, f"  - CV Score: {model_results.get('cv_scores', {}).get('mean', 'N/A')}", 0, 1)
                        pdf.cell(0, 10, f"  - Validation Score: {model_results.get('validation_score', 'N/A')}", 0, 1)
                        pdf.ln(3)
                        
            pdf.ln(5)
            
        # Add evaluation section if available
        if 'evaluation' in results:
            pdf.set_font("Arial", "", 14)
            pdf.cell(0, 10, "Evaluation", 0, 1)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, "Best Model Evaluation", 0, 1)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 10)
            best_model_metrics = results.get('evaluation', {}).get('models', {}).get(best_model_name, {}).get('metrics', {})
            
            if results.get('data', {}).get('task_type') == 'classification':
                pdf.cell(0, 10, f"Accuracy: {best_model_metrics.get('accuracy', 'N/A')}", 0, 1)
                pdf.cell(0, 10, f"Precision: {best_model_metrics.get('precision', 'N/A')}", 0, 1)
                pdf.cell(0, 10, f"Recall: {best_model_metrics.get('recall', 'N/A')}", 0, 1)
                pdf.cell(0, 10, f"F1 Score: {best_model_metrics.get('f1', 'N/A')}", 0, 1)
            else:
                pdf.cell(0, 10, f"MSE: {best_model_metrics.get('mse', 'N/A')}", 0, 1)
                pdf.cell(0, 10, f"RMSE: {best_model_metrics.get('rmse', 'N/A')}", 0, 1)
                pdf.cell(0, 10, f"MAE: {best_model_metrics.get('mae', 'N/A')}", 0, 1)
                pdf.cell(0, 10, f"R²: {best_model_metrics.get('r2', 'N/A')}", 0, 1)
                
            pdf.ln(5)
            
        # Add feature importance section if available
        if 'explanation' in results and 'feature_importance' in results['explanation']:
            pdf.set_font("Arial", "", 14)
            pdf.cell(0, 10, "Feature Importance", 0, 1)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 10)
            feature_importance = results['explanation'].get('feature_importance', {}).get('model', [])
            if isinstance(feature_importance, list):
                for feature in feature_importance[:10]:  # Show top 10 features
                    if isinstance(feature, dict) and 'feature' in feature and 'importance' in feature:
                        pdf.cell(0, 10, f"{feature['feature']}: {feature['importance']}", 0, 1)
                        
            pdf.ln(5)
            
        # Add plots section if available
        if 'plots' in results.get('data', {}):
            pdf.set_font("Arial", "", 14)
            pdf.cell(0, 10, "Plots", 0, 1)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 10, "The following plots are available in the plots directory:", 0, 1)
            
            for plot_name, plot_path in results.get('data', {}).get('plots', {}).items():
                pdf.cell(0, 10, f"  - {plot_name}: {plot_path}", 0, 1)
                
            pdf.ln(5)
            
        # Add footer
        pdf.set_font("Arial", "", 8)
        pdf.cell(0, 10, f"Generated by HumanML v{results.get('library_version', '0.3.0')}", 0, 1, "C")
        pdf.cell(0, 10, f"© {datetime.datetime.now().year} HumanML", 0, 1, "C")
        
        # Save PDF
        pdf.output(file_path)
        
        return file_path
    
    def get_report_results(self) -> Dict[str, Any]:
        """
        Get report results.
        
        Returns:
            Dictionary with report results
        """
        return self.report_results
