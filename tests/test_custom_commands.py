from pipecli import Command, Root


class MakeInit(Command):
    name = 'init'
    implement = {'generator'}
    sources = {'root'}

    def process(self):
        self.result = []
        yield  # get init params from root
        for i in range(1, 4):
            self.result.append(i)
            yield i


class MakeDouble(Command):
    name = 'double'
    implement = {'number_operations'}
    sources = {'generator'}

    def process(self):
        self.result = []
        while 1:
            src, x = yield
            self.result.append(x)
            yield x * 2


class MakeStr(Command):
    name = 'str'
    implement = {'converting'}
    sources = {'number_operations'}

    def process(self):
        self.result = []
        while 1:
            src, x = yield
            self.result.append(x)
            yield str(x)


def test_pipe():
    root = Root()
    test1 = MakeInit()
    test2 = MakeDouble()
    test3 = MakeStr()

    test2.subcommands.append(test3)
    test1.subcommands.append(test2)
    root.subcommands.append(test1)

    root.entrypoint()

    assert test1.result == [1, 2, 3]
    assert test2.result == [1, 2, 3]
    assert test3.result == [2, 4, 6]
