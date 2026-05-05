# Dataset: Telco Customer Churn

Generate this data by running:

```bash
# From the lab_generator root
python -c "
from components.dataset_manager import DatasetManager
DatasetManager.prepare_dataset('telco_churn', 'examples/sample_generated_lab')
"
```

Or generate it automatically:
```bash
python lab_generator.py create --topic 'Customer Churn Prediction' \
  --course machine_learning --dataset telco_churn \
  --difficulty intermediate --output examples/sample_generated_lab
```

## Columns

| Column | Type | Description |
|--------|------|-------------|
| customer_id | str | Unique ID |
| age | int | Customer age |
| tenure_months | int | Months as customer |
| monthly_charges | float | Monthly bill |
| total_charges | float | Lifetime charges |
| num_products | int | Number of products |
| support_calls | int | Support calls (last year) |
| has_contract | int | 1=has contract |
| payment_method | str | Payment type |
| churned | int | **Target**: 1=churned |
