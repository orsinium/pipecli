from argparse import ArgumentParser


class Command:
    name = None
    implement = frozenset()     # implemented protocols: http, grep, facebook...
    required = frozenset()      # required protocols into parents
    optional = frozenset()      # optional protocols into parents

    def __init__(self, debug=False):
        self.flush()
        self.debug = debug
        if debug:
            self.results = []

    def flush(self):
        self.subcommands = []
        self.args = {}
        if self.__class__.name is None:
            raise ValueError('name can not be None')
        self.name = self.__class__.name
        self.sources = self.required | self.optional
        self.parser = self.get_parser(ArgumentParser())
        self.update_args([])    # set default args

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
        process = self.process(**self.args)
        process.send(None)

        while 1:
            # get message from parent
            input_message = yield
            if input_message is None:
                break
            source, input_message = input_message
            assert input_message is not None, "message can not be None"

            # propagate input_message to subcommands
            for subcommand in subcommands:
                if self.filter_propagation(source, input_message):
                    subcommand.send((source, input_message))

            # check if message must be ignored
            if not self.filter_processing(source, input_message):
                continue

            # send message to current process
            output_message = process.send((source, input_message))

            # send messages from current process to subcommands
            while output_message is not None:
                if self.debug:
                    self.results.append(output_message)
                for subcommand in subcommands:
                    subcommand.send((self, output_message))
                try:
                    output_message = process.send(None)
                except StopIteration:
                    break

        for output_message in self.finish():
            subcommand.send((self, output_message))

    @staticmethod
    def get_parser(parser):
        return parser

    def filter_propagation(self, source, input_message):
        return True

    def filter_processing(self, source, input_message):
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

    def update_args(self, args):
        args, _argv = self.parser.parse_known_args(args)
        return self.args.update(dict(args._get_kwargs()))

    def describe(self):
        return dict(
            description=self.__doc__,
            args=self.parser.format_usage(),
        )
