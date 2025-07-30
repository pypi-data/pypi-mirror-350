#!/usr/bin/env python3
import random
import click
from .loader import load_quotes

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-n", "--count", default=1, show_default=True, type=int, help="Number of quotes.")
@click.version_option("0.1.0", prog_name="excellent-quote")
def main(count: int) -> None:
    """Print COUNT random quotes from Kevin Kelly."""
    if count < 1:
        click.echo("Count must be >= 1", err=True)
        raise SystemExit(1)

    quotes = load_quotes()
    for i in range(count):
        click.echo(random.choice(quotes))
        if i < count - 1:
            click.echo()

if __name__ == "__main__":
    main()
