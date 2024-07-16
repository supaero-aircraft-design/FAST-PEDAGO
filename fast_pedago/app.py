import logging

import os
from pathlib import Path

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
)


MAIN_NOTEBOOK_NAME = Path(__file__).parent / "notebook" / "FAST_OAD_app.ipynb"


class Main:
    """
    Class for managing command line and doing associated actions
    """

    def __init__(self):
        class _CustomFormatter(
            RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter
        ):
            pass

        self.parser = ArgumentParser(
            description="FAST pedagogical branch main program",
            formatter_class=_CustomFormatter,
        )

    @staticmethod
    def _run(args):
        """Run FAST pedagogical branch locally or with server configuration."""
        machine = "server" if args.server else "local"
        print(MAIN_NOTEBOOK_NAME)
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
            os.system(command + str(MAIN_NOTEBOOK_NAME))
        except KeyboardInterrupt:
            exit()

    # ENTRY POINT ============================================================
    def run(self):
        """Main function."""
        subparsers = self.parser.add_subparsers(title="sub-commands")

        # sub-command for running AeroMAPS -----------------------------------
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
