import pytest

from pipecli import Root
from pipecli.commands.generators import IntegersGenerator
from pipecli.commands.transforms import MultiplyTransform


@pytest.fixture
def chain():
    root = Root(debug=True)
    generator = IntegersGenerator(debug=True)
    generator.update_args(['--stop', '3'])
    transform = MultiplyTransform(debug=True)

    root.subcommands.append(generator)
    generator.subcommands.append(transform)
    return root


def test_run(chain):
    chain.run()
    generator = chain.subcommands[0]
    transform = generator.subcommands[0]

    assert generator.results == [1, 2, 3]
    assert transform.results == [2, 4, 6]


def test_filtering(chain):
    generator = chain.subcommands[0]
    transform = generator.subcommands[0]

    assert generator.implement & transform.sources
    assert transform.filter_processing(generator, '')


def test_two_branches(chain):
    generator = chain.subcommands[0]
    transform = generator.subcommands[0]

    transform2 = MultiplyTransform(debug=True)
    transform2.update_args(['-n', '4'])
    generator.subcommands.append(transform2)

    chain.run()
    assert generator.results == [1, 2, 3]
    assert transform.results == [2, 4, 6]
    assert transform2.results == [4, 8, 12]


def test_propagating(chain):
    generator = chain.subcommands[0]
    transform = generator.subcommands[0]
    transform2 = MultiplyTransform(debug=True)
    transform.subcommands.append(transform2)

    chain.run()
    assert generator.results == [1, 2, 3]
    assert transform.results == [2, 4, 6]
    assert transform2.results == [2, 4, 4, 8, 6, 12]
