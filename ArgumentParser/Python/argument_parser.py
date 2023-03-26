import argparse
import json
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import Optional, Any


def _filter_dict(dict: dict[str, Any]) -> dict[str, Any]:
    filtered = {}
    for k, v in dict.items():
        if v is not None and k != 'parser':
            if isinstance(v, (str, list)):
                if len(v) > 0:
                    filtered.update({k: v})
            if isinstance(v, bool):
                filtered.update({k: v})
    return filtered


def create_parser(
        prog: str,
        usage: Optional[str] = None,
        description: Optional[str] = None,
        epilog: Optional[str] = None,
        prefix_chars='-',
        fromfile_prefix_chars: Optional[str] = None,
        argument_default: Optional[str] = None,
        conflict_handler='error',
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True
        ) -> argparse.ArgumentParser:
    kwargs = _filter_dict(locals())
    return argparse.ArgumentParser(**kwargs)


def add_argument(
        parser: argparse.ArgumentParser,
        name_or_flags: list[str],
        action: Optional[str] = None,
        nargs: Optional[str] = None,
        const: Optional[str] = None,
        default: Optional[str] = None,
        choices: Optional[list[str]] = None,
        required: Optional[bool] = None,
        help: Optional[str] = None,
        metavar: Optional[str] = None,
        dest: Optional[str] = None
        ) -> argparse.ArgumentParser:
    kwargs = _filter_dict(locals())
    args = kwargs.pop('name_or_flags')
    parser.add_argument(*args, **kwargs)
    return parser


def add_subparsers(
        parser: argparse.ArgumentParser,
        title: Optional[str] = None,
        description: Optional[str] = None,
        prog: Optional[str] = None,
        action: Optional[str] = None,
        dest: Optional[str] = None,
        required: Optional[bool] = None,
        help: Optional[str] = None,
        metavar: Optional[str] = None
        ):
    kwargs = _filter_dict(locals())
    subparser = parser.add_subparsers(**kwargs)
    return [parser, subparser]


def _get_parser(p_sp):
    return p_sp[0]


def _get_subparser(p_sp):
    return p_sp[1]


def add_parser(
        subparser: argparse._SubParsersAction,
        name: str,
        aliases: list[str],
        usage: Optional[str] = None,
        description: Optional[str] = None,
        epilog: Optional[str] = None,
        prefix_chars='-',
        fromfile_prefix_chars: Optional[str] = None,
        argument_default: Optional[str] = None,
        conflict_handler='error',
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True
        ) -> argparse._SubParsersAction:
    kwargs = _filter_dict(locals())
    subparser.add_parser(**kwargs)
    return subparser


def parse_args(
        parser: argparse.ArgumentParser,
        arguments: list[str]
        ):
    err = out = parsed = ''
    with (
            redirect_stderr(StringIO()) as tmp_stderr,
            redirect_stdout(StringIO()) as tmp_stdout
            ):
        try:
            parsed = parser.parse_args(arguments)
            if parsed is not None:
                parsed = json.dumps(vars(parsed))
            else:
                parsed = ''
        except SystemExit as se:
            if se.code == 0 or 2:
                err = tmp_stderr.getvalue()
                out = tmp_stdout.getvalue()
            else:
                raise se
    return [parsed, out, err]


if __name__ == '__main__':
    out = err = parsed = ''
    parser = create_parser('parser')
    add_argument(
        parser,
        ['-o', '--option'],
        action='store_true',
        help='option help'
        )
    add_argument(
        parser,
        ['argument'],
        help='argument help'
        )
    _, subparser = add_subparsers(
        parser,
        title='commands',
        description='commands description',
        dest='cmd',
        help='commands help'
        )
    add_parser(
        subparser,
        name='read',
        aliases=['r'],
        )
    add_parser(
        subparser,
        name='write',
        aliases=['w'],
        )
    # parsed = parse_args(parser, ['-o', '1', 'r'])
    parsed = parse_args(parser, ['-h'])
    out = parsed[1]
    err = parsed[2]
    parsed = parsed[0]
    print(36*'#' + ' stdout ' + 36*'#')
    print(out)
    print(36*'#' + ' stderr ' + 36*'#')
    print(err)
    print(36*'#' + ' parsed ' + 36*'#')
    print(parsed)
