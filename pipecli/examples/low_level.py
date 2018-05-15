from pipecli import Command, Root


class MakeInit(Command):
    implement = 'generator'

    def process(self):
        yield  # get init params from root
        for i in range(1, 4):
            yield i


class MakeDouble(Command):
    implement = 'number_operations'
    required = ('generator', )

    def process(self):
        while 1:
            src, x = yield
            print(src, x * 2)
            yield x * 2


class MakeStr(Command):
    implement = 'converting'
    required = ('generator', )

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
