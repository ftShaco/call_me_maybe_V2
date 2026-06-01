from llm_sdk import Small_LLM_Model


class LLM:
    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        self.model = Small_LLM_Model(model_name)

    def encode(self, text: str) -> list[int]:
        raw_token_ids = self.model.encode(text)
        return raw_token_ids[0].tolist()

    def decode(self, token_ids: list[int]) -> str:
        return self.model.decode(token_ids)

    def next_token_logits(self, token_ids: list[int]) -> list[float]:
        return self.model.get_logits_from_input_ids(token_ids)
