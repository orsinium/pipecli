from collections import namedtuple
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
        ...

    def run(self):
        list(self.root.entrypoint())

    def pause(self):
        ...

    def stop(self):
        ...
