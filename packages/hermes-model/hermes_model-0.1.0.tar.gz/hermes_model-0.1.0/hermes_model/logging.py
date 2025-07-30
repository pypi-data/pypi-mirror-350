import logging


def set_up_logging(module_name):
    """
    If Prefect is installed, set up logging for the given module name.

    The standard log is "redirected" by prefect, therefore set up an
    additional handler for the given module.
    """
    try:
        from prefect.logging import get_logger  # noqa
    except ImportError:
        return

    module_name = module_name.split(".")[0]

    root_logger = logging.getLogger(module_name)

    handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter(
        "%(asctime)s.%(msecs)03d | %(levelname)-7s | "
        "%(name)r - %(message)s",
        datefmt="%H:%M:%S"))

    root_logger.addHandler(handler)

    root_logger.setLevel(logging.INFO)
