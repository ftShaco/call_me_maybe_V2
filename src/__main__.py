import sys

from .io_files import load_ft_definitions, load_prompts
from .parser import parse_args
from .models import InputError


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        functions = load_ft_definitions(args.functions_definition)
        prompts = load_prompts(args.input)
    except InputError as e:
        print(f"Error occured: {e}", file=sys.stderr)
        return 1

    print(f"Number of functions definition: {len(functions)}")
    for f in functions:
        print(f)
    print(f"Number of prompts: {len(prompts)}")
    for p in prompts:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
