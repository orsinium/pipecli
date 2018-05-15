from ..core import Command, commands, cached_property
import argparse


@commands.register('example')
class Root(Command):
    implement = 'example_protocol'

    def process(self):
        yield

    @cached_property
    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("square", help="display a square of a given number", type=int)
        parser.add_argument("--verbosity", help="increase output verbosity")
        return parser
