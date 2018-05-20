from .root import Root

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
