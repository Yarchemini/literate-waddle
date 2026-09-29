"""Модуль с декораторами для логирования работы функций."""
import functools
from datetime import datetime


def log(filename=None):
    """Декоратор для логирования вызовов функции.

    Записывает время вызова, имя функции, аргументы, результат
    выполнения и информацию об ошибках. Логи выводятся в консоль
    или записываются в файл, если передан аргумент filename.

    Args:
        filename: Необязательное имя файла для записи логов.
            Если не задан, логи выводятся в консоль.

    Returns:
        Декоратор, оборачивающий переданную функцию.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"[{timestamp}] {func.__name__} error: "
                    f"{type(error).__name__}: {error}. "
                    f"args={args}, kwargs={kwargs}"
                )
                _write_log(message, filename)
                raise
            else:
                message = (
                    f"[{timestamp}] {func.__name__} ok. "
                    f"args={args}, kwargs={kwargs}, result={result!r}"
                )
                _write_log(message, filename)
                return result

        return wrapper

    return decorator


def _write_log(message, filename):
    """Записывает сообщение лога в файл или выводит в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")
    else:
        print(message)
