

class Command:
    name = None
    implement = None    # implemented protocols: http, grep, facebook...
    required = None     # required protocols into parents
    optional = None     # optional protocols into parents

    def __init__(self):
        self.subcommands = []
        self.args = {}
        if self.name is None:
            raise ValueError('name can not be None')
        if not self.implement:
            self.implement = set()
        self.sources = (self.required or set()) | (self.optional or set())
        self.parser = self.get_parser()

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
            # get message from parent
            input_message = yield
            if input_message is None:
                break
            source, input_message = input_message

            # propagate input_message to subcommands
            for subcommand in subcommands:
                self.propagate(source, subcommand, input_message)

            # check if message must be ignored
            if not self.check_source(source):
                continue

            # send message to current process
            output_message = process.send((source, input_message))

            # send messages from current process to subcommands
            while output_message is not None:
                for subcommand in subcommands:
                    subcommand.send((self, output_message))
                try:
                    output_message = process.send(None)
                except StopIteration:
                    break

        for output_message in self.finish():
            subcommand.send((self, output_message))

    @staticmethod
    def propagate(source, subcommand, input_message):
        subcommand.send((source, input_message))

    def check_source(self, source):
        # source implement any allowed protocol
        if source.implement & self.sources:
            return True
        # source name in allowed sources
        if source.name in self.sources:
            return True
        return False

    def process(self):
        yield

    def finish(self):
        return ()

    def update_args(self, args_string):
        args = self.parser.parse_args(args_string.split())[0]
        return self.args.update(dict(args._get_kwargs()))

    def describe(self):
        return dict(
            description=self.__doc__,
            args=self.parser.format_usage(),
        )

    @classmethod
    def new(cls):
        return cls()


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
