from ..core import Command, commands


@commands.register('root')
class Root(Command):
    name = 'root'
    implement = 'root'

    def entrypoint(self):
        for subcommand in self.subcommands:
            subcommand = subcommand.entrypoint()
            subcommand.send(None)
            subcommand.send((self.implement, 0))