import pathlib
import argparse

from . import utils
from . import compile


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        utils.error(message)


parser = ArgumentParser(
    prog="ccb",
    description="Python Compiler Collection for Bash",
    epilog="Made by @simplyrohan",
    usage="%(prog)s input.py",
)


parser.add_argument("input", nargs="*", type=str, help="path to source Python file")
parser.add_argument(
    "-o",
    "--output",
    type=str,
    metavar="",
    help="output script file",
    required=False,
    default=None,
)


def main():
    args = parser.parse_args()

    # argument validation
    if len(args.input) == 0:
        utils.error("no input files")

    input_file = pathlib.Path(args.input[0])

    if not input_file.exists():
        utils.error(f"could not find input file {input_file.absolute()}")

    output_path = pathlib.Path(
        args.output if args.output else input_file.name.removesuffix(".py") + ".sh"
    )

    output_path.write_text(compile(input_file.read_text(), input_file.name))

    utils.log("Done!", "green", True)


if __name__ == "__main__":
    main()
