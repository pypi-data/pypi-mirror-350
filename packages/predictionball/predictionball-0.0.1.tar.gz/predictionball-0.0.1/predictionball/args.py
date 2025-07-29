"""Find the args used by the main CLI."""

import argparse

STDOUT_FILE = "-"


def parse_args() -> argparse.Namespace:
    """Create the args based on the CLI inputs."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        default=STDOUT_FILE,
        help="The file to write the output to (- if to stdout).",
    )
    return parser.parse_args()
