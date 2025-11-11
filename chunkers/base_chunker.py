from transformers import AutoTokenizer
import unicodedata
import html
import re


class BaseChunker:
    def __init__(self, tokenizer: AutoTokenizer):
        self.tokenizer = tokenizer

    def tokenize(self, text: str) -> list[int]:
        return self.tokenizer.encode(text, add_special_tokens=False)

    def detokenize(self, token_ids: list[int]) -> str:
        return self.tokenizer.decode(token_ids, clean_up_tokenization_spaces=True)

    def normalize_text(self, text: str) -> str:
        """
        Базовая нормализация текста.

        Нормализует юникод, HTML тэги, кавычки, тире,
        табуляцию, разрывы строк, пробелы.
        """

        text = unicodedata.normalize("NFC", text)
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = text.replace('«', '"').replace('»', '"').replace('“', '"').replace('”', '"').replace('„', '"').replace("‘", "'").replace("’", "'")
        text = re.sub(r"[—–]+", "-", text)
        text = re.sub(r"[^\S\n\t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        text = text.strip()

        return text
