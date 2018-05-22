from functools import partial
from inspect import getargspec

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
# from prompt_toolkit import print_formatted_text, HTML

from .core import Tree, commands


class Formatter:
    @staticmethod
    def success(text):
        return text
        # return HTML('<ansigreen>{}</ansigreen>'.format(text))

    @staticmethod
    def error(text):
        return text
        # return HTML('<ansired>{}</ansired>'.format(text))


class ProxyTree:
    def __init__(self):
        self._tree = Tree()

    def getter(self, name, *args):
        method = getattr(self._tree, name)
        if not args:
            return method(*args)

        argspec = getargspec(method).args
        if len(argspec) >= 2 and argspec[1] == 'command':
            command = self._tree._get_command_by_name(args[0])
            if command is None:
                return 'command not found'
            return method(command, *args[1:])

        result = method(*args)
        if type(result) is list:
            result = '\n'.join(result)
        return result

    def __getattr__(self, name):
        return partial(self.getter, name)

    def push(self, command_name):
        command = commands[command_name]
        return self._tree.push(command)

    def tree(self):
        tree = self._tree.tree()
        result = []
        for el in tree:
            line = ['-' * el.deepth * 2, el.command.name]
            if el.command.sources:
                line.extend(['[', ', '.join(sorted(el.command.sources)), ']'])
            if el.is_pointer:
                line.append(' <--- you are here')
            result.append(''.join(line))
        return '\n'.join(result)


ACTIONS = tuple(action for action in dir(Tree) if not action.startswith('_'))
COMMANDS = tuple(commands.keys())

tree = ProxyTree()
history = InMemoryHistory()
suggest = AutoSuggestFromHistory()
completer = WordCompleter(ACTIONS + COMMANDS)


def cli():
    while 1:
        try:
            text = prompt('> ', history=history, auto_suggest=suggest, completer=completer)
        except KeyboardInterrupt:
            print('Bye!')
            return
        if not text:
            continue
        action, *args = text.split()

        try:
            result = getattr(tree, action)(*args)
        except Exception as e:
            print(Formatter.error(e))
        else:
            print(result)


if __name__ == '__main__':
    cli()
