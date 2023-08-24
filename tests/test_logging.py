import pytest
from reqpy.__logging import Myconsole  # Import your Myconsole class from the appropriate module

class TestMyconsole:

    @staticmethod
    def test_title(capsys):
        Myconsole.title("Test Title")
        captured = capsys.readouterr()
        assert "Test Title".upper() in captured.out

    @staticmethod
    def test_apps(capsys):
        Myconsole.apps("Test Apps")
        captured = capsys.readouterr()
        assert ">>> Test Apps".upper() in captured.out

    @staticmethod
    def test_task(capsys):
        Myconsole.task("Test Task")
        captured = capsys.readouterr()
        assert " - Test Task..." in captured.out

    @staticmethod
    def test_info(capsys):
        Myconsole.info("Test Info")
        captured = capsys.readouterr()
        assert "Test Info" in captured.out

    @staticmethod
    def test_ok(capsys):
        Myconsole.ok("Test Ok")
        captured = capsys.readouterr()
        assert "Test Ok" in captured.out

    @staticmethod
    def test_ko(capsys):
        Myconsole.ko("Test Ko")
        captured = capsys.readouterr()
        assert "Test Ko" in captured.out

    @staticmethod
    def test_warning(capsys):
        Myconsole.warning("Test Warning")
        captured = capsys.readouterr()
        assert "WARNING: Test Warning" in captured.out

    @staticmethod
    def test_error(capsys):
        Myconsole.error("Test Error")
        captured = capsys.readouterr()
        assert "ERROR: Test Error" in captured.out

    @staticmethod
    def test_progressBar(capsys):
        items = [1, 2, 3]
        for _ in Myconsole.progressBar(items, "Test Progress"):
            pass
        captured = capsys.readouterr()
        assert "Test Progress" in captured.out
