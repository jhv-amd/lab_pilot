
# Lab Generator Tool - AI-Powered Lab Kit Creation System

## Project Overview

Generate a complete **automated lab generator** that creates ML assignment lab kits in minutes instead of hours. The tool should take simple parameters (topic, dataset, difficulty) and generate production-ready Jupyter notebooks, tests, solutions, and documentation.

---

## What to Generate

Create a command-line tool called `lab_generator` that automatically creates complete, working lab kits for machine learning courses.

### Core Functionality

The tool should accept parameters like:
```bash
python lab_generator.py create \
  --topic "Image Classification with CNNs" \
  --course "computer_vision" \
  --dataset "cifar10" \
  --difficulty "intermediate" \
  --output "./labs/cnn_classification"
```

And generate a complete lab structure with:
- Assignment notebook with exercises
- Public tests (student-visible)
- Hidden tests (grading only)
- Reference solution
- Dataset preparation
- Documentation

---

## Directory Structure to Generate

```
lab_generator/
├── lab_generator.py              # Main CLI tool
├── templates/                     # Jinja2 templates for all components
│   ├── assignment_template.ipynb.j2
│   ├── test_public_template.py.j2
│   ├── test_hidden_template.py.j2
│   ├── solution_template.ipynb.j2
│   ├── metadata_template.json.j2
│   └── readme_template.md.j2
│
├── generators/                    # Topic-specific generators
│   ├── __init__.py
│   ├── base_generator.py         # Base class for all generators
│   ├── classification_generator.py
│   ├── regression_generator.py
│   ├── deep_learning_generator.py
│   ├── nlp_generator.py
│   ├── computer_vision_generator.py
│   └── time_series_generator.py
│
├── components/                    # Reusable components
│   ├── __init__.py
│   ├── exercise_library.py       # Library of standard exercises
│   ├── test_library.py           # Generic test functions
│   ├── dataset_manager.py        # Dataset downloading/preparation
│   └── rubric_generator.py       # Automatic rubric creation
│
├── datasets/                      # Dataset configurations
│   ├── tabular.yaml
│   ├── image.yaml
│   ├── text.yaml
│   └── timeseries.yaml
│
├── config/                        # Configuration
│   ├── course_templates.yaml     # Course-specific templates
│   └── difficulty_levels.yaml    # Difficulty configurations
│
├── utils/                         # Utilities
│   ├── __init__.py
│   ├── notebook_builder.py       # Jupyter notebook manipulation
│   ├── code_generator.py         # Python code generation
│   └── validation.py             # Validate generated labs
│
├── examples/                      # Example outputs
│   └── sample_generated_lab/
│
├── requirements.txt
├── setup.py
└── README.md
```

---

## Key Components to Implement

### 1. Main CLI Tool (lab_generator.py)

**Should support these commands:**

```bash
# Create a new lab
python lab_generator.py create \
  --topic "Sentiment Analysis with LSTM" \
  --course "nlp" \
  --dataset "imdb" \
  --difficulty "advanced" \
  --exercises "preprocessing,embedding,model,evaluation" \
  --output "./labs/sentiment_lstm"

# List available templates
python lab_generator.py list --templates

# List available datasets
python lab_generator.py list --datasets

# Validate a generated lab
python lab_generator.py validate ./labs/sentiment_lstm

# Interactive mode (wizard)
python lab_generator.py interactive
```

**CLI should:**
- Use `click` or `argparse` for argument parsing
- Support both command-line arguments and interactive wizard mode
- Validate all inputs before generation
- Show progress bars during generation
- Display summary of what was created

---

### 2. Base Generator Class (generators/base_generator.py)

All topic-specific generators inherit from this base class.

**Key methods:**
```python
class BaseLabGenerator:
    def __init__(self, topic, dataset, difficulty, output_dir):
        """Initialize generator with parameters"""
        
    def generate_assignment(self) -> str:
        """Generate assignment.ipynb notebook"""
        
    def generate_public_tests(self) -> str:
        """Generate test_cases_public.py"""
        
    def generate_hidden_tests(self) -> str:
        """Generate test_cases_hidden.py"""
        
    def generate_solution(self) -> str:
        """Generate reference_solution.ipynb"""
        
    def prepare_dataset(self) -> None:
        """Download/prepare dataset"""
        
    def generate_metadata(self) -> dict:
        """Generate metadata.json"""
        
    def generate_readme(self) -> str:
        """Generate README.md"""
        
    def generate_all(self) -> None:
        """Generate complete lab kit"""
```

