"""Console script for src."""
import sys
import json

import click

from deftlariat import __version__
from deftlariat import EqualTo, NumberComparer, MatcherType


@click.group(no_args_is_help=True)
@click.version_option(version=__version__)
def deft_cli():
    """Console script for deft lariats."""
    pass


@deft_cli.command()
def hello(name: str) -> None:
    click.echo(f"Hello {name}")


zip_code_list = ['']


@deft_cli.command()
@click.option('--data-file',
              help='file to work with',
              type=click.File('r'),
              default=sys.stdin)
def example_coingecko(data_file) -> None:
    """
    Coin Gecko Example. Demonstrate how to use the data filter with a list of dictionaries from
    coingecko.com API. Return records that match any one of three configured filters.
    """
    click.echo("Example One - Data Filter.  \nThis example will search the input list of dictionaries for "
               "records that match any of three filters.\n\n"
               "The three filters are:\n"
               "1. EqualTo - Check if the value of a the `symbol` field is equal to a target value `OTCMKTS:FRMO`.\n"
               "2. NumberComparer - Check if the value of the `total_holdings` field is greater than or equal to "
               " the target value: `1000`\n"
               "3. NumberComparer - Check if the value of the `percentage_of_total_supply` field is greater than "
               "or equal to the target value: `0.1`\n"
               "Matching records will be printed to stdout.\n\n\n"
               )

    with data_file as f:
        try:
            # First read the data as a string
            content = f.read()

            # Check if there's any content
            if not content.strip():
                # No Data on stdin, so return
                click.echo("No Data found - Either File or stdin")
                return

            # Then parse it as JSON
            data = json.loads(content)
            # If data is not a list, wrap it in a list
            if not isinstance(data, list):
                data = [data]
        except json.JSONDecodeError as e:
            click.echo(f"Error parsing JSON: {e}")
            return

    # TODO: Assume stream is a json list
    field_key = 'symbol'
    filter_one = EqualTo(field_key)
    target_value = 'OTCMKTS:FRMO'

    filter_two = NumberComparer('total_holdings', MatcherType.GREATER_THAN_EQUAL_TO)
    filter_three = NumberComparer('percentage_of_total_supply', MatcherType.GREATER_THAN_EQUAL_TO)
    for x in data:
        if any([filter_one.is_match(target_value, x),
                filter_two.is_match(1000, x),
                filter_three.is_match(0.1, x),
                ]):
            click.echo(f"Data Filter hit for record:\n{x}\n\n")
