"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Pypi Test Srf."""


if __name__ == "__main__":
    main(prog_name="ssb-pypi-test-srf")  # pragma: no cover
