from exec import Template, Root
from exec.commands.generators import IntegersGenerator


def test_import_task():
    root = Root()
    task = IntegersGenerator()
    root.add(task)
    assert list(Template._iterate_tasks(root)) == [(root, task)]
    template = Template.from_task(root)
    assert template.struct['include'] == ['exec.commands.generators']
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
