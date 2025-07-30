import click

from ekko_cli.scripts.auth import auth
from ekko_cli.scripts.ekko import ekko
from ekko_cli.scripts.labels import labels

ekko.add_command(auth)
ekko.add_command(labels)

if __name__ == '__main__':
    ekko()