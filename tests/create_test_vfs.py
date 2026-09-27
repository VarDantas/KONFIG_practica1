"""
Генератор тестовых ZIP-архивов для проверки VFS.
"""

import os
import zipfile


def create_zip(path, files):
    """Создаёт ZIP-архив с указанными файлами."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    print(f"Создан: {path}")


def main():
    """Создаёт три тестовых VFS."""
    # Минимальный: один файл
    create_zip("test_vfs/vfs_minimal.zip", {
        "readme.txt": "Привет, мир!\n",
    })

    # Несколько файлов
    create_zip("test_vfs/vfs_several.zip", {
        "readme.txt": "Добро пожаловать\n",
        "notes.txt": "Заметки\n",
        "config.ini": "[main]\nkey=value\n",
    })

    # Глубокое дерево: 3+ уровня
    create_zip("test_vfs/vfs_deep.zip", {
        "home/user/readme.txt": "Домашняя папка\n",
        "home/user/docs/report.txt": "Отчёт\n",
        "home/user/docs/notes/todo.txt": "Список дел\n",
        "etc/config.txt": "Конфигурация\n",
    })


if __name__ == "__main__":
    main()
