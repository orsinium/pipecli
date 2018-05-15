from itertools import chain


class Command:
    name = None
    implement = None

    require = ('root', )
    optional = ()

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
            if source not in chain(self.require, self.optional):
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


class Root(Command):
    name = 'root'
    implement = 'root'

    def entrypoint(self):
        for subcommand in self.subcommands:
            subcommand = subcommand.entrypoint()
            subcommand.send(None)
            subcommand.send((self.implement, 0))


class MakeInit(Command):
    name = 'init'
    implement = 'generator'

    def process(self):
        yield  # get init params
        for i in range(1, 4):
            yield i


class MakeDouble(Command):
    name = 'double'
    implement = 'number_operations'
    require = ('generator', )

    def process(self):
        while 1:
            src, x = yield
            print(src, x * 2)
            yield x * 2


class MakeStr(Command):
    name = 'to_str'
    implement = 'converting'
    require = ('generator', )

    def process(self):
        while 1:
            src, x = yield
            print(src, x)
            yield str(x)


if __name__ == '__main__':
    print('start')
    root = Root()
    test1 = MakeInit()
    test2 = MakeDouble()
    test3 = MakeStr()

    test2.subcommands.append(test3)
    test1.subcommands.append(test2)
    root.subcommands.append(test1)

    root.entrypoint()
    print('end')

    # start
    # number_operations 2
    # converting 2
    # number_operations 4
    # converting 4
    # number_operations 6
    # converting 6
    # end
