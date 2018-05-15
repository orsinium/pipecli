from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
#from prompt_toolkit import print_formatted_text, HTML

from .commands.root import Root


class Formatter:
    @staticmethod
    def success(text):
        return text
        #return HTML('<ansigreen>{}</ansigreen>'.format(text))


class Tree:
    def __init__(self):
        self.root = Root()
        self.pointer = self.root

    def get_parent(self, command=None):
        if not command:
            command = self.pointer
        pass

    def get_name(self, command=None):
        if not command:
            command = self.pointer
        pass

    def get_tree(self):
        pass

    def push(self, command):
        pass
        return Formatter.success('Pushed!')

    def pop(self):
        pass

    def rebase(self, command):
        pass

    def set(self, *args):
        pass


tree = Tree()
history = InMemoryHistory()


def cli():
    while 1:
        text = prompt('> ', history=history, auto_suggest=AutoSuggestFromHistory())
        action, *args = text.split()
        result = getattr(tree, action)(*args)
        print(result)


if __name__ == '__main__':
    cli()
