# mongoagg

<img src="mongoagg-logo.png" alt="MongoAgg banner" style="max-width: 100%; height: auto;">

A fluent builder for constructing MongoDB aggregation pipelines in Python.

## Features

- Fluent interface for building complex MongoDB aggregation pipelines
- Type-safe stage construction
- Comprehensive validation of pipeline stages
- Support for all major MongoDB aggregation stages:
  - `$match` and `$expr`
  - `$project` and field selection
  - `$sort` and ordering
  - `$limit` and `$skip`
  - `$unwind`
  - `$group`
  - `$lookup` (with support for both simple and pipeline-based joins)
  - `$facet`
  - `$addFields`
  - `$replaceRoot`
  - `$redact`
  - `$comment`

## Installation

```bash
pip install mongoagg
```

## Quick Start

```python
from mongoagg import AggBuilder, Expr

# Create a simple pipeline
pipeline = (
    AggBuilder()
    .match({"status": "active"})
    .project({"name": 1, "age": 1, "_id": 0})
    .sort({"age": 1})
    .limit(10)
    .build()
)

# Use with PyMongo
result = collection.aggregate(pipeline)
```

## Examples

### Basic Querying

```python
from mongoagg import AggBuilder, Expr

# Find active users and project specific fields
pipeline = (
    AggBuilder()
    .match({"status": "active"})
    .project({"name": 1, "email": 1, "_id": 0})
    .build()
)
```

### Joining Collections

```python
from mongoagg import AggBuilder, Expr

# Join with another collection using $lookup
pipeline = (
    AggBuilder()
    .match({"status": "active"})
    .lookup(
        from_="orders",
        local_field="userId",
        foreign_field="userId",
        as_="orders"
    )
    .build()
)
```

### Complex Pipeline with Multiple Stages

```python
from mongoagg import AggBuilder, Expr

# Complex pipeline with grouping and sorting
pipeline = (
    AggBuilder()
    .match({"status": "active"})
    .group(
        id_field="$department",
        total_salary=Expr.sum("$salary"),
        avg_salary=Expr.avg("$salary"),
        count=Expr.sum(1)
    )
    .sort({"total_salary": -1})
    .limit(5)
    .build()
)
```

### Using Expressions

```python
from mongoagg import AggBuilder, Expr

# Using $expr for complex conditions
pipeline = (
    AggBuilder()
    .expr(Expr.gt("$price", "$budget"))
    .project({"name": 1, "price": 1, "budget": 1})
    .build()
)

# Using conditional expressions
pipeline = (
    AggBuilder()
    .add_fields({
        "status": Expr.when(Expr.gt("$price", 100))
                     .then("expensive")
                     .otherwise("affordable")
    })
    .build()
)

# Using arithmetic expressions
pipeline = (
    AggBuilder()
    .add_fields({
        "total": Expr.add("$price", Expr.multiply("$tax", "$price")),
        "discounted_price": Expr.subtract("$price", Expr.multiply("$price", 0.1))
    })
    .build()
)
```

## API Reference

### Core Methods

- `match(query)`: Add a $match stage
- `project(fields)`: Add a $project stage
- `sort(fields)`: Add a $sort stage
- `limit(n)`: Add a $limit stage
- `skip(n)`: Add a $skip stage
- `unwind(path)`: Add a $unwind stage
- `group(id_field, **accumulators)`: Add a $group stage
- `lookup(from_, as_, local_field, foreign_field)`: Add a $lookup stage
- `facet(**pipelines)`: Add a $facet stage
- `add_fields(fields)`: Add an $addFields stage
- `replace_root(new_root)`: Add a $replaceRoot stage
- `redact(condition)`: Add a $redact stage
- `comment(text)`: Add a $comment stage

### Expression Methods (Expr class)

The `Expr` class provides static methods for building MongoDB expressions:

- Comparison: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in_`, `nin`
- Logical: `and_`, `or_`, `not_`
- Conditional: `cond`, `if_null`, `coalesce`
- Arithmetic: `add`, `subtract`, `multiply`, `divide`, `mod`, `pow`
- Aggregation: `sum`, `avg`, `min`, `max`, `push`, `add_to_set`
- Array: `array_elem_at`, `concat`, `filter`, `map`, `reduce`
- String: `concat`, `substr`, `to_lower`, `to_upper`, `strcasecmp`
- Date: `date_from_string`, `date_to_string`, `year`, `month`, `day_of_month`
- Type Conversion: `to_decimal`, `to_double`, `to_int`, `to_long`, `to_string`
- Math: `abs`, `ceil`, `floor`, `round`, `exp`, `ln`, `log10`, `sqrt`

### Utility Methods

- `build()`: Returns the final pipeline
- `to_json()`: Serializes the pipeline to JSON
- `print_pretty()`: Prints the pipeline in a formatted way

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