---

### 3. Exercise Library (components/exercise_library.py)

**Provides reusable exercise templates:**

```python
class ExerciseLibrary:
    """Library of standard ML exercises that can be customized"""
    
    @staticmethod
    def data_exploration(dataset_type: str, difficulty: str) -> dict:
        """
        Returns exercise specification for data exploration
        
        Returns:
            {
                'title': 'Exercise 1: Data Exploration',
                'points': 10,
                'instructions': '...',
                'starter_code': '...',
                'solution_code': '...',
                'public_tests': [...],
                'hidden_tests': [...]
            }
        """
        
    @staticmethod
    def preprocessing(dataset_type: str, difficulty: str) -> dict:
        """Preprocessing exercise (scaling, encoding, etc.)"""
        
    @staticmethod
    def model_building(model_type: str, difficulty: str) -> dict:
        """Model building exercise"""
        
    @staticmethod
    def model_evaluation(task_type: str, difficulty: str) -> dict:
        """Model evaluation exercise"""
        
    @staticmethod
    def hyperparameter_tuning(model_type: str, difficulty: str) -> dict:
        """Hyperparameter tuning exercise (bonus)"""
```

**Exercise structure:**
- Each exercise returns a complete specification
- Includes TODO markers for students
- Has starter code and solution code
- Includes both public and hidden tests
- Adapts based on difficulty level

---

### 4. Test Library (components/test_library.py)

**Generic test functions that work for any ML task:**

```python
class TestLibrary:
    """Reusable test functions for ML assignments"""
    
    @staticmethod
    def test_function_exists(function_name: str) -> str:
        """Generate test to check if function exists"""
        return f'''
def test_{function_name}_exists():
    assert '{function_name}' in dir(), "Function {function_name} not found"
    assert callable({function_name}), "{function_name} is not callable"
'''
    
    @staticmethod
    def test_return_type(function_name: str, expected_type: str) -> str:
        """Generate test for return type"""
        
    @staticmethod
    def test_model_accuracy(min_accuracy: float, task: str) -> str:
        """Generate test for model performance"""
        
    @staticmethod
    def test_no_data_leakage() -> str:
        """Generate test for data leakage detection"""
        
    @staticmethod
    def test_no_overfitting(max_gap: float = 0.1) -> str:
        """Generate test for overfitting detection"""
```

---

### 5. Notebook Builder (utils/notebook_builder.py)

**Programmatically create Jupyter notebooks:**

```python
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

class NotebookBuilder:
    """Build Jupyter notebooks programmatically"""
    
    def __init__(self):
        self.cells = []
        
    def add_title(self, title: str, description: str) -> 'NotebookBuilder':
        """Add title and description"""
        
    def add_exercise(self, exercise_spec: dict) -> 'NotebookBuilder':
        """
        Add an exercise with:
        - Instructions (markdown)
        - Starter code with TODO markers (code cell)
        - Test cell (code cell)
        """
        
    def add_setup_cell(self, imports: list, data_loading: str) -> 'NotebookBuilder':
        """Add setup cell with imports and data loading"""
        
    def add_submission_cell(self, assignment_id: str) -> 'NotebookBuilder':
        """Add final submission cell"""
        
    def build(self, output_path: str) -> None:
        """Save notebook to file"""
        nb = new_notebook(cells=self.cells)
        with open(output_path, 'w') as f:
            nbformat.write(nb, f)
```

---

### 6. Topic-Specific Generators

Each generator customizes the base generator for a specific ML domain:

#### Classification Generator (generators/classification_generator.py)

