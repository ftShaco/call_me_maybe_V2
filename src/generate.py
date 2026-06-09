# ABOUTME: Two-phase constrained generation: pick the function name, then fill
# ABOUTME: its parameters, producing guaranteed-valid JSON function calls.

from .builder import build_coordinator
from .coordinator import Coordinator
from .validators import FixedValidator, NameValidator


def build_prompt(user_request: str, functions: list) -> str:
    """Construct the instruction prompt fed to the model."""
    system_instruction = (
        "You are an AI assistant equipped with specific tools. "
        "Your task is to analyze the user's request and determine which "
        "function to call.\n"
    )
    lines = []
    for f in functions:
        params = ", ".join(f"{k}: {v.type}" for k, v in f.parameters.items())
        lines.append(f"- {f.name}({params}): {f.description}")
    tools_section = "### AVAILABLE FUNCTIONS ###\n" + "\n".join(lines) + "\n"
    json_shape = (
        "### OUTPUT FORMAT ###\n"
        "You must respond ONLY with a valid JSON object. Do not include "
        "markdown formatting, explanations, or conversational text. "
        "Use the following exact schema (values are an example):\n"
        '{"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}\n'
    )
    user_section = f"### USER REQUEST ###\n{user_request}\n"
    return (f"{system_instruction}\n{tools_section}\n{json_shape}"
            f"\n{user_section}\n")


def _build_name_only(names: list[str]) -> Coordinator:
    """Coordinator for just  {"name": "<NAME>"  (no closing yet)."""
    segments = [FixedValidator('{"name": "'), NameValidator(names)]
    literals = ['{"name": "', None]
    return Coordinator(segments, literals)


def _step(llm, coordinator: Coordinator, prompt_ids: list, output_text: str):
    """One constrained step. Returns the new output_text, or None if stuck."""
    output_ids = llm.encode(output_text) if output_text else []
    logits = llm.next_token_logits(prompt_ids + output_ids)
    ranked = sorted(range(len(logits)), key=lambda x: logits[x], reverse=True)
    for token_id in ranked:
        piece = llm.decode([token_id])
        if piece == "":
            continue
        candidate = output_text + piece
        if coordinator.accept(candidate):
            print(piece, end="", flush=True)
            return candidate
    return None


def generate_call(llm, function_defs: list, prompt_text: str,
                  max_tokens: int = 96) -> str:
    """Generate one complete, valid JSON function call for `prompt_text`.

    Phase 1: pick the function name (constrained to the known names).
    Phase 2: build that function's full template, finish the parameters.
    """
    names = [fn.name for fn in function_defs]
    name_by_str = {fn.name: fn for fn in function_defs}
    full_prompt = build_prompt(prompt_text, function_defs)
    prompt_ids = llm.encode(full_prompt)

    # --- Phase 1: discover the function name ---
    name_coord = _build_name_only(names)
    output_text = ""
    chosen_fn = None
    for _ in range(max_tokens):
        nxt = _step(llm, name_coord, prompt_ids, output_text)
        if nxt is None:
            break
        output_text = nxt
        # has the name become exactly one of the known names?
        # the text is  {"name": "<partial>  ; extract the partial after prefix
        prefix = '{"name": "'
        if output_text.startswith(prefix):
            partial = output_text[len(prefix):]
            if partial in name_by_str:
                chosen_fn = name_by_str[partial]
                break
    if chosen_fn is None:
        return ""  # could not pick a function

    # --- Phase 2: full template, continue from current output_text ---
    full_coord = build_coordinator(chosen_fn, names)
    for _ in range(max_tokens):
        if full_coord.is_complete(output_text):
            break
        nxt = _step(llm, full_coord, prompt_ids, output_text)
        if nxt is None:
            break
        output_text = nxt

    return output_text
