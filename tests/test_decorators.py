import os
import pytest
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.decorators import log


# ========== ПРОСТЫЕ ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ ==========

@log()
def add(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b


@log(filename="test_log.txt")
def multiply(a: int, b: int) -> int:
    """Умножает два числа."""
    return a * b


@log()
def divide(a: int, b: int) -> float:
    """Делит одно число на другое."""
    return a / b


# ========== ТЕСТЫ ==========

def test_log_to_console(capsys):
    """Тест: логирование в консоль."""
    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_file():
    """Тест: логирование в файл."""
    test_file = "test_log.txt"
    # Удаляем файл, если он существует
    if os.path.exists(test_file):
        os.remove(test_file)

    result = multiply(4, 5)
    assert result == 20

    # Проверяем, что файл создался
    assert os.path.exists(test_file)

    # Проверяем содержимое
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "multiply ok" in content

    # Удаляем тестовый файл
    os.remove(test_file)


def test_log_error_to_console(capsys):
    """Тест: логирование ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_error_to_file():
    """Тест: логирование ошибки в файл."""
    test_file = "test_error_log.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    @log(filename = test_file)
    def faulty_function(x: int) -> int:
        """Функция, которая падает."""
        return x/0

    with pytest.raises(ZeroDivisionError):
        faulty_function(42)

    assert os.path.exists(test_file)

    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "faulty_function error: ZeroDivisionError" in content
        assert "Inputs: (42,), {}" in content

    os.remove(test_file)


def test_log_without_filename_default(capsys):
    """Тест: по умолчанию логируются в консоль."""

    @log()
    def say_hello(name: str) -> str:
        return f"Hello, {name}!"

    result = say_hello("World")
    assert result == "Hello, World!"

    captured = capsys.readouterr()
    assert "say_hello ok" in captured.out


def test_log_multiple_calls(tmp_path):
    """Тест: несколько вызовов одной функции."""
    log_file = tmp_path / "multiple.log"

    @log(filename=str(log_file))
    def counter(n: int) -> int:
        return n + 1

    for i in range(3):
        counter(i)

    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert len(lines) == 3
        for line in lines:
            assert "counter ok" in line