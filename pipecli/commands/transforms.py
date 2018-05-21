from ..core import Command, commands


@commands.register
class StrTransform(Command):
    """Transform any message to string.
    """
    name = 'transform/string'
    implements = frozenset({'text', 'string'})
    optional = frozenset({'integer'})

    def process(self):
        while 1:
            source, message = yield
            yield str(message)


@commands.register
class MultiplyTransform(Command):
    """Multiply integer numbers to n.
    """
    name = 'transform/multiply'
    implements = frozenset({'integer', 'number'})
    required = frozenset({'integer'})

    @staticmethod
    def get_parser(parser):
        parser.add_argument('--n', type=int, default=2)
        return parser

    def process(self, n):
        while 1:
            source, message = yield
            yield message * n
