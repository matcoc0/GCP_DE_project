from __future__ import annotations

import argparse

from open_meteo_pipeline.main import main as open_meteo_pipeline_main


def add_explore_command(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Add the Open-Meteo exploration command."""

    parser = subparsers.add_parser(
        "explore",
        help="Explore Open-Meteo weather and air-quality APIs.",
        description="Fetch weather and ai-quality forecast for a selected city",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--city",
        "-c",
        help="City name, for example Paris or London.",
    )

    parser.add_argument(
        "--country-code",
        "-cc",
        help="Optional ISO country code, for example FR.",
    )

    parser.add_argument(
        "--forecast-days",
        "-fc",
        type=int,
        default=3,
        choices=range(1, 8),
        metavar="[1-7]",
        help="Number of forecast days.",
    )

    parser.set_defaults(func=open_meteo_pipeline_main)


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


def run(argv: list[str] | None = None) -> None:
    """Parse arguments and run the application."""

    parser = build_parser()
    arguments, unknown_arguments = parser.parse_known_args(argv)

    command_function = arguments.func

    argument_dictionnary = vars(arguments).copy()
    argument_dictionnary.pop("func")
    argument_dictionnary.pop("command")

    if unknown_arguments:
        argument_dictionnary["unknown_args"] = unknown_arguments

    command_function(**argument_dictionnary)


if __name__ == "__main__":
    run()