```python
class ClassificationGenerator(BaseLabGenerator):
    """Generate classification labs"""
    
    def __init__(self, topic, dataset, difficulty, output_dir):
        super().__init__(topic, dataset, difficulty, output_dir)
        self.task_type = 'classification'
        
    def get_exercises(self) -> list:
        """Return exercises specific to classification"""
        return [
            ExerciseLibrary.data_exploration('tabular', self.difficulty),
            ExerciseLibrary.preprocessing('classification', self.difficulty),
            self.build_classification_model(),
            self.evaluate_classification_model(),
            ExerciseLibrary.hyperparameter_tuning('classifier', self.difficulty)
        ]
    
    def build_classification_model(self) -> dict:
        """Custom exercise for building classifier"""
        return {
            'title': 'Exercise 3: Build Classification Model',
            'points': 30,
            'instructions': f'''
Train a classification model for {self.topic}.

Requirements:
- Use scikit-learn or similar
- Implement proper train/validation split
- Track training metrics
''',
            'starter_code': '''
def train_classifier(X_train, y_train):
    """
    Train a classification model
    
    Args:
        X_train: Training features
        y_train: Training labels
    
    Returns:
        Trained model
    """
    ### START CODE HERE ###
    model = None  # TODO: Initialize your model
    # TODO: Train the model
    ### END CODE HERE ###
    
    return model
''',
            'solution_code': '''
from sklearn.ensemble import RandomForestClassifier

def train_classifier(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model
''',
            'public_tests': [
                TestLibrary.test_function_exists('train_classifier'),
                TestLibrary.test_return_type('train_classifier', 'model')
            ],
            'hidden_tests': [
                TestLibrary.test_model_accuracy(0.75, 'classification'),
                TestLibrary.test_no_overfitting()
            ]
        }
```

**Similar generators for:**
- `RegressionGenerator`
- `DeepLearningGenerator` (CNNs, RNNs, Transformers)
- `NLPGenerator` (text classification, sentiment analysis, etc.)
- `ComputerVisionGenerator` (image classification, object detection, etc.)
- `TimeSeriesGenerator` (forecasting, anomaly detection)

---

### 7. Dataset Manager (components/dataset_manager.py)

**Automatically handle dataset preparation:**

```python
class DatasetManager:
    """Manage dataset downloading and preparation"""
    
    DATASETS = {
        'cifar10': {
            'source': 'tensorflow.keras.datasets',
            'type': 'image',
            'classes': 10,
            'size': (32, 32, 3)
        },
        'imdb': {
            'source': 'tensorflow.keras.datasets',
            'type': 'text',
            'classes': 2
        },
        'titanic': {
            'source': 'seaborn',
            'type': 'tabular',
            'target': 'survived'
        },
        # ... more datasets
    }
    
    @staticmethod
    def prepare_dataset(dataset_name: str, output_dir: str) -> dict:
        """
        Download and prepare dataset
        
        Returns:
            {
                'train_path': 'data/train.csv',
                'test_path': 'data/test.csv',
                'description': '...',
                'features': [...],
                'target': 'label'
            }
        """
        
    @staticmethod
    def generate_data_loading_code(dataset_name: str) -> str:
        """Generate code to load this dataset"""
```

---

### 8. Template System (templates/)

**Use Jinja2 templates for all generated files:**

#### assignment_template.ipynb.j2
```python
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# {{ topic }}\n",
    "\n",
    "{{ description }}\n",
    "\n",
    "**Learning Objectives:**\n",
    "{% for objective in learning_objectives %}\n",
    "- {{ objective }}\n",
    "{% endfor %}\n",
    "\n",
    "**Grading:** {{ total_points }} points total\n",
    "{% for exercise in exercises %}\n",
    "- {{ exercise.title }}: {{ exercise.points }} points\n",
    "{% endfor %}"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Setup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "{{ setup_code }}"
   ]
  },
  {% for exercise in exercises %}
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## {{ exercise.title }}\n",
    "\n",
    "{{ exercise.instructions }}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "{{ exercise.starter_code }}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Test your solution\n",
    "from test_cases_public import test_{{ exercise.function_name }}\n",
    "test_{{ exercise.function_name }}({{ exercise.function_name }})"
   ]
  },
  {% endfor %}
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Submit Your Work"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "from core.submission import lab_submit\n",
    "lab_submit.submit_assignment('{{ assignment_id }}', 'assignment.ipynb')"
   ]
  }
 ]
}
```

---

## Example Usage

### Generate a Classification Lab
```bash
python lab_generator.py create \
  --topic "Customer Churn Prediction" \
  --course "machine_learning" \
  --dataset "telco_churn" \
  --difficulty "intermediate" \
  --output "./labs/churn_classification"

# Output:
# ✓ Created assignment.ipynb (5 exercises)
# ✓ Created test_cases_public.py (15 tests)
# ✓ Created test_cases_hidden.py (25 tests)
# ✓ Created reference_solution.ipynb
# ✓ Downloaded dataset to data/
# ✓ Created metadata.json
# ✓ Created README.md
# 
# Lab ready at: ./labs/churn_classification
# Time taken: 2.3 seconds
```

