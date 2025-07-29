"""Módulo CLI principal."""

import click


@click.command()
def cli():
    """A simple CLI tool."""
    click.echo("Hello, World!")


def main():
    """Main function to run the CLI."""
    cli()


if __name__ == "__main__":
    main()
