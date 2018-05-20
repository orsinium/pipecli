
class Catalog:
    def __init__(self):
        self.commands = dict()

    def register(self, command, name=None):
        if not name:
            name = command.name
        if name in self.commands:
            raise KeyError('Command already registered')
        self.commands[name] = command
        return command


commands = Catalog()
