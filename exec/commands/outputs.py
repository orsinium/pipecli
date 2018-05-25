import sys
from exec import Command, commands


class BaseOutput(Command):
    sources = frozenset({'text'})

    def process(self, name=None):
        custom = self._file is None
        if custom:
            self._file = open(name, 'w')

        while 1:
            source, message = yield
            print(message, file=self._file)

        if custom:
            self._file.close()


@commands.register
class StdoutOutput(BaseOutput):
    name = 'output/stdout'
    _file = sys.stdout


@commands.register
class StderrOutput(BaseOutput):
    name = 'output/stderr'
    _file = sys.stderr


@commands.register
class FileOutput(BaseOutput):
    name = 'output/file'
    _file = None

    @staticmethod
    def get_parser(parser):
        parser.add_argument('--name', default='out.txt')
        return parser
