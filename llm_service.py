import asyncio
from typing import AsyncGenerator, Dict, List
from ollama import AsyncClient


class AsyncLLMService:
    def __init__(self,
                 llm_host: str,
                 model_name: str = "qwen3:8b",
                 context_window_size: int = 20000):
        self.client = AsyncClient(llm_host)
        self.model_name = model_name
        self.context_window_size = context_window_size

    def _build_system_prompt(self) -> str:
        return (
            "Ты - профессиональный юридический помощник Федеральной антимонопольной службы. "
            "Твоя задача - отвечать на вопросы пользователя, основываясь ИСКЛЮЧИТЕЛЬНО на предоставленных документах.\n"
            "Правила:\n"
            "1. Не используй собственные знания, если их нет в контексте.\n"
            "2. Если в документах нет ответа, так и скажи: 'К сожалению, в базе данных нет информации по данному вопросу'.\n"
            "3. Ссылайся на документы, указывая их названия или номера дел, когда приводишь факты.\n"
            "4. Ответ должен быть полным, юридически грамотным, но понятным.\n"
            "5. Форматируй ответ в Markdown."
        )

    def _prepare_context(self, documents: List[Dict]) -> str:
        """
        Формирует строку контекста (без изменений)
        """
        context_parts = []
        current_length = 0

        for i, doc in enumerate(documents, 1):
            text = doc.get("full_text") or doc.get("best_chunk") or ""
            doc_id = doc.get("doc_id", "unknown")

            doc_block = f"<document id='{doc_id}'>\n{text}\n</document>\n"

            if current_length + len(doc_block) > self.context_window_size:
                break

            context_parts.append(doc_block)
            current_length += len(doc_block)

        return "\n".join(context_parts)

    async def generate_stream(self, query: str, documents: List[Dict]) -> AsyncGenerator[str, None]:
        if not documents:
            yield "Документы не найдены."
            return

        context_str = self._prepare_context(documents)

        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Вопрос: {query}\n\nДокументы:\n{context_str}"}
        ]

        try:
            stream = await self.client.chat(
                model=self.model_name,
                messages=messages,
                options={
                    "num_ctx": 8192
                },
                stream=True
            )

            async for chunk in stream:
                content = chunk['message']['content']
                yield content

        except Exception as e:
            yield f"\n[Ollama Error: {e}]"
