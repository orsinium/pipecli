from exec.core.taskset import task, TaskSet


def test_task():
    taskset = task('generate/integers', stop=10)
    assert isinstance(taskset, TaskSet)


def test_taskset():
    taskset = task('generate/integers', stop=10) | task('transform/multiply', multiplier=2)
    result = list(taskset.filter('transform/multiply'))
    assert taskset.tail.results == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    assert result == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
