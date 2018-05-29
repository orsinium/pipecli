from functools import partial
from .catalog import catalog
from .root import Root


class TaskSet:
    def __init__(self, task):
        self.root = Root()      # left task in chain
        self.task = task        # second task in chain
        self.tail = task        # right task in chain

        self.tail.debug = True  # save results into task
        self.tail.results = []  # save results into task
        self.root.subtasks.append(self.tail)  # chain root and tail

        self.filters = []
        self.done = False

    @staticmethod
    def _check_name(name, task):
        return task.name == name

    def __or__(self, other):
        self.tail.subtasks.append(other.task)
        self.tail = other.task
        self.tail.debug = True  # save results into task
        self.tail.results = []  # save results into task
        self.done = False
        return self

    @classmethod
    def _chain(cls, task):
        yield task
        if task.subtasks:
            yield from cls._chain(task.subtasks[0])

    @property
    def chain(self):
        return self._chain(self.root)

    def filter(self, condition):
        if isinstance(condition, str):
            condition = partial(self._check_name, condition)
        self.filters.append(condition)
        return self

    def __iter__(self):
        if not self.done:
            self.run()
        for task in self.chain:
            for check in self.filters:
                if not check(task):
                    break
            else:
                yield from task.results

    def run(self):
        self.root.run()
        self.done = True
        return self

    def get(self):
        return tuple(self)

    def __str__(self):
        self.tail.name


def task(name, task_name=None, **kwargs):
    command = catalog.get(name)
    task = command()
    if task_name is not None:
        task.name = task_name
    task.args.update(kwargs)
    return TaskSet(task)


def chain(root_task, *other_tasks):
    for task in other_tasks:
        root_task.__or__(task)
    return root_task.get()
