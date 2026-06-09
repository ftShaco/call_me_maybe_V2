import sys
from .llm import LLM
from .io_files import load_ft_definitions, load_prompts, InputError
from .parser import parse_args
from .generate import generate_call
import json
import os
import time


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        functions = load_ft_definitions(args.functions_definition)
        prompts = load_prompts(args.input)
    except InputError as e:
        print(f"Error occured: {e}", file=sys.stderr)
        return 1

    llm = LLM()
    results = []
    start = time.perf_counter()
    total = len(prompts)
    for i, entry in enumerate(prompts, start=1):
        print(f"{i}/{total} processing...\n", file=sys.stderr)
        print(f"User prompt: {entry.prompt}\n")
        try:
            raw = generate_call(llm, functions, entry.prompt)
            call = json.loads(raw)
            results.append({
                "prompt": entry.prompt,
                "name": call["name"],
                "parameters": call["parameters"],
            })
            elapsed = time.perf_counter() - start
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: could not generate a valid call for "
                  f"{entry.prompt!r}: {e}", file=sys.stderr)

    print(f"\nProcessed {total} prompt(s) in {elapsed:.1f}s "
          f"({elapsed/total:.1f}s per prompt).", file=sys.stderr)
    output_dir = os.path.dirname(args.output)
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"Error: Failed to create output directory '{output_dir}'"
                  f".\nDetails: {e}", file=sys.stderr)
            return 1

    try:
        with open(args.output, "w", encoding="utf-8") as f:

            json.dump(results, f, indent=4)
    except OSError as e:
        print(f"Error: Failed to write results to '{args.output}'.\n"
              f"Details: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
