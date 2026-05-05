# Lab Generator

Generate complete, production-ready ML lab kits in seconds.

## Install

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Create a classification lab
python lab_generator.py create \
  --topic "Customer Churn Prediction" \
  --course machine_learning \
  --dataset telco_churn \
  --difficulty intermediate \
  --output ./labs/churn_lab

# Interactive wizard
python lab_generator.py interactive

# List all available templates and datasets
python lab_generator.py list --templates
python lab_generator.py list --datasets

# Validate a generated lab
python lab_generator.py validate ./labs/churn_lab
```

## Supported Courses & Topics

| Course | Generator | Example Topics |
|--------|-----------|----------------|
| `machine_learning` | Classification | Customer Churn, Fraud Detection |
| `machine_learning` | Regression | House Prices, Sales Forecasting |
| `deep_learning` | Deep Learning | MNIST, Custom Architectures |
| `nlp` | NLP | Sentiment Analysis, Text Classification |
| `computer_vision` | Computer Vision | CIFAR-10, Image Classification |
| `time_series` | Time Series | Demand Forecasting, Anomaly Detection |

## Difficulty Levels

| Level | Description | Hints | Starter Code | Min Accuracy |
|-------|-------------|-------|--------------|--------------|
| `beginner` | Step-by-step guidance | Detailed | 70% filled | 0.70 |
| `intermediate` | Some guidance | Moderate | 30% filled | 0.80 |
| `advanced` | Minimal hints | Minimal | Skeleton only | 0.85 |

## Generated Lab Structure

```
labs/my_lab/
├── assignment.ipynb          # Student notebook
├── reference_solution.ipynb  # Instructor solution
├── test_cases_public.py      # Visible tests
├── test_cases_hidden.py      # Grading tests
├── utils.py                  # Helper functions
├── metadata.json             # Lab configuration
├── data/
│   ├── train.csv
│   └── test.csv
└── README.md
```

## Adding New Generators

See [Developer Guide](docs/developer_guide.md).

## Running Tests

```bash
pytest tests/ -v
```
