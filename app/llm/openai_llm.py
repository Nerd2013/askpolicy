import openai


class OpenAILLM:
    """
    Minimal LLM adapter compatible with rag-core.
    """

    def __init__(
        self,
        *,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
    ):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content