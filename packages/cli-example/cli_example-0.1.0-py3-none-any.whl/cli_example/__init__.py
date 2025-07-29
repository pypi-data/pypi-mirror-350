"""Módulo CLI principal."""

import click


@click.command()
def cli():
    """A simple CLI tool."""
    click.echo("Hello, World!")


if __name__ == "__main__":
    cli()
