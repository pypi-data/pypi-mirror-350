from . import process, check_config
import argparse


def main():
    parser = argparse.ArgumentParser(prog="pigeon-config")
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help=f"Check if {parser.prog} should be run again.",
    )
    parser.add_argument(
        "-r",
        "--root",
        type=str,
        default=None,
        help="The path to use as the current working directory.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="materialized",
        help="The directory to output the configuration files to.",
    )
    parser.add_argument("leaf", type=str, nargs="?", help="The leaf directory to use.")

    args = parser.parse_args()

    if args.check:
        exit(not check_config(args.root, args.output))
    else:
        if args.leaf is None:
            print("leaf must be specified!")
            exit(1)
        process(args.leaf, output=args.output, root=args.root)


if __name__ == "__main__":
    main()
