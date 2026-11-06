"""Kenya food market analysis package."""

__all__ = ["__version__", "main"]

__version__ = "0.1.0"


def main() -> None:
    from .cli import main as cli_main

    cli_main()
