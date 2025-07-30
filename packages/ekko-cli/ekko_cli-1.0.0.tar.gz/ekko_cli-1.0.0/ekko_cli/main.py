import click

from ekko.scripts.auth import auth
from ekko.scripts.ekko import ekko
from ekko.scripts.labels import labels

ekko.add_command(auth)
ekko.add_command(labels)

if __name__ == '__main__':
    ekko()