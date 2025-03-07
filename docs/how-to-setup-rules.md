# Rules file setup

## What is this file for

This file is where the user can configure parameters for the decision-making
process of data classification.

Further down this file, you will find a few examples of these rules. This repo
comes with a pre-built set of rules, and there's also a `sample-rules.yaml`
file [here](../sample-rules.yaml).

Here's a list of operators that are defined within the system:

| Word              | Equivalent Operator   |
|-------------------|-----------------------|
| "exact"           | "=="                  |
| "equal"           | "=="                  |
| "equals"          | "=="                  |
| "greater"         | ">"                   |
| "less"            | "<"                   |
| "greater_equal"   | ">="                  |
| "less_equal"      | "<="                  |
| "not_equal"       | "!="                  |

## Classification rules reference &rarr; `rules.yaml`

This file should be placed at the root directory of the project.

Here are some examples of comparisons that are possible at the moment:


### Date

```yaml
rules:
  - id: "founding_age"
    name: "Company Founded in Last 5 Years"
    parameters:
      type: "date"
      operator: "less_equal"
      value: 5
      reference_date: "current_year"
      field: "Founded Year"
```

### Numeric

```yaml
  - id: "employee_count"
    name: "Exact Employee Count"
    parameters:
      type: "numeric"
      operator: "exact"
      value: 50
      field: "Total Employees"
  - id: "total_employees_range"
    name: "Range of employees"
    parameters:
      type: "numeric"
      operator: "range"
      min: 20
      max: 60
      field: "Total Employees"
```

### Delta

```yaml
  - id: "employee_growth_stability"
    name: "Employee growth stability"
    parameters:
      type: "delta"
      operator: "range"
      min: 0.0
      max: 0.10
      ref_unit: 1
      series:
        - field: "Employee Growth 2Y (%)"
          unit_span: 2
        - field: "Employee Growth 1Y (%)"
          unit_span: 1
        - field: "Employee Growth 6M (%)"
          unit_span: 0.5
```

### Percentage

```yaml
  - id: "min_usa_employees"
    name: "Minimum of employees in USA"
    parameters:
      type: "percentage"
      operator: "greater_equal"
      value: 0.75
      reference: "Total Employees"
      field: "Employee Locations"
      locator: "USA"
```
