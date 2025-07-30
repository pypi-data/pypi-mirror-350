from vajra.logger import init_logger

logger = init_logger(__name__)


def log_and_print_info(message: str):
    logger.info(message)


def log_and_print_warning(message: str):
    logger.warning(f"[yellow]{message}[/yellow]", extra={"markup": True})


def log_and_print_error(message: str):
    logger.error(f"[red]{message}[/red]", extra={"markup": True})
