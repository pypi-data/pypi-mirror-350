import logging
import sys
import types

from hermes_model.logging import set_up_logging


def test_set_up_logging_without_prefect(monkeypatch):
    """
    Test that set_up_logging does nothing when prefect is not installed.
    """

    # Simulate ImportError by removing 'prefect' from sys.modules
    monkeypatch.setitem(sys.modules, 'prefect', None)
    monkeypatch.setitem(sys.modules, 'prefect.logging', None)

    logger = logging.getLogger("test_module")
    logger.handlers.clear()

    set_up_logging("test_module")

    # Assert that no handler was added
    assert len(logger.handlers) == 0


def test_set_up_logging_with_prefect(monkeypatch):
    """
    Test that set_up_logging adds a handler when prefect is present.
    """

    # Create a fake prefect.logging module with a dummy get_logger
    fake_prefect_logging = types.SimpleNamespace(get_logger=lambda: None)
    fake_prefect = types.SimpleNamespace(logging=fake_prefect_logging)

    monkeypatch.setitem(sys.modules, 'prefect', fake_prefect)
    monkeypatch.setitem(sys.modules, 'prefect.logging', fake_prefect_logging)

    logger = logging.getLogger("test_module")
    logger.handlers.clear()

    set_up_logging("test_module")

    # Check that one StreamHandler was added
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
