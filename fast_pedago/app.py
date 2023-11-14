# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import logging
import os
import os.path as pth

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
)

import webbrowser


MAIN_NOTEBOOK_NAME = pth.join(
    pth.join(pth.dirname(__file__), "notebook"), "FAST_OAD_app.ipynb"
)


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
                "jupyter notebook "
                "--port=8080 "
                "--no-browser "
                "--MappingKernelManager.cull_idle_timeout=7200 "
            )
        else:
            command = "jupyter notebook --no-browser --port=8888 "

        # It shouldn't, it really shouldn't but it works ^^' It looks like because of the custom
        # CSS background (the only thing not working), I can't launch voila directly in the
        # command line. However, when launching from a notebook (with the small button on top) it
        # displays well. This can be replicated, once the jupyter command is launched by going to
        # the url listed below. So the plan is simple, launch notebook and open the URL.
        # Unfortunately, if we launch notebooks, the terminal is put on hold and the browser
        # never open. For some reasons however, if we launch the browser first and then launch the
        # notebooks it works ^^'
        webbrowser.open(
            "http://localhost:8888/voila/render/fast_pedago/notebook/FAST_OAD_app.ipynb"
        )
        try:
            os.system(command)
        except KeyboardInterrupt:
            exit()

    # ENTRY POINT ==================================================================================
    def run(self):
        """Main function."""
        subparsers = self.parser.add_subparsers(title="sub-commands")

        # sub-command for running AeroMAPS -------------------------------------
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

        # Parse ------------------------------------------------------------------------------------
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
