from hashlib import md5
from exec import Command, commands


class Basehasher(Command):
    implement = frozenset({'binary', 'text'})
    sources = frozenset({'text'})

    def process(self, **kwargs):
        while 1:
            source, message = yield
            hasher = self.hasher(message)
            if kwargs['hex']:
                yield hasher.hexdigest()
            else:
                yield hasher.digest()

    @staticmethod
    def get_parser(parser):
        parser.add_argument('--hex', action='store_true', default=False, help='return hex digest instead of binary')
        return parser


@commands.register
class MD5Hasher(Basehasher):
    """Hash text by MD5 algorithm
    """
    name = 'hash/md5'
    hasher = md5
