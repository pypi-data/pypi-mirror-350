from __future__ import annotations

import re
from functools import wraps
from typing import Any
from typing import Callable
from typing import Type
from typing import TypedDict

from typeguard import check_type
from typeguard import TypeCheckError

from migipo import log as migipo_log
from migipo import LogType

# ==================== Context ====================
# this is a shared context that is passed to all commands


class CommandContext:
    def __init__(self) -> None:
        self._vars: dict[str, Any] = {}

    def _set_var(self, key: str, val: Any) -> None:
        self._vars[key] = val

    def _get_vat(self, key: str) -> Any:
        return self._vars.get(key, None)


CommandFnType = Callable[[Any, CommandContext], int]


COMMANDS: dict[str, CommandFnType] = {}


def _register_command(name: str, ip_type: Type[object]) -> \
        Callable[[CommandFnType], Callable[[Any, CommandContext], int]]:
    def dec_func(fn: CommandFnType) -> Callable[[Any, CommandContext], int]:

        @wraps(fn)
        def wrap(args: Any, ctx: CommandContext) -> int:
            try:
                check_type(args, ip_type)
                return fn(args, ctx)
            except TypeCheckError as e:
                migipo_log(str(e), log_type=LogType.ERROR)
                return 1

        COMMANDS[name] = wrap
        return wrap
    return dec_func


def substitute_vars(s: str, values: dict[str, Any]) -> str:
    def replacer(match: re.Match[str]) -> str:
        key = match.group(1)
        return str(values.get(key, match.group(0)))

    return re.sub(r'\$(\w[\w-]*)', replacer, s)


# ==================== ECHO ====================
EchoInputType = list[str]


@_register_command('echo', EchoInputType)
def echo(args: EchoInputType, ctx: CommandContext) -> int:
    print('\n'.join(map(lambda x: substitute_vars(x, ctx._vars), args)))
    return 0


# ==================== META ====================

MetaInputType = TypedDict(
    'MetaInputType',
    {
        'version': int,
        'authors': list[str] | None,
        'author-emails': list[str] | None,
        'verbose': bool,
    },
)


@_register_command('meta', MetaInputType)
def meta(args: MetaInputType, ctx: CommandContext) -> int:
    ctx._set_var('version', args['version'])
    ctx._set_var('authors', args['authors'])
    ctx._set_var('author-emails', args['author-emails'])
    ctx._set_var('verbose', args['verbose'])
    return 0