### Interactive Mode
```bash
python lab_generator.py interactive

# Wizard:
# ? Select course: [Computer Vision / NLP / Machine Learning]
# ? Select topic: [Image Classification / Object Detection / ...]
# ? Select dataset: [CIFAR-10 / ImageNet / COCO / ...]
# ? Difficulty level: [Beginner / Intermediate / Advanced]
# ? Include bonus exercise? [Yes / No]
# ? Output directory: ./labs/my_lab
#
# Generating lab... ✓
```

---

## Configuration Files

### course_templates.yaml
```yaml
computer_vision:
  default_exercises:
    - data_exploration
    - image_preprocessing
    - cnn_model
    - evaluation
    - transfer_learning
  
  common_imports:
    - "import tensorflow as tf"
    - "from tensorflow import keras"
    - "import cv2"
    - "import numpy as np"
    
  difficulty_levels:
    beginner:
      model_types: ["simple_cnn"]
      min_accuracy: 0.70
    intermediate:
      model_types: ["cnn", "resnet"]
      min_accuracy: 0.80
    advanced:
      model_types: ["efficientnet", "vision_transformer"]
      min_accuracy: 0.85

nlp:
  default_exercises:
    - text_exploration
    - tokenization
    - embedding
    - model_training
    - evaluation
  
  common_imports:
    - "import tensorflow as tf"
    - "from transformers import *"
    - "import nltk"
```

---

## Validation System

The tool should include validation to ensure generated labs are correct:

```python
class LabValidator:
    """Validate generated lab kits"""
    
    def validate_lab(self, lab_dir: str) -> dict:
        """
        Validate a generated lab
        
        Checks:
        - All required files exist
        - Notebooks are valid JSON
        - Tests can be imported and run
        - Dataset files exist
        - No syntax errors in code
        
        Returns:
            {
                'valid': True/False,
                'errors': [...],
                'warnings': [...]
            }
        """
```

---

## Advanced Features

### 1. Multi-Exercise Generation
Allow specifying which exercises to include:
```bash
python lab_generator.py create \
  --exercises "exploration,preprocessing,model,evaluation" \
  # Skip hyperparameter tuning
```

### 2. Custom Exercise Addition
Support adding custom exercises:
```bash
python lab_generator.py add-exercise \
  --lab ./labs/my_lab \
  --exercise custom_exercise.yaml
```

### 3. Difficulty Scaling
Automatically adjust:
- Hint levels in instructions
- Starter code completeness
- Test case strictness
- Required performance thresholds

### 4. Dataset Synthesis
Generate synthetic datasets when real ones aren't available:
```python
python lab_generator.py create \
  --topic "Binary Classification" \
  --dataset "synthetic" \
  --features 10 \
  --samples 1000
```

---

## Testing Requirements

Include comprehensive tests:

```
tests/
├── test_generators.py          # Test each generator
├── test_exercise_library.py    # Test exercise generation
├── test_notebook_builder.py    # Test notebook creation
├── test_validation.py          # Test validation system
└── integration/
    └── test_full_generation.py # End-to-end test
```

---

## Success Criteria

The generated tool should:

1. ✅ Generate complete, working lab in < 5 seconds
2. ✅ Support at least 5 different ML topics
3. ✅ Handle 10+ different datasets
4. ✅ Produce valid Jupyter notebooks
5. ✅ Include comprehensive tests (public + hidden)
6. ✅ Generate readable, well-documented code
7. ✅ Support 3 difficulty levels
8. ✅ Validate generated labs automatically
9. ✅ Provide clear CLI interface
10. ✅ Include complete documentation

---

## Documentation Requirements

Generate:
- README.md with usage examples
- API documentation for all classes
- Tutorial: "Creating Your First Lab"
- Developer guide for adding new generators
- Examples directory with sample outputs

---

## Output Quality

Generated labs must:
- Have clear, pedagogical instructions
- Include helpful hints at appropriate difficulty
- Use consistent code style (PEP 8)
- Have meaningful variable names
- Include complete docstrings
- Provide useful error messages in tests

---

## Example Generated Assignment Structure

```
labs/customer_churn_classification/
├── assignment.ipynb              # Student notebook
├── reference_solution.ipynb      # Instructor solution
├── test_cases_public.py         # 15 public tests
├── test_cases_hidden.py         # 25 hidden tests
├── data/
│   ├── train.csv
│   ├── test.csv
│   └── README.md
├── utils.py                      # Helper functions
├── metadata.json                 # Lab configuration
└── README.md                     # Lab documentation
```
