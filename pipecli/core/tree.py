import fnmatch
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from collections import namedtuple
from .catalog import commands
from .root import Root


TreeElement = namedtuple('TreeElement', ['deepth', 'command', 'is_pointer'])


class Tree:
    def __init__(self, logger):
        self.root = Root()
        self.pointer = self.root
        self.logger = logger

    def _get_parent(self, command=None, parent=None):
        if command is None:
            command = self.pointer
        if parent is None:
            parent = self.root
        if command in parent.subcommands:
            return parent
        for subcommand in parent.subcommands:
            result = self._get_parent(command, subcommand)
            if result:
                return result
        if parent == self.root:
            self.logger.error('parent for command not found')

    def _get_command_by_name(self, name):
        for el in self.tree():
            if el.command.name == name:
                return el.command
        self.logger.error('command not found')

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
        self.logger.info('pushed')
        return True

    def pop(self, command=None):
        if command is None:
            command = self.pointer
        self.pointer = self._get_parent(command)
        if self.pointer is None:
            return False
        self.pointer.subcommands = [cmd for cmd in self.pointer.subcommands if cmd is not command]
        self.logger.info('poped')
        return True

    def goto(self, command):
        for el in self.tree():
            if el.command is command:
                self.pointer = command
                return True
        self.logger.error('command not found in tree')
        return False

    def reset(self, *args):
        self.root = Root()
        self.pointer = self.root
        self.logger.info('reseted')
        return True

    def rename(self, command=None, name=None):
        if type(command) is str and name is None:
            command, name = name, command
        if name is None:
            self.logger.error('new name required')
            return False
        if command is None:
            command = self.pointer
        command.name = name
        self.logger.info('renamed')
        return True

    def args(self, *args):
        command = self.pointer
        return command.update_args(args)

    def sources(self, *sources):
        command = self.pointer
        command.sources = set(sources)
        self.logger.info('sources changed')
        return True

    def flush(self, command=None):
        if command is None:
            command = self.pointer
        command.flush()
        self.logger.info('flushed')
        return True

    def load(self, path):
        exists = set(commands)
        # file
        if path.endswith('.py'):
            # get module info
            path = Path(path)
            if not path.exists():
                self.logger.error('file not found')
                return []
            module_name = path.stem
            full_path = path.absolute()
            # load module
            spec = spec_from_file_location(module_name, full_path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
        # module name
        else:
            try:
                import_module(path)
            except ImportError:
                self.logger.error('module not found')
                return []
        # return list of loaded commands
        loaded = set(commands) - exists
        if loaded:
            self.logger.info('loaded')
        else:
            self.logger.warning('loaded 0 commands')
        return sorted(list(loaded))

    def list(self, pattern=None):
        result = list(commands)
        if pattern:
            result = fnmatch.filter(names=result, pattern=pattern)
        if not result:
            self.logger.warning('no matches found')
        return sorted(result)

    def run(self):
        self.root.run()

    def pause(self):
        ...

    def stop(self):
        ...
