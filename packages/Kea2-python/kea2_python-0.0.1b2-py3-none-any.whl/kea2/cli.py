# coding: utf-8
# cli.py

from __future__ import absolute_import, print_function
import sys
from .utils import getProjectRoot, getLogger
from .kea_launcher import run
import argparse

import os
from pathlib import Path


logger = getLogger(__name__)


def cmd_version(args):
    from importlib.metadata import version
    print(version("Kea2-python"), flush=True)


def cmd_init(args):
    cwd = Path(os.getcwd())
    configs_dir = cwd / "configs"
    if os.path.isdir(configs_dir):
        logger.warning("Kea2 project already initialized")
        return

    import shutil
    def copy_configs():
        src = Path(__file__).parent / "assets" / "fastbot_configs"
        dst = configs_dir
        shutil.copytree(src, dst)

    def copy_samples():
        src = Path(__file__).parent / "assets" / "quicktest.py"
        dst = cwd / "quicktest.py"
        shutil.copyfile(src, dst)

    copy_configs()
    copy_samples()
    logger.info("Kea2 project initialized.")


def cmd_load_configs(args):
    pass


def cmd_run(args):
    base_dir = getProjectRoot()
    if base_dir is None:
        logger.error("kea2 project not initialized. Use `kea2 init`.")
        return
    run(args)


_commands = [
    dict(action=cmd_version, command="version", help="show version"),
    dict(
        action=cmd_init,
        command="init",
        help="init the Kea2 project in current directory",
    )
]


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-d", "--debug", action="store_true",
                        help="show detail log")

    subparser = parser.add_subparsers(dest='subparser')

    actions = {}
    for c in _commands:
        cmd_name = c['command']
        actions[cmd_name] = c['action']
        sp = subparser.add_parser(
            cmd_name,
            help=c.get('help'),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        for f in c.get('flags', []):
            args = f.get('args')
            if not args:
                args = ['-'*min(2, len(n)) + n for n in f['name']]
            kwargs = f.copy()
            kwargs.pop('name', None)
            kwargs.pop('args', None)
            sp.add_argument(*args, **kwargs)

    from .kea_launcher import _set_runner_parser
    _set_runner_parser(subparser)
    actions["run"] = cmd_run
    if sys.argv[1:] == ["run"]:
        sys.argv.append("-h")
    args = parser.parse_args()

    import logging
    logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug("args: %s", args)

    if args.subparser:
        actions[args.subparser](args)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
