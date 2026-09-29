"""Тесты для декоратора log."""
import pytest

from decorators import log


def test_log_success_prints_to_console(capsys):
    """Успешный вызов функции логируется в консоль по умолчанию."""

    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add" in captured.out
    assert "result=5" in captured.out


def test_log_success_writes_to_file(tmp_path):
    """При указании filename логи записываются в файл."""
    filename = tmp_path / "success.log"

    @log(filename=str(filename))
    def multiply(a, b):
        return a * b

    result = multiply(2, 4)

    assert result == 8
    content = filename.read_text(encoding="utf-8")
    assert "multiply" in content
    assert "result=8" in content


def test_log_error_prints_to_console(capsys):
    """Ошибка выполнения функции логируется в консоль."""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide" in captured.out
    assert "ZeroDivisionError" in captured.out


def test_log_error_writes_to_file(tmp_path):
    """Ошибка выполнения функции логируется в файл с входными параметрами."""
    filename = tmp_path / "errors.log"

    @log(filename=str(filename))
    def fail(x):
        raise ValueError("bad value")

    with pytest.raises(ValueError):
        fail(10)

    content = filename.read_text(encoding="utf-8")
    assert "fail" in content
    assert "ValueError" in content
    assert "bad value" in content
    assert "10" in content


def test_log_preserves_function_metadata():
    """Декоратор сохраняет имя и docstring исходной функции."""

    @log()
    def sample(x):
        """Sample docstring."""
        return x

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Sample docstring."


def test_log_supports_kwargs(capsys):
    """Декоратор корректно логирует именованные аргументы."""

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet(name="World", greeting="Hi")
    captured = capsys.readouterr()

    assert result == "Hi, World!"
    assert "greet" in captured.out
    assert "World" in captured.out
