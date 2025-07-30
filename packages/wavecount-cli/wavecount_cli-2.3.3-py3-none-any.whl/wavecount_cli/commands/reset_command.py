import re

import click
import inquirer as inq
from inquirer.themes import GreenPassion
from wavecount_cli.services.backend_services import Backend


@click.command(
    name="reset", help="Restart device services. Use options to filter devices"
)
@click.pass_context
@click.option("-v", "--firmware-version", help="Firmware version", is_eager=True)
@click.option(
    "-sn", "--serial-number", help="Device serial number", default=None, is_eager=True
)
@click.option(
    "-pn", "--part-number", help="Device part number", default=None, is_eager=True
)
@click.option("-id", "--device-id", help="Device id", default=None, is_eager=True)
@click.option("-n", "--device-name", help="Device name", default=None, is_eager=True)
@click.option("-c", "--company", help="Company name", default=None, is_eager=True)
@click.option("-st", "--store", help="Store name", default=None, is_eager=True)
@click.option(
    "-stn", "--store-number", help="Store number", default=None, is_eager=True
)
@click.option("-cl", "--cluster", help="Cluster name", default=None, is_eager=True)
def reset(
    ctx,
    firmware_version,
    serial_number,
    part_number,
    device_id,
    device_name,
    company,
    store,
    store_number,
    cluster,
):
    try:
        if (
            not firmware_version
            and not serial_number
            and not part_number
            and not device_id
            and not device_name
            and not company
            and not store
            and not store_number
            and not cluster
        ):
            click.secho(
                "You are trying to reboot all devices because no filters are defined!",
                fg="yellow",
            )
            confirm = False
            answer = inq.prompt(
                theme=GreenPassion(),
                raise_keyboard_interrupt=True,
                questions=[
                    inq.Confirm(name="confirm", message="Are you sure ?", default=False)
                ],
            )
            if answer is not None:
                confirm = answer["confirm"]
            if not answer or not confirm:
                exit(1)
        backend = Backend(ctx)
        query_params = {
            "firmwareVersion": firmware_version,
            "deviceId": device_id,
            "store": store,
            "storeNumber": store_number,
            "cluster": cluster,
            "company": company,
            "serialNumber": serial_number,
            "deviceName": device_name,
            "partNumber": part_number,
        }
        result = backend.reset_service(query_params)
        click.secho("")
        for key in result:
            row_length = 25
            splitted_key = re.findall(".[^A-Z]*", key)
            cap_splitted_key = [k.capitalize() for k in splitted_key]
            joined = " ".join(cap_splitted_key)
            txt = (
                "  {0}:".format(joined)
                + " " * (row_length - len(joined))
                + "{0}".format(result[key])
            )
            click.secho(txt, bold=True, fg="blue")
        click.secho()
    except BaseException:
        exit(1)
