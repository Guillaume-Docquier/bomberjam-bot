# A base game loop.
# You shouldn't have to modify this file unless you have specific needs.
# Your bot logic should be implemented in bot_logic/bot.py.
# You can, however, do anything you'd like in here.
#
# This script takes one optional argument: --logging
# Example usage: python MyBot.py --logging=True
# ==============================================================================

import argparse

from bot_logic.bot import get_bot_name
from bot_logic.bot import compute_next_action
from core.commands import ActionCommand
from core.commands import RegisterBotCommand
from core.logging import configure_file_logging
from core.logging import log
from models.state import State


def is_logging_enabled():
    """
    Gets the --logging argument

    :return: bool
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--logging", help="Activate logging", default=False)

    return parser.parse_args().logging


def play():
    """
    Abstracts the game loop and the configurations required.
    You will need to implement bot_logic/bot.py for this to work properly.

    :return: None
    """
    bot_name = get_bot_name()

    print(RegisterBotCommand(bot_name))
    bot_id = input()

    if is_logging_enabled():
        configure_file_logging(f"MyBot-{bot_id}")

    log(f"Bot name is '{bot_name}' with id '{bot_id}'")

    while True:
        try:
            state = State(input(), bot_id)
            tick = state.tick
            action = compute_next_action(state)

            print(ActionCommand(tick, action))
        except Exception:
            pass


play()
