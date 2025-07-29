# oa-utils

Statically typed Python utilities. 

## Pipeline

Fluent wrapper around a list.

```python
from oa_utils.pipeline import Pipeline

result = (Pipeline(range(10))
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * x)
            .sum()) # 120
```
