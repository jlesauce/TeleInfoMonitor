import argparse
import os
import sys


def main():
    parser = _create_argument_parser()
    parser.parse_args(sys.argv[1:])

    print("Hello World!")


def _create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Application used to monitor TeleInfo serial data from Enedis Linky equipment.')
    parser.add_argument('--data_file', metavar='FILE', type=lambda x: is_valid_file(parser, x),
                        help='File containing TeleInfo data.')
    return parser


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    return arg


if __name__ == "__main__":
    main()
