import pytest

from exec import Root
from exec.commands.generators import IntegersGenerator
from exec.commands.transforms import MultiplyTransform


@pytest.fixture
def chain():
    root = Root(debug=True)
    generator = IntegersGenerator(debug=True)
    generator.update_args(['--stop', '3'])
    transform = MultiplyTransform(debug=True)

    root.add(generator)
    generator.add(transform)
    return root


def test_run(chain):
    chain.run()
    generator = chain.subtasks[0]
    transform = generator.subtasks[0]

    assert generator.results == [1, 2, 3]
    assert transform.results == [2, 4, 6]


def test_filtering(chain):
    generator = chain.subtasks[0]
    transform = generator.subtasks[0]

    assert generator.implement & transform.sources
    assert transform.filter_processing(generator, '')


def test_two_branches(chain):
    generator = chain.subtasks[0]
    transform = generator.subtasks[0]

    transform2 = MultiplyTransform(debug=True)
    transform2.update_args(['-n', '4'])
    generator.add(transform2)

    chain.run()
    assert generator.results == [1, 2, 3]
    assert transform.results == [2, 4, 6]
    assert transform2.results == [4, 8, 12]


def test_propagation(chain):
    generator = chain.subtasks[0]
    transform = generator.subtasks[0]
    transform2 = MultiplyTransform(debug=True)
    transform.add(transform2)

    chain.run()
    assert generator.results == [1, 2, 3]
    assert transform.results == [2, 4, 6]
    assert transform2.results == [2, 4, 4, 8, 6, 12]
