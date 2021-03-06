"""This module contains script entrypoints for shreddit.
"""
import argparse
import yaml
import logging
from shreddit import default_config
from shreddit.oauth import oauth_test
from shreddit.shredder import Shredder


def main():
    parser = argparse.ArgumentParser(description="Command-line frontend to the shreddit library.")
    parser.add_argument("-c", "--config", help="Config file to use instead of the default shreddit.yml")
    parser.add_argument("-p", "--praw", help="PRAW config (if not ./praw.ini)")
    parser.add_argument("-t", "--test-oauth", help="Perform OAuth test and exit", action="store_true")
    args = parser.parse_args()

    if args.test_oauth:
        oauth_test(args.praw)
        return

    with open(args.config or "shreddit.yml") as fh:
        # Not doing a simple update() here because it's preferable to only set attributes that are "whitelisted" as
        # configuration options in the form of default values.
        user_config = yaml.safe_load(fh)
        for option in default_config:
            if option in user_config:
                default_config[option] = user_config[option]

    # TODO: Validate config options
    shredder = Shredder(default_config, args.praw)
    shredder.shred()


if __name__ == "__main__":
    main()
