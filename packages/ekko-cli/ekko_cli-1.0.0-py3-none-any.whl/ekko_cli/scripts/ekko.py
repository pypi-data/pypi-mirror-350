import click
from InquirerPy import inquirer
from InquirerPy.base import Choice

from ekko.utils import EkkoUtils, SessionUtils, LabelUtils

ekko_utils: EkkoUtils
session_utils: SessionUtils
label_utils: LabelUtils

@click.group()
def ekko():
    global ekko_utils
    global session_utils
    global label_utils
    from ekko.utils.singleton_utils import get_ekko_utils, get_session_utils, get_label_utils
    ekko_utils = get_ekko_utils()
    session_utils = get_session_utils()
    label_utils = get_label_utils()
    pass

@click.command()
@click.option('-m', '--message')
@click.option('-d', '--description', 'has_description', is_flag=True)
@click.option('-l', '--labels', 'has_labels', is_flag=True)
def add(message: str, has_description: bool, has_labels: bool):
    session_utils.require_auth()
    if not message:
        message = click.prompt('Message')
    description = None
    if has_description:
        description = ekko_utils.get_description()
    picked_labels = []
    if has_labels:
        labels = label_utils.get_labels('visible')
        picked_labels = inquirer.select(
            message="Which labels do you want to add to this entry?",
            choices=[Choice(label, label.name) for label in labels],
            multiselect=True
        ).execute()

    ekko_utils.add_entry(message, description, picked_labels)
    click.echo()
    click.echo(message)
    if description:
        click.echo('-' * len(message))
        click.echo()
        click.echo(description)
     
ekko.add_command(add)