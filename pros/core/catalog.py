from .command import Command
from deal import pre


class Catalog(dict):

    @pre(lambda self, command, name=None: type(command) is type, 'command must be class, not instance')
    @pre(lambda self, command, name=None: Command in command.mro(), 'command must be pros.Command child')
    @pre(lambda self, command, name=None: not name or isinstance(name, str), 'name must be str')
    @pre(lambda self, command, name=None: (name or command.name) not in self, 'command already registered')
    def register(self, command, name=None):
        if not name:
            name = command.name
        self[name] = command
        return command


catalog = Catalog()
