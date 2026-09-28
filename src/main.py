"""
Эмулятор командной оболочки (REPL) для Варианта №16.
Этап 4: основные команды — ls, cd, echo, du.
"""

import argparse
import getpass
import os
import socket
import sys

from vfs import VFS


def get_prompt(vfs, cwd):
    """Формирует приглашение с текущей директорией VFS."""
    user = getpass.getuser()
    host = socket.gethostname()
    return f"{user}@{host}:{cwd}$ "


def parse_input(user_input):
    """Разбирает ввод на команду и аргументы."""
    expanded = os.path.expandvars(user_input)
    parts = expanded.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def resolve_path(target, cwd):
    """Преобразует относительный путь в абсолютный."""
    if target.startswith("/"):
        return target
    if cwd == "/":
        return "/" + target
    return cwd + "/" + target


def cmd_ls(args, vfs, cwd):
    """Команда ls — выводит содержимое директории."""
    target = args[0] if args else cwd
    target = resolve_path(target, cwd)

    if not vfs.exists(target):
        print(f"ls: {target}: нет такого файла или папки")
        return True

    if not vfs.is_dir(target):
        print(target)
        return True

    for name in vfs.list_dir(target):
        print(name)
    return True


def cmd_cd(args, vfs, cwd):
    """Команда cd — меняет текущую директорию."""
    if not args:
        return "/"

    target = args[0]

    if target == "..":
        if cwd == "/":
            return "/"
        return os.path.dirname(cwd) or "/"

    target = resolve_path(target, cwd)

    if not vfs.exists(target):
        print(f"cd: {target}: нет такой директории")
        return cwd

    if not vfs.is_dir(target):
        print(f"cd: {target}: это не директория")
        return cwd

    return target


def cmd_echo(args):
    """Команда echo — печатает аргументы."""
    print(" ".join(args))
    return True


def cmd_du(args, vfs, cwd):
    """Команда du — выводит размер файла или папки."""
    target = args[0] if args else cwd
    target = resolve_path(target, cwd)

    size = vfs.get_size(target)
    if size < 0:
        print(f"du: {target}: нет такого файла или папки")
        return True

    print(f"{size}\t{target}")
    return True


def execute_command(command, args, vfs, cwd):
    """Выполняет команду. Возвращает True, False или новый cwd."""
    if command == "exit":
        print("Выход из эмулятора...")
        sys.exit(0)
    elif command == "ls":
        return cmd_ls(args, vfs, cwd)
    elif command == "cd":
        return cmd_cd(args, vfs, cwd)
    elif command == "echo":
        return cmd_echo(args)
    elif command == "du":
        return cmd_du(args, vfs, cwd)
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
    """Выполняет скрипт, останавливается при ошибке."""
    if not os.path.exists(script_path):
        print(f"Ошибка: файл {script_path} не найден")
        return

    cwd = "/"
    with open(script_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{get_prompt(vfs, cwd)}{line}")

            command, args = parse_input(line)
            if not command:
                continue

            result = execute_command(command, args, vfs, cwd)
            if isinstance(result, str):
                cwd = result
            elif result is False:
                print("Скрипт остановлен из-за ошибки.")
                sys.exit(1)


def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки"
    )
    parser.add_argument("--vfs", default=None)
    parser.add_argument("--script", default=None)
    return parser.parse_args()


def main():
    """Главный цикл REPL."""
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

    cwd = "/"
    print("Эмулятор оболочки запущен. Введите 'exit'.")
    while True:
        try:
            user_input = input(get_prompt(vfs, cwd))
            command, args_list = parse_input(user_input)
            if command:
                result = execute_command(command, args_list, vfs, cwd)
                if isinstance(result, str):
                    cwd = result
        except KeyboardInterrupt:
            print("\nВыход...")
            sys.exit(0)
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
