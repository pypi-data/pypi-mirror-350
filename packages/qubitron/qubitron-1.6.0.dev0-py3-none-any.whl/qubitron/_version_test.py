# pylint: disable=wrong-or-nonexistent-copyright-notice
import qubitron


def test_version() -> None:
    assert qubitron.__version__ == "1.6.0.dev0"
