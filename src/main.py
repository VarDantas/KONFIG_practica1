"""
Эмулятор командной оболочки (REPL) для Варианта №16.
Этап 3: подключение виртуальной файловой системы (VFS).
"""

import argparse
import getpass
import os
import socket
import sys

from vfs import VFS


def get_prompt():
    """Формирует приглашение на основе данных ОС."""
    user = getpass.getuser()
    host = socket.gethostname()
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]
    return f"{user}@{host}:{cwd}$ "


def parse_input(user_input):
    """Разбирает ввод на команду и аргументы."""
    expanded = os.path.expandvars(user_input)
    parts = expanded.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def execute_command(command, args, vfs):
    """Выполняет команду. Возвращает True при успехе."""
    if command == "exit":
        print("Выход из эмулятора...")
        return True
    elif command in ("ls", "cd"):
        args_str = " ".join(args)
        print(f"{command}: {args_str}")
        return True
    elif command == "vfs-info":
        if vfs and vfs.source:
            print(vfs.info())
        else:
            print("VFS не загружена")
        return True
    else:
        print(f"{command}: команда не найдена")
        return False


def run_startup_script(script_path, vfs):
    """Выполняет команды из скрипта, стоп при ошибке."""
    if not os.path.exists(script_path):
        print(f"Ошибка: файл {script_path} не найден")
        return

    with open(script_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{get_prompt()}{line}")
            command, args = parse_input(line)
            if command:
                ok = execute_command(command, args, vfs)
                if not ok:
                    print("Скрипт остановлен из-за ошибки.")
                    sys.exit(1)


def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки"
    )
    parser.add_argument(
        "--vfs",
        help="Путь к физическому расположению VFS",
        default=None
    )
    parser.add_argument(
        "--script",
        help="Путь к стартовому скрипту",
        default=None
    )
    return parser.parse_args()


def main():
    """Главный цикл REPL или выполнение скрипта."""
    args = parse_args()

    print("Параметры запуска")
    print(f"VFS: {args.vfs}")
    print(f"Стартовый скрипт: {args.script}")

    vfs = VFS()
    if args.vfs:
        if not vfs.load_zip(args.vfs):
            sys.exit(1)
        print(vfs.info())

    if args.script:
        run_startup_script(args.script, vfs)
        return

    print("Эмулятор оболочки запущен. Введите 'exit'.")
    while True:
        try:
            user_input = input(get_prompt())
            command, args_list = parse_input(user_input)
            if command:
                execute_command(command, args_list, vfs)
                if command == "exit":
                    sys.exit(0)
        except KeyboardInterrupt:
            print("\nВыход...")
            sys.exit(0)
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
