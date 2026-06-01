import argparse
from pathlib import Path

DEFAULT_FUNCTIONS = Path("data/input/functions_definition.json")
DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT = Path("data/output/function_calling_results.json")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='blablabla')
    parser.add_argument("--functions_definition", type=Path,
                        help="", default=DEFAULT_FUNCTIONS)
    parser.add_argument("--input", type=Path, help="",
                        default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, help="",
                        default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)
