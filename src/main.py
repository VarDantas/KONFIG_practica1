"""
Эмулятор командной оболочки (REPL) для Варианта №16.
Этап 1: минимальный прототип с заглушками ls, cd и обработкой ошибок.
"""

import getpass
import os
import socket
import sys


def get_prompt():
    """
    Формирует приглашение к вводу на основе реальных данных ОС.
    Пример: username@hostname:~$
    """
    user = getpass.getuser()
    host = socket.gethostname()
    cwd = os.getcwd()
    home = os.path.expanduser("~")

    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]

    return f"{user}@{host}:{cwd}$ "


def parse_input(user_input):
    """
    Разбирает строку ввода на команду и аргументы.
    Раскрывает переменные окружения (например, $HOME).
    Возвращает кортеж (команда, список аргументов).
    """
    expanded = os.path.expandvars(user_input)
    parts = expanded.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def execute_command(command, args):
    """
    Выполняет команду или выводит сообщение об ошибке.
    Команды ls и cd — заглушки, выводят своё имя и аргументы.
    """
    if command == "exit":
        print("Выход из эмулятора...")
        sys.exit(0)
    elif command in ("ls", "cd"):
        args_str = " ".join(args)
        print(f"{command}: {args_str}")
    else:
        print(f"{command}: команда не найдена")


def main():
    """
    Главный цикл REPL.
    """
    print("Эмулятор оболочки запущен. Введите 'exit' для выхода.")
    while True:
        try:
            user_input = input(get_prompt())
            command, args = parse_input(user_input)
            if command:
                execute_command(command, args)
        except KeyboardInterrupt:
            print("\nВыход...")
            sys.exit(0)
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
