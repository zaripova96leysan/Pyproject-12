"""
Модуль с декоратором для логирования вызовов функций.

Содержит декоратор log, который позволяет логировать успешные вызовы функций
и ошибки с их параметрами. Логи могут выводиться в консоль или записываться в файл.
"""

import functools
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Логирует вызов функции и её результат. При успешном выполнении записывает
    сообщение "function_name ok". При ошибке записывает сообщение об ошибке
    и входные параметры функции.
    """

    def decorator(func: Callable) -> Callable:
        """
        Внутренний декоратор, принимающий функцию для обёртки.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)

                raise

        return wrapper

    return decorator
