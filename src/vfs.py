"""
Модуль виртуальной файловой системы (VFS).
Загружает VFS из ZIP-архива в память.
"""

import base64
import os
import zipfile


class VFS:
    """Виртуальная файловая система в памяти."""

    def __init__(self):
        """Создаёт пустую VFS."""
        self.files = {}
        self.binary = set()
        self.source = None

    def load_zip(self, zip_path):
        """
        Загружает VFS из ZIP-архива.
        Не распаковывает архив на диск.
        Возвращает True при успехе, иначе False.
        """
        if not os.path.exists(zip_path):
            print(f"Ошибка: файл {zip_path} не найден")
            return False

        if not zipfile.is_zipfile(zip_path):
            print(f"Ошибка: {zip_path} не ZIP-архив")
            return False

        self.files = {"/": None}
        self.binary = set()

        try:
            with zipfile.ZipFile(zip_path, "r") as archive:
                for name in archive.namelist():
                    if name.endswith("/"):
                        continue
                    path = "/" + name
                    self._ensure_parents(path)
                    data = archive.read(name)
                    self._store(path, data)
        except zipfile.BadZipFile:
            print(f"Ошибка: неверный формат {zip_path}")
            return False

        self.source = zip_path
        return True

    def _store(self, path, data):
        """Сохраняет данные. Бинарные — в base64."""
        try:
            self.files[path] = data.decode("utf-8")
        except UnicodeDecodeError:
            encoded = base64.b64encode(data)
            self.files[path] = encoded.decode("ascii")
            self.binary.add(path)

    def _ensure_parents(self, path):
        """Добавляет родительские папки пути."""
        parts = path.strip("/").split("/")
        current = ""
        for part in parts[:-1]:
            current += "/" + part
            if current not in self.files:
                self.files[current] = None

    def info(self):
        """Возвращает краткую информацию о VFS."""
        files = sum(1 for v in self.files.values() if v is not None)
        dirs = len(self.files) - files
        return f"VFS: {self.source}, файлов: {files}, папок: {dirs}"

    def exists(self, path):
        """Проверяет, существует ли путь."""
        return path in self.files

    def is_dir(self, path):
        """Проверяет, является ли путь папкой."""
        return path in self.files and self.files[path] is None

    def list_dir(self, path):
        """
        Возвращает список имён файлов и папок внутри директории.
        """
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        prefix = path if path == "/" else path + "/"
        names = set()

        for item in self.files:
            if item == path:
                continue
            if not item.startswith(prefix):
                continue
            rest = item[len(prefix):]
            if not rest:
                continue
            first = rest.split("/")[0]
            names.add(first)

        return sorted(names)

    def get_size(self, path):
        """
        Возвращает размер файла или директории в байтах.
        Для директории — сумма размеров всех файлов внутри.
        """
        if path not in self.files:
            return -1

        if self.files[path] is not None:
            return len(self.files[path].encode("utf-8"))

        prefix = path if path == "/" else path + "/"
        total = 0
        for item, content in self.files.items():
            if item == path:
                continue
            if not item.startswith(prefix):
                continue
            if content is not None:
                total += len(content.encode("utf-8"))
        return total
