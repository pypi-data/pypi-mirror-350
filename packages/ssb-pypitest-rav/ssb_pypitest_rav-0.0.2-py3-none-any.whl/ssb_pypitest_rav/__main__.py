"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Pypitest Rav."""


if __name__ == "__main__":
    main(prog_name="ssb-pypitest-rav")  # pragma: no cover
