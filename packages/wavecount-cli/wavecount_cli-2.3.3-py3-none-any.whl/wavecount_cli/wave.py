import os
import sys

import click
import pyfiglet
import inquirer as inq
from inquirer.themes import GreenPassion

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from wavecount_cli import VERSION
from wavecount_cli.commands.change_commands import change
from wavecount_cli.commands.delete_commands import delete
from wavecount_cli.commands.hash_command import calculate_hash
from wavecount_cli.commands.new_commands import new
from wavecount_cli.commands.reboot_commands import reboot
from wavecount_cli.commands.reset_command import reset
from wavecount_cli.commands.failed_update_commands import failed_update
from wavecount_cli.commands.show_commands import show
from wavecount_cli.commands.update_commands import update
from wavecount_cli.services.backend_services import Backend
from wavecount_cli.utils import read_config, save_config
from wavecount_cli.version_check import compare_versions


@click.group(name="main", help="Wavecount CLI for controlling and monitoring things!")
@click.pass_context
def main(ctx):
    compare_versions()
    ctx.obj = read_config()
    if "roles" not in ctx.obj:
        ctx.forward(login)
    pass


@click.command("sync", help="Synchronize cache.")
@click.option("-t", "--access-token", type=click.STRING, help="Your access token")
@click.pass_context
def sync(ctx, access_token, **kwarg):
    if not access_token:
        if "access_token" not in ctx.obj:
            ctx.forward(login)
        else:
            access_token = ctx.obj["access_token"]
    backend = Backend(context=ctx)
    result = backend.sync_cache()
    ctx.obj = {**ctx.obj, **result}
    save_config(ctx.obj)


@click.command("login", help="Authorize user.")
@click.pass_context
def login(ctx):
    try:
        username = ""
        password = ""
        answer = inq.prompt(
            questions=[
                inq.Text(
                    name="username",
                    message="Enter username",
                ),
            ],
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )
        if answer is not None:
            username = answer["username"]

        answer = inq.prompt(
            questions=[
                inq.Password(
                    name="password",
                    message="Enter password",
                ),
            ],
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )
        if answer is not None:
            password = answer["password"]
        backend = Backend(context=ctx)
        response = backend.login({"user": username, "password": password})
        ctx.obj["name"] = response["name"]
        ctx.obj["roles"] = response["roles"]
        ctx.obj["access_token"] = response["accessToken"]
        ctx.forward(sync)
        text_logo = "wavecount cli"
        pyfiglet.print_figlet(text=text_logo, font="big", justify="center")
        click.secho()
        click.secho(
            bold=True,
            fg="blue",
            message="Welcome {}!".format(response["name"].split(" ")[0]),
        )
        click.secho()
        click.echo(
            "Now run:" + click.style(text=" {} --help".format("wave"), fg="blue")
        )
        click.secho()
    except Exception as e:
        exit()


@click.command("version", help="Show version.")
@click.pass_context
def version(ctx):
    message = "using version: {0}".format(VERSION)
    click.secho(message, fg="bright_black")


main.add_command(sync)
main.add_command(login)
main.add_command(show)
main.add_command(new)
main.add_command(update)
main.add_command(reboot)
main.add_command(delete)
main.add_command(reset)
main.add_command(version)
main.add_command(change)
main.add_command(calculate_hash)
main.add_command(failed_update)

if __name__ == "__main__":
    main()
