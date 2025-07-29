from .himl import ConfigProcessor, ConfigGenerator
import yaml
import os
from glob import glob
from itertools import chain


def process(leaf, output="materialized", root=None):
    leaf = os.path.abspath(leaf)
    output = os.path.abspath(output)
    if root is None:
        root = os.path.abspath(os.getcwd())
    else:
        root = os.path.abspath(root)
    os.chdir(root)

    processor = ConfigProcessor()

    config_data = processor.process(
        path=leaf,
        cwd=root,
    )

    config_data = remove_null(config_data)

    if not os.path.exists(output):
        os.mkdir(output)
    else:
        for f in os.listdir(output):
            os.remove(os.path.join(output, f))

    for name, config in config_data.items():
        with open(f"{output}/{name}.yaml", "w") as f:
            yaml.dump(
                config,
                f,
                Dumper=ConfigGenerator.yaml_dumper(),
                default_flow_style=False,
                width=200,
                sort_keys=False,
            )


def remove_null(config):
    if isinstance(config, (list, tuple)):
        return [remove_null(el) for el in config if el is not None]
    elif isinstance(config, dict):
        return {k: remove_null(v) for k, v in config.items() if v is not None}
    else:
        return config


def check_config(root, output):
    root = os.path.abspath(root)
    output = os.path.abspath(output)

    oldest_materialized = min([os.path.getmtime(file) for file in glob(f"{output}/*.yaml")])

    up_to_date = True
    for file in chain(glob(f"{root}/**.yaml"), glob(f"{root}/**.yml")):
        if os.path.getmtime(file) > oldest_materialized:
            up_to_date = False
            print(f"{file} is newer than the materialized config.")

    return up_to_date
