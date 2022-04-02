# Third party imports
from typer.testing import CliRunner

# Local imports
from porclr import __app_name__, __app_version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__app_version__}\n" in result.stdout
