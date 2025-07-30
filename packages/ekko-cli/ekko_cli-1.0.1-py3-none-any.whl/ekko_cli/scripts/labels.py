import click
from InquirerPy.base import Choice
from rich.console import Console
from rich.table import Table

from ekko_cli.utils import SessionUtils
from ekko_cli.utils.label_utils import LabelUtils

from InquirerPy import inquirer

label_utils: LabelUtils
session_utils: SessionUtils

@click.group()
def labels():
    global label_utils
    global session_utils
    from ekko_cli.utils.singleton_utils import get_label_utils
    label_utils = get_label_utils()
    from ekko_cli.utils.singleton_utils import get_session_utils
    session_utils = get_session_utils()
    pass

@click.command()
@click.option('--name', prompt=True)
@click.option('-d', '--description', 'has_description', is_flag=True)
def create(name: str, has_description: bool):
    session_utils.require_auth()
    description: str = ''
    if has_description:
        description = label_utils.get_description()

    label_utils.create(name, description)
    click.echo()
    click.echo('#' + name)
    if description:
        click.echo('-' * (len(name) + 1))
        click.echo()
        click.echo(description)

@click.command('list')
@click.option('--hidden', is_flag=True)
def list_labels(hidden: bool):
    if hidden:
        labels = label_utils.get_labels('all')
    else:
        labels = label_utils.get_labels('visible')
    console = Console()
    table = Table(title="Labels")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Description")
    if hidden:
        table.add_column("Hidden")
    for label in labels:
        if hidden:
            table.add_row(label.id, label.name, label.description, str(label.hidden))
        else:
            table.add_row(label.id, label.name, label.description)
    console.print(table)

@click.command()
def hide():
    labels = label_utils.get_labels('visible')
    choices = []
    for label in labels:
        choices.append(Choice(label, label.name))
    label_to_hide = inquirer.select(
        message="Which label do you want to hide?",
        choices=choices,
    ).execute()
    label_utils.hide(label_to_hide)

@click.command()
def show():
    labels = label_utils.get_labels('hidden')
    choices = []
    for label in labels:
        choices.append(Choice(label, label.name))
    label_to_show = inquirer.select(
        message="Which label do you want to show?",
        choices=choices,
    ).execute()
    label_utils.show(label_to_show)

labels.add_command(create)
labels.add_command(list_labels)
labels.add_command(hide)
labels.add_command(show)