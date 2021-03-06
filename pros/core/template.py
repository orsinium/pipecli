# built-in
import os
from collections import OrderedDict, defaultdict
from pathlib import Path

# external
import yaml
from jinja2 import Environment

# project
from .catalog import catalog
from .loader import Loader
from .root import Root


TEMPLATE_NAME = 'template.yml'
CONFIG_NAME = 'config.yml'
CONFIG_CONTENT = '# This file must be ignored into your VCS. Place your local setings here.\n'
DEFAULTS_NAME = 'defaults.yml'
DEFAULTS_CONTENT = '# This file contains default vars for template.\n'


# https://pyyaml.org/wiki/PyYAMLDocumentation
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


# https://gist.github.com/oglops/c70fb69eef42d40bed06
Dumper.add_representer(OrderedDict, lambda dumper, data: dumper.represent_dict(data.items()))


class Template:
    version = 1

    def __init__(self, struct):
        self.struct = struct

    @classmethod
    def _iterate_tasks(cls, task):
        for subtask in task.subtasks:
            yield task, subtask
            yield from cls._iterate_tasks(subtask)

    @classmethod
    def from_task(cls, root):
        tasks = []
        includes = set()
        for parent, task in cls._iterate_tasks(root):
            module_name = task.__class__.__module__
            includes.add(module_name)
            args = OrderedDict(sorted(task.args.items()))
            tasks.append(OrderedDict((
                ('name', task.name),
                ('parent', parent.name),
                ('command', task.__class__.name),
                ('sources', sorted(task.sources)),
                ('args', args),
            )))
        return cls(OrderedDict((
            ('version', cls.version),
            ('tasks', tasks),
            ('include', sorted(list(includes))),
        )))

    @staticmethod
    def _get_env(path):
        # defaults
        config_path = path / DEFAULTS_NAME
        with config_path.open() as f:
            env = yaml.load(f.read()) or dict()

        # config
        config_path = path / CONFIG_NAME
        if config_path.exists():
            with config_path.open() as f:
                env.update(yaml.load(f.read()) or dict())

        # env
        env.update(dict(os.environ))
        return env

    @classmethod
    def from_file(cls, path):
        if not isinstance(path, Path):
            path = Path(path)

        # read template
        template_path = path / TEMPLATE_NAME
        with template_path.open() as f:
            document = f.read()

        # render yaml
        template = Environment().from_string(document)
        env = cls._get_env(path)
        document = template.render(**env)

        # read yaml
        struct = yaml.load(document)
        return Template(struct)

    def to_task(self):
        # load modules
        for module_name in self.struct['include']:
            Loader.load_module(module_name)

        tasks = {'root': Root()}
        childs = defaultdict(list)

        # make tasks
        for task_info in self.struct['tasks']:
            command = catalog.get(task_info['command'])
            task = command()
            task.name = task_info['name']
            task.args = task_info['args']
            task.sources = frozenset(task_info['sources'])

            tasks[task.name] = task
            childs[task_info['parent']].append(task)

        # make tree
        for parent, subtasks in childs.items():
            for subtask in subtasks:
                tasks[parent].add(subtask)

        return tasks['root']

    def to_file(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        if not path.exists():
            path.mkdir()
        if path.is_file():
            raise FileExistsError('path must be directory, not file')

        # write template
        document = yaml.dump(self.struct, default_flow_style=False)
        template_path = path / TEMPLATE_NAME
        with template_path.open('w') as f:
            f.write(document)

        # write config
        config_path = path / DEFAULTS_NAME
        if not config_path.exists():
            with config_path.open('w') as f:
                f.write(DEFAULTS_CONTENT)
        config_path = path / CONFIG_NAME
        if not config_path.exists():
            with config_path.open('w') as f:
                f.write(CONFIG_CONTENT)
