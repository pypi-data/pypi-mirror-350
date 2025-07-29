# HumanML Library - User Guide

## Overview

HumanML is a human-centered machine learning library designed to simplify the machine learning workflow while providing professional results. The library automates data preprocessing, model selection, training, evaluation, and reporting, making machine learning accessible to users of all skill levels.

## Key Features

- **Simplified Workflow**: Complete machine learning pipeline in just a few lines of code
- **Intelligent Adaptivity**: Automatically adapts to your dataset characteristics
- **Reinforcement Learning Optimization**: Uses RL to find optimal hyperparameters
- **Professional Reports**: Generates comprehensive PDF reports
- **Interactive Visualizations**: Easily visualize model performance and insights
- **Human-Centered Design**: Clear, stepwise progress and intuitive interface

## Installation

```bash
pip install humanml
```

Or install from the source:

```bash
pip install -e .
```

## Quick Start

```python
from humanml import HumanML
import pandas as pd
from sklearn.datasets import load_iris

# Load data
data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Initialize HumanML
model = HumanML()

# Fit model
model.fit(X, y)

# Make predictions
predictions = model.predict(X)

# Visualize results
model.plot()
```

## Main Steps

HumanML follows a 5-step process:

1. **Data preprocessing and feature engineering**
2. **Model selection and hyperparameter tuning**
3. **Model training and evaluation**
4. **Model explanation and visualization**
5. **Report generation and model export**

## Key Methods

- `fit(X, y)`: Train models on your data
- `predict(X)`: Make predictions with the best model
- `predict_proba(X)`: Get probability predictions (classification only)
- `plot()`: Visualize model performance
- `get_results()`: Get detailed results dictionary
- `get_best_model()`: Get the best model and its name

## Configuration Options

When initializing HumanML, you can customize its behavior:

```python
model = HumanML(
    preference="speed",  # Options: "accuracy", "speed", "interpretability", "balanced"
    output_dir="humanml_output",  # Directory for outputs
    verbose=True,  # Whether to print detailed information
    random_state=42,  # Random seed for reproducibility
    n_jobs=-1,  # Number of parallel jobs (-1 for all cores)
    excluded_models=None,  # List of models to exclude
    included_models=None,  # List of models to include (overrides excluded_models)
    hyperparameter_tuning="auto",  # Options: "auto", "grid", "random", "bayesian", "rl", "none"
    cross_validation=5,  # Number of cross-validation folds
    test_size=0.2,  # Proportion of data for testing
    validation_size=0.1,  # Proportion of training data for validation
    auto_report=True,  # Whether to automatically generate reports
    report_formats=["pdf"]  # Report formats to generate
)
```

## Example: Classification

```python
from humanml import HumanML
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# Load data
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize HumanML
model = HumanML(preference="accuracy")

# Fit model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate model
from sklearn.metrics import accuracy_score
print(f"Accuracy: {accuracy_score(y_test, predictions)}")

# Visualize results
model.plot("confusion_matrix")
model.plot("roc_curve")
model.plot("feature_importance")
```

## Changelog

### Version 0.3.0
- Redesigned fit method to show only stepwise progress
- Integrated reinforcement learning for auto-parameter tuning
- Enhanced library adaptivity and smartness
- Changed report generation to PDF only
- Improved plot utilities for better visualization
- Added new plot() method for interactive visualization

### Version 0.2.0
- Added support for more models
- Improved preprocessing capabilities
- Enhanced report generation

### Version 0.1.0
- Initial release

## License

MIT License
