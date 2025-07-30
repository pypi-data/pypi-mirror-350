import hashlib
import keyword
import os
from typing import Set, List


class NamesGenerator:
    """
    Генератор уникальных детерминированных имён на основе seed и списка слов.
    - Автоматически избегает ключевых слов Python (добавляет '_val').
    - Если слово неуникальное, выбирает следующее из списка.
    - Если все варианты исчерпаны, добавляет детерминированный суффикс.
    """

    def __init__(self, seed: int, word_file: str = "random_words_list.txt"):
        """
        Инициализация генератора.
        :param seed: Начальное значение для детерминированности.
        :param word_file: Файл со словами (по одному на строку).
        """
        self.seed = seed
        self.word_file = word_file
        self.words = self._load_words()
        self.used_names: Set[str] = set()

    def _load_words(self) -> List[str]:
        """Загружает слова из файла."""
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, self.word_file)
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def _generate_hash_int(self, index: int) -> int:
        """Генерирует целое число на основе seed и индекса."""
        combined = f"{self.seed}_{index}".encode()
        hash_bytes = hashlib.sha256(combined).digest()
        return int.from_bytes(hash_bytes, byteorder="big")

    def generate_name(self, index: int) -> str:
        """
        Генерирует уникальное имя для заданного индекса.
        :param index: Уникальный идентификатор для генерации.
        :return: Уникальное имя.
        """
        hash_int = self._generate_hash_int(index)
        base_idx = hash_int % len(self.words)
        attempts = 0
        name = None

        # Пытаемся найти уникальное имя из списка
        while attempts < len(self.words):
            current_idx = (base_idx + attempts) % len(self.words)
            name = self.words[current_idx]
            if name in keyword.kwlist:
                name = f"{name}_val"
            if name not in self.used_names:
                break
            attempts += 1

        # Если все варианты исчерпаны — добавляем суффикс
        if attempts >= len(self.words) or name in self.used_names:
            suffix = hash_int % 1000
            name = f"{self.words[base_idx]}_{suffix}"

        self.used_names.add(name)
        return name