from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
# from prompt_toolkit import print_formatted_text, HTML

from .core import Tree


class Formatter:
    @staticmethod
    def success(text):
        return text
        # return HTML('<ansigreen>{}</ansigreen>'.format(text))

    @staticmethod
    def error(text):
        return text
        # return HTML('<ansired>{}</ansired>'.format(text))


ACTIONS = ('push', 'pop', 'rebase', 'set')
COMMANDS = tuple(commands.commands.keys())

tree = Tree()
history = InMemoryHistory()
suggest = AutoSuggestFromHistory()
completer = WordCompleter(ACTIONS + COMMANDS)


def cli():
    while 1:
        text = prompt('> ', history=history, auto_suggest=suggest, completer=completer)
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
