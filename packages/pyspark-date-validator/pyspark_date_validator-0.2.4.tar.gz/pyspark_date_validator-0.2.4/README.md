# Date Validator PySpark
A PySpark utility for validating date completeness in tables.

## Installation
```bash
pip install pyspark-date-validator
```

## Example Usage
### Validating Multiple Tables with `MultipleTablesValidator`

Run checks across multiple tables and raise an error if any have missing dates.

```python
from date_validator import MultipleTablesValidator

# Define table configurations
table_configs = [
    {
        "table_name": "table1"
        , "start_date": "2023-01-01"
        , "end_date": "2023-01-05"
        , "frequency": "daily"
        , "custom_filter": "field_A = 10" # Optional
        , "exclude_date": ['2021-02-01','2021-02-02','2021-02-03'] # Optional
    },
    {
        "table_name": "table2"
        , "start_date": "2023-01-01"
        , "end_date": "2023-03-31"
        , "frequency": "monthly"
        , "custom_filter": "field_A = 10" # Optional
        , "exclude_date": ['2021-02-01','2021-02-02','2021-02-03'] # Optional
    }
]

# Run validation
validator = MultipleTablesValidator(table_configs)
validator.run_checks()
# Output:
# Missing dates in table 'table1' (daily):
# +----------+
# |  as_at_dt|
# +----------+
# |2023-01-02|
# |2023-01-04|
# |2023-01-05|
# +----------+
# Missing dates in table 'table2' (monthly):
# +----------+
# |  as_at_dt|
# +----------+
# |2023-02-28|
# +----------+
# ValueError: Missing dates detected in one or more tables.
```