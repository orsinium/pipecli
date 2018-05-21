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

    assert generator.implement & transform.required
    assert transform.sources == transform.required | transform.optional == frozenset({'integer'})
    assert transform.filter_processing(generator, '')
