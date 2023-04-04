import argparse
import json
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import importlib.util
from pathlib import Path


def load_parser(parser_path: str) -> argparse.ArgumentParser:
    module_path = Path(parser_path)
    current_file_directory = Path(__file__).resolve().parent
    if not module_path.is_absolute():
        module_path = current_file_directory.joinpath(module_path)
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, 'parser')
    return func()


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

    parser = load_parser('parsers/example_parser.py')
    parsed = parse_args(parser, 'echo -h'.split())

    out = parsed[1]
    err = parsed[2]
    parsed = parsed[0]

    print(36*'#' + ' stdout ' + 36*'#')
    print(out)
    print(36*'#' + ' stderr ' + 36*'#')
    print(err)
    print(36*'#' + ' parsed ' + 36*'#')
    print(parsed)
