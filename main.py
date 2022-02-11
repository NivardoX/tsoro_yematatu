from collections import defaultdict
from logging import getLogger
import logging

import click

from client.run import run as client_run

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

logger = getLogger("START")


def module_not_found():
    logger.fatal("MODULE NOT FOUND")


start_commands = {"CLIENT": client_run}


@click.command()
@click.argument("module", default="CLIENT", required=True)
def start(module):
    start_commands.get(module, module_not_found)()


if __name__ == "__main__":
    start()
