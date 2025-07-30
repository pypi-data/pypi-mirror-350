"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Libtest Urb."""


if __name__ == "__main__":
    main(prog_name="ssb-libtest-urb")  # pragma: no cover
