from functools import partial
from itertools import chain


class Command:
    implement = None        # implemented protocol: http, grep, facebook...
    required = ('root', )   # required protocols into parents
    optional = ()           # optional protocols into parents

    def __init__(self):
        self.subcommands = []

    def entrypoint(self):
        subcommands = []
        for subcommand in self.subcommands:
            # point to entrypoint
            subcommand = subcommand.entrypoint()
            # go to first yield
            subcommand.send(None)
            # save generator to list
            subcommands.append(subcommand)

        # get generator for proccess and go to first yield
        process = self.process()
        process.send(None)

        while 1:
            # get line from parent
            input_line = yield
            if input_line is None:
                break
            source, input_line = input_line

            # propagate input line to subprocesses
            for subcommand in subcommands:
                subcommand.send((source, input_line))

            # process input line into current process
            if source not in chain(self.required, self.optional):
                continue
            output_line = process.send((self.implement, input_line))

            # send line from current process to subprocesses
            while output_line is not None:
                for subcommand in subcommands:
                    subcommand.send((self.implement, output_line))
                try:
                    output_line = process.send(None)
                except StopIteration:
                    break

    def process(self):
        raise NotImplementedError


class Catalog:
    def __init__(self):
        self.commands = dict()

    def register(self, name, command=None):
        if not isinstance(name, str):
            raise ValueError('Command name required')
        if command:
            return self._register(name, command)
        else:
            return partial(self._register, command)

    def _register(self, name, command):
        if not isinstance(command, Command):
            raise ValueError('Command must be inherit from pipecli.Command')
        if name in self.commands:
            raise KeyError('Command already registered')
        self.commands[name] = command


commands = Catalog()
