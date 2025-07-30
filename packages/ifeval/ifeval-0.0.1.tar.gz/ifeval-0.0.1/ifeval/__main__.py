import argparse
import os

from .core import IfEval, logger


def main():
    parser = argparse.ArgumentParser(
        prog="ifeval",
        description="Evaluate all if-statement predicates in a Python file")
    parser.add_argument("filepath",
                        help="Path to the Python (.py) file to analyze")
    parser.add_argument("-N",
                        "--no-dry",
                        action="store_true",
                        help="Disable dry run (change the original file)")
    args = parser.parse_args()
    assert os.path.isfile(args.filepath), f"Can not find file {args.filepath}"

    ife = IfEval(args.filepath)
    ife.print_diff()
    if args.no_dry:
        ife.save_to(args.filepath)
        logger.warning(f"The file {args.filepath} has been updated")


if __name__ == "__main__":
    main()
