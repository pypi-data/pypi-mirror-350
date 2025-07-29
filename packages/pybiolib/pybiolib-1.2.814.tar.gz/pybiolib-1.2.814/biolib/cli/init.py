import os
import sys

import click

from biolib import templates
from biolib._internal.add_copilot_prompts import add_copilot_prompts


@click.command(help='Initialize a project with a .biolib/config.yml file', hidden=True)
def init() -> None:
    cwd = os.getcwd()
    config_file_path = f'{cwd}/.biolib/config.yml'
    readme_path = f'{cwd}/README.md'

    if os.path.exists(config_file_path):
        print(f'The file "{config_file_path}" already exists', file=sys.stderr)
        exit(1)

    try:
        project_name = input('Enter a name for your project: ')

        os.makedirs(f'{cwd}/.biolib', exist_ok=True)
        with open(config_file_path, 'w') as config_file:
            config_file.write(templates.example_app.CONFIG_YML)

        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as readme_file:
                readme_file.write(f'# {project_name}\n')

        add_copilot_prompts(force=False, silent=True)

    except KeyboardInterrupt:
        print('\nInit command cancelled.', file=sys.stderr)
        exit(1)
