from __future__ import annotations

import argparse

from open_meteo_pipeline.main import main


def add_explore_command(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Add the Open-Meteo exploration command."""

    explore_parser = subparsers.add_parser(
        "explore",
        help="Explore Open-Meteo weather and air-quality APIs.",
    )

    explore_parser.add_argument(
        "city",
        help="City name, for example Paris or London.",
    )

    explore_parser.add_argument(
        "--country-code",
        help="Optional ISO country code, for example FR.",
    )

    explore_parser.add_argument(
        "--forecast-days",
        type=int,
        default=3,
        choices=range(1, 8),
        metavar="[1-7]",
        help="Number of forecast days. Default: 3.",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="DE_tool",
        description="Open-Meteo data engineering pipeline CLI.",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_explore_command(subparsers)

    return parser


def run() -> None:
    """Parse arguments and run the application."""

    parser = build_parser()
    arguments = parser.parse_args()

    main(arguments)


if __name__ == "__main__":
    run()
