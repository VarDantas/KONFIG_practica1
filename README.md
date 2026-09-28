Практическое задание №1. Эмулятор оболочки ОС (Вариант 16)


Общее описание

Эмулятор командной оболочки UNIX-подобной ОС. Реализован на Python.

Этап 1: минимальный прототип REPL.
Этап 2: конфигурация — поддержка параметров командной строки и стартовых скриптов.
Этап 3: виртуальная файловая система (VFS), загружаемая из ZIP-архива в память.
Этап 4: основные команды — ls, cd, echo, du.
Этап 5: дополнительные команды — rmdir.

Функции и настройки

get_prompt(vfs, cwd) — формирует приглашение вида username@hostname:cwd.
parse_input(user_input) — разбирает ввод на команду и аргументы, раскрывает переменные окружения.
resolve_path(target, cwd) — преобразует относительный путь в абсолютный.
cmd_ls(args, vfs, cwd) — команда ls.
cmd_cd(args, vfs, cwd) — команда cd.
cmd_echo(args) — команда echo.
cmd_du(args, vfs, cwd) — команда du.
execute_command(command, args, vfs, cwd) — выполняет команду.
run_startup_script(script_path, vfs) — выполняет команды из стартового скрипта.
parse_args() — разбирает аргументы командной строки.
main() — главный цикл REPL или выполнение стартового скрипта.


Класс VFS (в src/vfs.py)

load_zip(zip_path) — загружает VFS из ZIP-архива в память (без распаковки на диск).
exists(path) — проверяет существование пути.
is_dir(path) — проверяет, является ли путь папкой.
list_dir(path) — возвращает список содержимого папки.
get_size(path) — возвращает размер файла или папки.
info() — краткая информация о VFS.


Параметры командной строки

--vfs    — путь к ZIP-архиву с VFS.
--script — путь к стартовому скрипту.


Команды эмулятора

exit     — завершение работы.
vfs-info — информация о загруженной VFS.
ls       — вывод содержимого директории (работает с VFS).
cd       — смена директории (работает с VFS).
echo     — печать аргументов.
du       — размер файла или папки в байтах.
rmdir    — удаление пустой директории (работает с VFS).

Команды для сборки и запуска

Запуск в интерактивном режиме:
./run.sh

Запуск с параметрами:
python3 src/main.py --vfs test_vfs/vfs_deep.zip --script scripts/start3.txt

Генерация тестовых VFS:
python3 tests/create_test_vfs.py


Тестовые скрипты

./run_test1.sh — тест с параметром --vfs
./run_test2.sh — тест с --vfs и --script
./run_test3.sh — тест только с --script
./run_test4.sh — тест с VFS и стартовым скриптом
./run_test5.sh — тест команд ls, cd, echo, du
./run_test6.sh — тест команды rmdir

Примеры использования

Интерактивный режим:

    user@host:/$ ls
    etc
    home
    user@host:/$ cd /home/user
    user@host:/home/user$ ls
    docs
    readme.txt
    user@host:/home/user$ echo Привет
    Привет
    user@host:/home/user$ du /home/user/readme.txt
    28    /home/user/readme.txt
    user@host:/home/user$ exit
    Выход из эмулятора...


Обработка ошибок загрузки VFS

    python3 src/main.py --vfs test_vfs/not_exist.zip
    Ошибка: файл test_vfs/not_exist.zip не найден

    python3 src/main.py --vfs README.md
    Ошибка: README.md не ZIP-архив


Тестирование

Для демонстрации работы используются скрипты run_test1.sh ... run_test5.sh
и стартовые скрипты в папке scripts.
Юнит-тесты будут добавлены позже.
