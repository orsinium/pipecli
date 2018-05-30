from exec.core.taskset import task, TaskSet
from exec.commands.generators import IntegersGenerator


def test_task():
    taskset = task('generate/integers', stop=10)
    assert isinstance(taskset, TaskSet)
    assert isinstance(taskset.head, IntegersGenerator)

    taskset = task(IntegersGenerator, stop=10)
    assert isinstance(taskset, TaskSet)
    assert isinstance(taskset.head, IntegersGenerator)


def test_taskset_result():
    taskset = task('generate/integers', stop=5) | task('transform/multiply', multiplier=2)
    result = list(taskset.result.filter())
    assert taskset.tail.results == [2, 4, 6, 8, 10]
    assert result == [2, 4, 6, 8, 10]
