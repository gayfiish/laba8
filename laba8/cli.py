"""Simple command-line application using argparse."""

import argparse


def main() -> None:
    """Parse command-line arguments and print greetings."""
    parser = argparse.ArgumentParser(
        description="A simple greeting application"
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Name of the person to greet"
    )

    parser.add_argument(
        "--times",
        type=int,
        default=1,
        help="Number of greetings"
    )

    args = parser.parse_args()

    if args.times < 1:
        parser.error("--times must be a positive integer")

    for _ in range(args.times):
        print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
