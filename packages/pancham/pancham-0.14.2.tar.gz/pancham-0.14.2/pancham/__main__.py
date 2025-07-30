from typing import Annotated, Optional

import typer

from .reporter_lib.halo_reporter import HaloReporter
from .reporter import get_reporter
from .runner import PanchamRunner
from .pancham_configuration import OrderedPanchamConfiguration

app = typer.Typer()

@app.command()
def run(
        configuration: Annotated[str, typer.Argument(help = "Path to the Pancham configuration file")],
        data_configuration: Annotated[Optional[str], typer.Argument(help = "Path to the data mapping if individual files are being used")] = None,
        test: Annotated[bool, typer.Option(help="Run all the tests")] = False
):
    print("Starting Pancham!")
    pancham_configuration = OrderedPanchamConfiguration(configuration)

    if pancham_configuration.reporter_name == 'spinner':
        reporter = get_reporter(pancham_configuration.debug_status, HaloReporter())
    else:
        reporter = get_reporter(pancham_configuration.debug_status)

    print(f"Reporter enabled - Debug = {pancham_configuration.debug_status}")
    runner = PanchamRunner(pancham_configuration, reporter = reporter)

    if data_configuration is not None:
        runner.load_and_run(data_configuration)
    else:
        if test:
            runner.run_all_tests()
        else:
            runner.run_all()
