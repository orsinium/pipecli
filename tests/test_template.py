from pros import Template, Root
from pros.commands.generators import IntegersGenerator


def test_import_task():
    root = Root()
    task = IntegersGenerator()
    root.add(task)
    assert list(Template._iterate_tasks(root)) == [(root, task)]
    template = Template.from_task(root)
    assert template.struct['include'] == ['pros.commands.generators']
    assert len(template.struct['tasks']) == 1
    assert template.struct['tasks'][0]['name'] == 'generate/integers'


def test_export_task():
    root = Root()
    task = IntegersGenerator()
    root.add(task)
    template = Template.from_task(root)

    new_root = template.to_task()
    assert isinstance(new_root, Root)
    assert len(new_root.subtasks) == 1
    assert new_root.subtasks[0].name == task.name


def test_export_file(tmpdir):
    root = Root()
    task = IntegersGenerator()
    root.add(task)
    template = Template.from_task(root)
    template.to_file(str(tmpdir))

    files = {'template.yml', 'defaults.yml', 'config.yml'}
    assert {path.basename for path in tmpdir.listdir()} == files

    with tmpdir.join('template.yml').open() as f:
        document = f.read()
    assert document.startswith('version:')
    assert 'tasks:' in document


def test_import_file(tmpdir):
    root = Root()
    task = IntegersGenerator()
    root.add(task)
    template = Template.from_task(root)
    template.to_file(str(tmpdir))

    Template.from_file(str(tmpdir))
    new_root = template.to_task()
    assert isinstance(new_root, Root)
    assert len(new_root.subtasks) == 1
    assert new_root.subtasks[0].name == task.name
