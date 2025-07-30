# main entry point lol
from __future__ import annotations

import argparse

import argcomplete

from migipo.core._commands import CommandContext
from migipo.core._commands import COMMANDS


def main() -> int:
    parser = argparse.ArgumentParser()

    # main args
    parser.add_argument('--verbose', '-v', action='store_true', default=False, help='Enable verbose output')

    sub = parser.add_subparsers(dest='sub')

    # load the config file
    load = sub.add_parser('load', help='Load the migipo config file')

    load_where = load.add_mutually_exclusive_group(required=True)
    load_where.add_argument('--file', help='Load from a file')
    load_where.add_argument('--origin', help='Load from a remote origin point')

    load.add_argument(
        '--dry-run', action='store_true', default=False,
        help='Dry run (Check whether migipo can read the config file',
    )

    args = parser.parse_args()
    print(args)

    argcomplete.autocomplete(parser)

    ctx = CommandContext()
    COMMANDS['echo'](['a', 'b'], ctx)

    meta = {
        'version': 1,

        'authors': None,
        'author-emails': ['me[at]adwaith[dot]dev'],

        'verbose': True,
    }

    COMMANDS['meta'](meta, ctx)

    # print(ctx._vars)

    COMMANDS['echo'](['$author-emails is the version'], ctx)
    COMMANDS['echo'](['$author-emails is the version'], ctx)

    # print(echo(['hello'], ctx))
    # print(echo([4], ctx))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
