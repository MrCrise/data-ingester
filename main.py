from transformers import AutoTokenizer
from chunkers.token_chunker import TokenChunker
from text import document


TOKENIZER_NAME = "Qwen/Qwen3-8B"
tokenizer = AutoTokenizer.from_pretrained(
    TOKENIZER_NAME, trust_remote_code=True)


text = document
chunker = TokenChunker(tokenizer)
text = chunker.normalize_text(text)
chunks = chunker.chunk_tokens_by_size(text)
print("Чанков:", len(chunks))
print("Токенов в первом:", len(chunks[0]["tokens"]))
print()
print("Пример текста первого чанка:", chunks[0]["text"])
print()
print("Пример текста второго чанка:", chunks[1]["text"])
