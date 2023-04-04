import argparse


def parser() -> argparse.ArgumentParser:
    root_parser = argparse.ArgumentParser(
        prog='lvcli',
        description='LabVIEW CLI Framework example parser.'
    )
    root_subparsers = root_parser.add_subparsers(
        title='commands',
        dest='cmd',
        description='Set of example commands.'
    )
    cmd_echo_parser = root_subparsers.add_parser(
        name='echo',
        help='echo whatever you pass'
    )
    cmd_echo_parser.add_argument(
        'smth',
        help='something to be echoed'
    )
    return root_parser
