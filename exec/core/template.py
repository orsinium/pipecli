from pathlib import Path
import configparser
from jinja2 import Environment
import yaml


TEMPLATE_NAME = 'template.yml'
CONFIG_NAME = 'config.ini'
BASE_INI = "[defaults]\n"


class Template:
    def __init__(self, struct):
        self.struct = struct

    @classmethod
    def from_task(cls, task):
        ...

    @classmethod
    def from_file(cls, path):
        if not isinstance(path, Path):
            path = Path(path)

        # read template
        template_path = path / TEMPLATE_NAME
        with template_path.open() as f:
            document = f.read()

        # read config
        config_path = path / CONFIG_NAME
        config = configparser.ConfigParser()
        config.read(str(config_path))

        # render yaml
        template = Environment.from_string(document)
        document = template.render(**config['defaults'])

        # read yaml
        struct = yaml.load(document)
        return Template(struct)

    def to_task(self):
        ...

    def to_file(self, path):
        # write template
        document = yaml.dump(self.struct, default_flow_style=False)
        template_path = path / TEMPLATE_NAME
        with template_path.open('w') as f:
            f.write(document)

        # write config
        config_path = path / CONFIG_NAME
        with config_path.open('w') as f:
            f.write(BASE_INI)
