import click

from ekko_cli.utils.session_utils import SessionUtils

session_utils: SessionUtils

@click.group()
def auth():
    global session_utils
    from ekko_cli.utils.singleton_utils import get_session_utils
    session_utils = get_session_utils()
    pass

@auth.command()
def login():
    if session_utils.check_session():
        click.echo("You are already logged in.", err=True)
        return

    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    try:
        session_utils.save_session(email, password)
    except Exception:
        click.echo("Failed to authenticate. Please try again.", err=True)

@auth.command()
def logout():
    if not session_utils.check_session():
        click.echo("You are not logged in.", err=True)
    else:
        session_utils.clear_session()

@auth.command()
def me():
    if not session_utils.check_session():
        click.echo("You are not logged in.", err=True)
    else:
        session = session_utils.get_session()
        click.echo(f"Logged in with {session.email}")