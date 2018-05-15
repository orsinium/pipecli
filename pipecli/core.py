

class Command:
    name = None

    implement = ()
    require = ()
    optional = ()

    def __init__(self):
        self.subcommands = []

    def entrypoint(self):
        names = [command.name for command in self.subcommands]
        subcommands = []
        for subcommand in self.subcommands:
            # point to entrypoint
            subcommand = subcommand.entrypoint()
            # go to first yield
            subcommand.send(None)
            # save generator to list
            subcommands.append(subcommand)

        process = self.process()
        process.send(None)

        while 1:
            input_line = yield
            if input_line is None:
                break

            output_line = process.send(input_line)
            while output_line is not None:
                for name, subcommand in zip(names, subcommands):
                    subcommand.send((name, output_line))
                try:
                    output_line = process.send(None)
                except StopIteration:
                    break

    def process(self):
        raise NotImplementedError


class Root(Command):
    name = 'root'

    def entrypoint(self):
        for subcommand in self.subcommands:
            subcommand = subcommand.entrypoint()
            subcommand.send(None)
            subcommand.send(0)


class MakeInit(Command):
    name = 'init'

    def process(self):
        yield  # get init params
        for i in range(1, 4):
            yield i


class MakeDouble(Command):
    name = 'double'

    def process(self):
        while 1:
            src, x = yield
            print(src, x * 2)
            yield x * 2


class MakeStr(Command):
    name = 'to_str'

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
    # double 2
    # to_str 2
    # double 4
    # to_str 4
    # double 6
    # to_str 6
    # end
