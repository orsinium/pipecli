# API usage

```python
from pros import task, Loader

Loader.load_all()
taskset = task('generate/integers', stop=10) | task('transform/multiply', multiplier=2)
for message in taskset.filter('transform/multiply'):
    print(message)
```

Output: 2, 4, 6... 20.

* task(...)
    * `name` -- name of command
    * `task_name` -- name for task. Same as `name` by default.
    * `**kwargs` -- args for task
* TaskSet:
    * `filter(condition)` -- filter results by name or lambda expression
    * `run()` -- run taskset.
    * `get()` -- run taskset and return list of results
    * `__iter__()` -- iterate by results.
