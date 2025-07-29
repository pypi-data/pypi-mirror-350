from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="Nuscenes Hacker")
    subparsers = parser.add_subparsers(title="commands")

    # hack
    hack_parser = subparsers.add_parser("hack", help="hack mode")
    from .hack import main as hack_module

    hack_module.add_arguments(hack_parser)

    # restore
    restore_parser = subparsers.add_parser("restore", help="restore mode")
    from .restore import main as restore_module

    restore_module.add_arguments(restore_parser)

    args, unknown = parser.parse_known_args()

    if hasattr(args, "func"):
        args.func(args, unknown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
