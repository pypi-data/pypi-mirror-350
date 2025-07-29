#!/usr/bin/env python

"""Tests for `src` package."""


import unittest

from click.testing import CliRunner
from deftlariat.scripts import cli
from hamcrest import *


class TestSrc(unittest.TestCase):
    """Tests for `src` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        pass

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.deft_cli)
        print(result.output)
        assert_that(result.exit_code, equal_to(2))  # Should be SystemExit issue, no command
        assert 'deft lariats' in result.output
        help_result = runner.invoke(cli.deft_cli, ['--help'])
        assert_that( help_result.exit_code, equal_to(0))
        assert_that(help_result.output, string_contains_in_order('--version', '--help'))

    def test_example_one_with_json_input(self):
        """Test the example_one command with JSON input."""
        runner = CliRunner()

        # Test with a single JSON object using a temporary file
        with runner.isolated_filesystem():
            with open('test.json', 'w') as f:
                f.write('[{"symbol": "OTCMKTS:FRMO", "total_holdings": 2000, "percentage_of_total_supply": 0.2}]')

            result = runner.invoke(cli.deft_cli, ['example-coingecko', '--data-file', 'test.json'], catch_exceptions=False)
            print(f"Single JSON output: {result.output}")
            print(f"Exit code: {result.exit_code}")
            if result.exception:
                print(f"Exception: {result.exception}")
            assert result.exit_code == 0
            assert 'Data Filter hit' in result.output

        # Test with a JSON array using a temporary file
        with runner.isolated_filesystem():
            with open('test.json', 'w') as f:
                f.write('[{"symbol": "OTCMKTS:FRMO", "total_holdings": 2000, "percentage_of_total_supply": 0.2}]')

            result = runner.invoke(cli.deft_cli, ['example-coingecko', '--data-file', 'test.json'], catch_exceptions=False)
            print(f"JSON array output: {result.output}")
            print(f"JSON array exit code: {result.exit_code}")
            if result.exception:
                print(f"JSON array exception: {result.exception}")
            assert result.exit_code == 0
            assert 'Data Filter hit' in result.output

        # Test with JSON that doesn't match the filter criteria
        with runner.isolated_filesystem():
            with open('test.json', 'w') as f:
                f.write('[{"symbol": "BTC", "total_holdings": 10, "percentage_of_total_supply": 0.01}]')

            result = runner.invoke(cli.deft_cli, ['example-coingecko', '--data-file', 'test.json'], catch_exceptions=False)
            print(f"Non-matching JSON output: {result.output}")
            print(f"Non-matching JSON exit code: {result.exit_code}")
            if result.exception:
                print(f"Non-matching JSON exception: {result.exception}")
            assert result.exit_code == 0
            # No filter hit, so no output expected
            assert 'Data Filter hit' not in result.output
