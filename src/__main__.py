import sys
from .llm import LLM
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

    # print(f"Number of functions definition: {len(functions)}")
    # for f in functions:
    #     print(f)
    # print(f"Number of prompts: {len(prompts)}")
    # for p in prompts:
    #     print(p)

    llm = LLM()
    ids = llm.encode("What is the sum of 2 and 3?")
    print("token ids:", ids)
    print("decoded back:", llm.decode(ids))
    logits = llm.next_token_logits(ids)
    print("num logits:", len(logits))

    return 0


if __name__ == "__main__":
    sys.exit(main())
