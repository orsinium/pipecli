import fnmatch
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from collections import namedtuple
from .catalog import commands
from .root import Root


TreeElement = namedtuple('TreeElement', ['deepth', 'command', 'is_pointer'])


class Tree:
    def __init__(self):
        self.root = Root()
        self.pointer = self.root

    def _get_parent(self, command=None, parent=None):
        if command is None:
            command = self.pointer
        if parent is None:
            parent = self.root
        if command == parent:
            return parent
        for subcommand in parent.subcommands:
            return self._get_parent(command, subcommand)

    def _get_command_by_name(self, name):
        for el in self.tree():
            if el.command.name == name:
                return el.command

    def tree(self, command=None):
        if command is None:
            command = self.root
        is_pointer = (command is self.pointer)
        result = [TreeElement(0, command, is_pointer)]
        for subcommand in command.subcommands:
            subtree = [el._replace(deepth=el.deepth + 1) for el in self.tree(subcommand)]
            result.extend(subtree)
        return result

    def push(self, command):
        command = command()
        self.pointer.subcommands.append(command)
        self.pointer = command

    def pop(self, command=None):
        if command is None:
            command = self.pointer
        self.pointer = self._get_parent(command)
        self.pointer.subcommands = [cmd for cmd in self.pointer.subcommands if cmd is not command]

    def goto(self, command):
        self.pointer = command

    def reset(self, *args):
        self.root = Root()
        self.pointer = self.root

    def rename(self, command=None, name=None):
        if type(command) is str and name is None:
            command, name = name, command
        if command is None:
            command = self.pointer
        command.name = name

    def args(self, *args):
        command = self.pointer
        command.update_args(args)

    def sources(self, *sources):
        command = self.pointer
        command.sources = set(sources)

    def flush(self, command=None):
        if command is None:
            command = self.pointer
        command.flush()

    def load(self, path):
        exists = set(commands)
        # file
        if path.endswith('.py'):
            # get module info
            path = Path(path)
            module_name = path.stem
            full_path = path.absolute()
            # load module
            spec = spec_from_file_location(module_name, full_path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
        # module name
        else:
            import_module(path)
        # return list of loaded commands
        loaded = set(commands) - exists
        return sorted(list(loaded))

    def list(self, pattern=None):
        result = list(commands)
        if pattern:
            result = fnmatch.filter(names=result, pattern=pattern)
        return sorted(result)

    def run(self):
        self.root.run()

    def pause(self):
        ...

    def stop(self):
        ...
