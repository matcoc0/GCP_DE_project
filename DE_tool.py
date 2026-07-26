from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:

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

    return parser


def main() -> None:

    parser = build_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()
