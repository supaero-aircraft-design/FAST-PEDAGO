import logging
import os
import shutil
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
)
from pathlib import Path

MAIN_NOTEBOOK_NAME = "FAST_OAD_app.ipynb"
MAIN_NOTEBOOK_PATH = Path(__file__).parent / "notebook" / MAIN_NOTEBOOK_NAME


class Main:
    """
    Class for managing command line and doing associated actions
    """

    def __init__(self):
        class _CustomFormatter(RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter):
            pass

        self.parser = ArgumentParser(
            description="FAST pedagogical branch main program",
            formatter_class=_CustomFormatter,
        )

    @staticmethod
    def _run(args):
        """Run FAST pedagogical branch locally or with server configuration."""
        machine = "server" if args.server else "local"
        print(MAIN_NOTEBOOK_PATH)
        if machine == "server":
            command = (
                "voila "
                "--port=8080 "
                "--no-browser "
                "--MappingKernelManager.cull_idle_timeout=7200 "
                r"""--VoilaConfiguration.file_whitelist="['.*\."""
                """(png|jpg|gif|xlsx|ico|pdf|json)']" """
            )
        else:
            command = (
                "voila "
                r"""--VoilaConfiguration.file_whitelist="['.*\."""
                """s(png|jpg|gif|xlsx|ico|pdf|json)']" """
            )

        # To not get an ugly error message when you ctrl+c
        try:
            os.system(command + str(MAIN_NOTEBOOK_PATH))  # noqa: S605 this is a literal string, it can be considered safe.
        except KeyboardInterrupt:
            sys.exit()

    @staticmethod
    def _copy_notebook(args):
        # Should be a pathlib Path already
        requested_destination = args.destination
        if not requested_destination.is_dir():
            print("Input path should be the path to a directory. Exiting")
            return 1

        if not requested_destination.exists():
            requested_destination.mkdir(parents=True, exist_ok=True)

        shutil.copy(MAIN_NOTEBOOK_PATH, args.destination)
        print("You may now run Jupyter with:")
        print(f'   jupyter lab "{MAIN_NOTEBOOK_NAME}"')
        return 0

    # ENTRY POINT ============================================================
    def run(self):
        """Main function."""
        subparsers = self.parser.add_subparsers(title="sub-commands")

        # sub-command for running FAST-PEDAGO -----------------------------------
        parser_run = subparsers.add_parser(
            "run",
            help="run FAST-OAD pedagogical branch",
            description="run FAST-OAD pedagogical branch",
        )

        parser_run.add_argument(
            "--server",
            action="store_true",
            help="to be used if ran on server",
        )
        parser_run.set_defaults(func=self._run)

        # subcommand for copying the notebook ----------------------------------
        parser_copy = subparsers.add_parser(
            "copy_notebook",
            help="copy notebook to target directory to run without voila",
            description="copy notebook to target directory to run without voila",
        )

        parser_copy.add_argument(
            "-d",
            "--destination",
            type=Path,
            required=True,
            help="Location in which to copy the notebook.",
        )
        parser_copy.set_defaults(func=self._copy_notebook)

        # Parse --------------------------------------------------------------
        args = self.parser.parse_args()
        try:
            args.func(args)
        except AttributeError:
            self.parser.print_help()


def main():
    log_format = "%(levelname)-8s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    Main().run()


if __name__ == "__main__":
    main()
