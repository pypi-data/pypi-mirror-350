#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["click>=8.0"]
# ///

# [tool.uvs]
# name = "hello"

import click


@click.command()
@click.option("--name", default="World", help="Name to greet")
def main(name: str):
    """A simple greeting script."""
    click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    main()
