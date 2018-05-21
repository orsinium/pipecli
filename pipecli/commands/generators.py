from ..core import Command, commands


@commands.register
class IntegersGenerator(Command):
    """Return sequence of integers from start (inclusive) to stop (inclusive) by step.
    """
    name = 'generate/integers'
    implement = frozenset({'integer', 'number'})
    sources = frozenset({'root'})

    @staticmethod
    def get_parser(parser):
        parser.add_argument('--start', type=int, default=1)
        parser.add_argument('--stop', type=int)
        parser.add_argument('--step', type=int, default=1, help='can be negative')
        return parser

    def process(self, start, stop, step):
        yield
        yield from range(start, stop + 1, step)
