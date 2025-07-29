#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Auto Logger Module for HumanML.

Provides comprehensive logging capabilities for tracking model training,
evaluation, and other operations.
"""

import os
import time
import json
import logging
import datetime
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from contextlib import contextmanager


class AutoLogger:
    """
    Comprehensive logger for tracking model training, evaluation, and other operations.
    """
    
    def __init__(
        self,
        logs_dir: str = "logs",
        verbose: bool = True,
        session_id: Optional[str] = None
    ):
        """
        Initialize the AutoLogger.
        
        Args:
            logs_dir: Directory for log files
            verbose: Whether to print detailed information
            session_id: Unique identifier for the session
        """
        self.logs_dir = logs_dir
        self.verbose = verbose
        self.session_id = session_id or datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create logs directory
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(f"humanml_{self.session_id}")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # Create file handler
        file_handler = logging.FileHandler(os.path.join(self.logs_dir, f"{self.session_id}.log"))
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.verbose else logging.WARNING)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Initialize metrics
        self.metrics = {}
        
        # Initialize step context
        self.current_step = None
        
        # Initialize step timers
        self.step_timers = {}
        
        # Log initialization
        self.log_info(f"Initialized AutoLogger with session ID: {self.session_id}")
        self.log_info(f"Logs directory: {self.logs_dir}")
        
    def log_info(self, message: str) -> None:
        """
        Log information message.
        
        Args:
            message: Message to log
        """
        self.logger.info(message)
        
    def log_warning(self, message: str) -> None:
        """
        Log warning message.
        
        Args:
            message: Message to log
        """
        self.logger.warning(message)
        
    def log_error(self, message: str) -> None:
        """
        Log error message.
        
        Args:
            message: Message to log
        """
        self.logger.error(message)
        
    def log_debug(self, message: str) -> None:
        """
        Log debug message.
        
        Args:
            message: Message to log
        """
        self.logger.debug(message)
        
    def log_metric(self, name: str, value: Union[float, int, str, bool]) -> None:
        """
        Log metric.
        
        Args:
            name: Metric name
            value: Metric value
        """
        # Store metric
        if name not in self.metrics:
            self.metrics[name] = []
            
        self.metrics[name].append({
            "value": value,
            "timestamp": time.time(),
            "step": self.current_step
        })
        
        # Log metric
        self.log_info(f"Metric: {name} = {value}")
        
    def log_metrics(self, metrics: Dict[str, Union[float, int, str, bool]]) -> None:
        """
        Log multiple metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        for name, value in metrics.items():
            self.log_metric(name, value)
            
    def log_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Log parameters.
        
        Args:
            parameters: Dictionary of parameters
        """
        # Log parameters
        self.log_info(f"Parameters: {json.dumps(parameters, default=str)}")
        
    def log_model(self, model_name: str, model_info: Dict[str, Any]) -> None:
        """
        Log model information.
        
        Args:
            model_name: Model name
            model_info: Model information
        """
        # Log model
        self.log_info(f"Model: {model_name} - {json.dumps(model_info, default=str)}")
        
    def log_artifact(self, artifact_name: str, artifact_path: str) -> None:
        """
        Log artifact.
        
        Args:
            artifact_name: Artifact name
            artifact_path: Artifact path
        """
        # Log artifact
        self.log_info(f"Artifact: {artifact_name} - {artifact_path}")
        
    def log_step_start(self, step_name: str) -> None:
        """
        Log step start.
        
        Args:
            step_name: Step name
        """
        # Store previous step
        previous_step = self.current_step
        
        # Set current step
        self.current_step = step_name
        
        # Start timer
        self.step_timers[step_name] = time.time()
        
        # Log step start
        self.log_info(f"Step '{step_name}' started")
        
    def log_step_end(self, step_name: str) -> None:
        """
        Log step end.
        
        Args:
            step_name: Step name
        """
        # Check if step exists
        if step_name not in self.step_timers:
            self.log_warning(f"Step '{step_name}' was not started")
            return
            
        # Calculate duration
        duration = time.time() - self.step_timers[step_name]
        
        # Log step end
        self.log_info(f"Step '{step_name}' completed in {duration:.2f} seconds")
        
        # Remove timer
        del self.step_timers[step_name]
        
    def get_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get metrics.
        
        Returns:
            Dictionary of metrics
        """
        return self.metrics
    
    @contextmanager
    def step_context(self, step_name: str) -> None:
        """
        Context manager for logging steps.
        
        Args:
            step_name: Step name
        """
        # Store previous step
        previous_step = self.current_step
        
        # Set current step
        self.current_step = step_name
        
        # Log step start
        self.log_info(f"Step '{step_name}' started")
        start_time = time.time()
        
        try:
            # Yield control
            yield
            
            # Log step end
            end_time = time.time()
            self.log_info(f"Step '{step_name}' completed in {end_time - start_time:.2f} seconds")
            
        except Exception as e:
            # Log step error
            end_time = time.time()
            self.log_error(f"Step '{step_name}' failed after {end_time - start_time:.2f} seconds: {str(e)}")
            
            # Re-raise exception
            raise
            
        finally:
            # Restore previous step
            self.current_step = previous_step


# Example Usage (for testing purposes)
if __name__ == "__main__":
    print("Running AutoLogger Example...")
    
    # Initialize logger
    logger = AutoLogger(
        logs_dir="logs",
        verbose=True
    )
    
    # Log information
    logger.log_info("This is an information message")
    logger.log_warning("This is a warning message")
    logger.log_error("This is an error message")
    logger.log_debug("This is a debug message")
    
    # Log metrics
    logger.log_metric("accuracy", 0.85)
    logger.log_metric("loss", 0.25)
    
    # Log multiple metrics
    logger.log_metrics({
        "precision": 0.82,
        "recall": 0.79,
        "f1": 0.80
    })
    
    # Log parameters
    logger.log_parameters({
        "learning_rate": 0.01,
        "batch_size": 32,
        "epochs": 10
    })
    
    # Log model
    logger.log_model("random_forest", {
        "n_estimators": 100,
        "max_depth": 10,
        "min_samples_split": 2
    })
    
    # Log artifact
    logger.log_artifact("model_weights", "models/random_forest.pkl")
    
    # Use step context
    with logger.step_context("data_preprocessing"):
        logger.log_info("Preprocessing data...")
        logger.log_metric("n_features", 10)
        time.sleep(1)  # Simulate work
        
    # Log step start/end directly
    logger.log_step_start("model_training")
    logger.log_info("Training model...")
    time.sleep(1)  # Simulate work
    logger.log_step_end("model_training")
    
    # Get metrics
    metrics = logger.get_metrics()
    print("\nMetrics:")
    for name, values in metrics.items():
        print(f"  • {name}: {values}")
    
    print("\nAutoLogger example completed successfully!")
