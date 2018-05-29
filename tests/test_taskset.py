from exec import task, Loader

Loader.load_all()

def test_taskset():
    taskset = task('generate/integers', stop=10) | task('transform/multiply', multiplier=2)
    result = list(taskset.filter('reduce/sum'))
    assert result == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
