# Customer Churn Prediction

**Course:** machine_learning
**Difficulty:** intermediate
**Total Points:** 90

## Learning Objectives

- Perform exploratory data analysis on a real-world dataset
- Preprocess tabular data for machine learning
- Train and evaluate a classification model
- Interpret classification metrics (accuracy, precision, recall, F1)
- Apply machine learning to solve: Customer Churn Prediction

## Getting Started

```bash
# Generate the dataset (one-time setup)
python ../../components/dataset_manager.py

# Open the lab notebook
jupyter lab assignment.ipynb
```

## Exercises

| Exercise | Points |
|----------|--------|
| Exercise 1: Data Exploration | 10 |
| Exercise 2: Data Preprocessing | 20 |
| Exercise 3: Build Model | 30 |
| Exercise 4: Model Evaluation | 30 |
| Bonus Exercise: Hyperparameter Tuning | 10 |
| **Total** | **100** |

## Submission

Run the last cell in `assignment.ipynb`. Your score appears in the portal within ~60 seconds.

## Dataset

Telco customer data with features: tenure_months, monthly_charges, num_products, support_calls, has_contract.
Target: `churned` (0 = stayed, 1 = left)

## How This Lab Was Generated

```bash
python lab_generator.py create \
  --topic "Customer Churn Prediction" \
  --course machine_learning \
  --dataset telco_churn \
  --difficulty intermediate \
  --output examples/sample_generated_lab
```
