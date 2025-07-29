#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model Exporter Module for HumanML.

Provides functionality for exporting trained models to various formats
and saving them to disk.
"""

import os
import pickle
import json
import time
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from sklearn.base import BaseEstimator


class ModelExporter:
    """
    Export trained models to various formats and save them to disk.
    """
    
    def __init__(
        self,
        output_dir: str = "models",
        verbose: bool = True
    ):
        """
        Initialize the ModelExporter.
        
        Args:
            output_dir: Directory to save exported models
            verbose: Whether to print detailed information
        """
        self.output_dir = output_dir
        self.verbose = verbose
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize export results
        self.export_results = {}
        
    def export_model(
        self,
        model: BaseEstimator,
        model_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Export model to disk.
        
        Args:
            model: Model to export
            model_name: Name of the model
            metadata: Additional metadata to save with the model
            
        Returns:
            Path to the exported model
        """
        # Initialize export results
        self.export_results = {
            "model_name": model_name,
            "export_time": time.time(),
            "formats": {}
        }
        
        if self.verbose:
            print(f"Exporting model '{model_name}'...")
            
        # Export model to pickle format
        pickle_path = self._export_to_pickle(model_name, model)
        self.export_results["formats"]["pickle"] = pickle_path
        
        # Export metadata to JSON format
        if metadata:
            json_path = self._export_metadata_to_json(model_name, metadata)
            self.export_results["formats"]["json"] = json_path
            
        if self.verbose:
            print(f"Model '{model_name}' exported successfully")
            for format_name, path in self.export_results["formats"].items():
                print(f"  • {format_name}: {path}")
                
        return pickle_path
    
    def _export_to_pickle(self, model_name: str, model: BaseEstimator) -> str:
        """
        Export model to pickle format.
        
        Args:
            model_name: Name of the model
            model: Model to export
            
        Returns:
            Path to the exported model
        """
        # Create file path
        file_path = os.path.join(self.output_dir, f"{model_name}.pkl")
        
        # Save model to pickle file
        with open(file_path, "wb") as f:
            pickle.dump(model, f)
            
        return file_path
    
    def _export_metadata_to_json(self, model_name: str, metadata: Dict[str, Any]) -> str:
        """
        Export metadata to JSON format.
        
        Args:
            model_name: Name of the model
            metadata: Metadata to export
            
        Returns:
            Path to the exported metadata
        """
        # Create file path
        file_path = os.path.join(self.output_dir, f"{model_name}_metadata.json")
        
        # Save metadata to JSON file
        with open(file_path, "w") as f:
            json.dump(metadata, f, indent=2, default=str)
            
        return file_path
    
    def load_model(self, model_name: str) -> BaseEstimator:
        """
        Load model from disk.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Loaded model
        """
        # Create file path
        file_path = os.path.join(self.output_dir, f"{model_name}.pkl")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Model file not found: {file_path}")
            
        # Load model from pickle file
        with open(file_path, "rb") as f:
            model = pickle.load(f)
            
        if self.verbose:
            print(f"Model '{model_name}' loaded successfully")
            
        return model
    
    def load_metadata(self, model_name: str) -> Dict[str, Any]:
        """
        Load metadata from disk.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Loaded metadata
        """
        # Create file path
        file_path = os.path.join(self.output_dir, f"{model_name}_metadata.json")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Metadata file not found: {file_path}")
            
        # Load metadata from JSON file
        with open(file_path, "r") as f:
            metadata = json.load(f)
            
        if self.verbose:
            print(f"Metadata for model '{model_name}' loaded successfully")
            
        return metadata
    
    def get_export_results(self) -> Dict[str, Any]:
        """
        Get export results.
        
        Returns:
            Dictionary with export results
        """
        return self.export_results
