from .command import Command
from .catalog import commands


@commands.register
class Root(Command):
    name = 'root'
    implement = {'root'}

    def entrypoint(self):
        for subcommand in self.subcommands:
            subcommand = subcommand.entrypoint()
            subcommand.send(None)
            subcommand.send((self, 0))

    def run(self):
        return self.entrypoint()
