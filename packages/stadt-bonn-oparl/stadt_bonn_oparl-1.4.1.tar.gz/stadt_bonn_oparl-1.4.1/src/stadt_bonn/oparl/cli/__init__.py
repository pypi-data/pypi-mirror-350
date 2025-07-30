"""
Main entry point and setup for the CLI application.

This module initializes the cyclopts application, configures logging based on
verbosity flags, defines global CLI options, and registers all command groups
from the cli subpackages.
"""

from typing import Annotated

import cyclopts
import logfire

from stadt_bonn.oparl.logging import configure_logging

from ..papers.classifier import analyse_paper
from .convert import convert
from .download import download
from .enrich import enrich
from .extract import extract
from .find import find
from .vectordb import vectordb

"""The main cyclopts application instance."""


app = cyclopts.App(
    help="Stadt Bonn OPARL Papers CLI",
    name="oparl-cli",
    config=cyclopts.config.Env(
        "OPARL_",  # Every environment variable will begin with this.
    ),
    default_parameter=cyclopts.Parameter(negative=()),
)


# https://github.com/BrianPugh/cyclopts/issues/212
app.meta.group_parameters = cyclopts.Group("Global Parameters", sort_key=0)


@app.meta.default
def app_launcher(
    *tokens: Annotated[str, cyclopts.Parameter(show=False, allow_leading_hyphen=True)],
    very_verbose: Annotated[
        list[bool],
        cyclopts.Parameter(
            name=["--very-verbose", "-vv"],
            required=False,
            show_default=False,
            help="Increase verbosity level.",
        ),
    ] = [],
    verbose: Annotated[
        list[bool],
        cyclopts.Parameter(
            name=["--verbose", "-v"],
            required=False,
            show_default=False,
            help="Increase verbosity level.",
        ),
    ] = [],
):
    """
    Default entry point for handling global options and configuring the application.

    This function is decorated with @app.default and processes global flags
    like verbosity before any subcommand is executed. It configures logging
    based on the verbosity flags.

    Subcommands are registered after this function definition.

    Args:
        verbose: A list of boolean flags indicating verbosity levels.
    """
    # Calculate verbosity level
    verbosity = sum(verbose)
    if very_verbose:
        verbosity = 2
    configure_logging(verbosity)

    logfire.instrument_system_metrics()

    with logfire.span("This is the main entry point of the CLI application."):
        logfire.info("Starting the Stadt Bonn OPARL Papers CLI application.")
        app(tokens)


app.meta.command(obj=download)

app.meta.command(convert)

app.meta.command(analyse_paper, name=["analyse", "classify", "classify-paper"])

app.meta.command(find)

app.meta.command(enrich)

app.meta.command(extract)

app.meta.command(vectordb)
