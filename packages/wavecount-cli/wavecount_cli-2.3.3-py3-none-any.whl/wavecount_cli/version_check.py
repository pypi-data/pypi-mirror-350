import math
import click
import requests
from halo import Halo
from wavecount_cli import PACKAGE_NAME, VERSION


class Version:
    """Represents a version and provides parsing utilities."""

    def __init__(self, version_str):
        self.version_tuple = self._parse_version(version_str)

    def _parse_version(self, version_str):
        """Parse a version string into a tuple of integers."""
        try:
            return tuple(map(int, version_str.split(".")))
        except ValueError:
            return (0,)


def get_current_version():
    """Retrieve the current version of the package."""
    return Version(VERSION).version_tuple


def get_latest_version():
    """Fetch the latest version of the package from PyPI."""
    pypi_url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
    with Halo(spinner="dots3", text_color="grey") as spinner:
        try:
            response = requests.get(pypi_url, timeout=2)
            response.raise_for_status()
            latest_version = response.json()["info"]["version"]
            return Version(latest_version).version_tuple
        except requests.ConnectionError as err:
            spinner.fail("Connection Error: Ensure you are connected to the Internet.")
            raise RuntimeError(f"Connection Error: {err}")
        except requests.Timeout as err:
            spinner.fail("Timeout Error: Update check timed out.")
            raise RuntimeError(f"Timeout Error: {err}")
        except requests.RequestException as err:
            spinner.fail("General Error: Failed to check for updates.")
            raise RuntimeError(f"Request Error: {err}")
        except KeyboardInterrupt:
            spinner.fail("Update check interrupted by user.")
            raise RuntimeError("Update check interrupted.")


def compare_versions():
    """Compare the current version with the latest version and notify the user."""
    try:
        current_version = get_current_version()
        with Halo(spinner="dots3", text_color="grey") as spinner:
            spinner.start("Checking version")
            latest_version = get_latest_version()

            if current_version < latest_version:
                spinner.warn("Out-of-date")
                display_update_message(current_version, latest_version)
                return latest_version
            else:
                spinner.succeed("Up-to-date")
    except RuntimeError as e:
        click.secho(f"Error: {e}", fg="red")
    except Exception as e:
        click.secho(f"Unexpected error: {e}", fg="red")
        raise


def display_update_message(current_version, latest_version):
    """Display a message to the user about the available update."""
    cl = 60
    click.echo("\n")
    click.secho("╭" + (cl - 2) * "─" + "╮", fg="yellow")
    click.secho("│" + (cl - 2) * " " + "│", fg="yellow")
    avail_msg = f"Update available {'.'.join(map(str, current_version))} → {'.'.join(map(str, latest_version))}"
    click.secho(
        "│"
        + math.ceil((cl - 2 - len(avail_msg)) / 2) * " "
        + avail_msg
        + math.floor((cl - 2 - len(avail_msg)) / 2) * " "
        + "│",
        fg="yellow",
    )
    hint_msg = (
        click.style("Run ", fg="yellow")
        + click.style(f"pip3 install --upgrade {PACKAGE_NAME} ", fg="blue")
        + click.style("to update", fg="yellow")
    )
    click.secho(
        click.style("│", fg="yellow")
        + math.floor((cl - 2 - 50) / 2) * " "
        + hint_msg
        + math.floor((cl - 2 - 50) / 2) * " "
        + click.style("│", fg="yellow")
    )
    click.secho("│" + (cl - 2) * " " + "│", fg="yellow")
    click.secho("╰" + (cl - 2) * "─" + "╯", fg="yellow")
    click.secho()
