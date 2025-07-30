import re
from datetime import datetime, timedelta

import click
import inquirer as inq
from inquirer.themes import GreenPassion
from wavecount_cli.services.backend_services import Backend


@click.command(
    name="hash", help="Calculate hash on devices. Use options to filter devices"
)
@click.pass_context
@click.option(
    "-sn", "--serial-number", help="Device serial number", default=None, is_eager=True
)
@click.option("-id", "--device-id", help="Device id", default=None, is_eager=True)
@click.option("-n", "--device-name", help="Device name", default=None, is_eager=True)
@click.option("-c", "--company", help="Company name", default=None, is_eager=True)
@click.option("-st", "--store", help="Store name", default=None, is_eager=True)
@click.option(
    "-stn", "--store-number", help="Store number", default=None, is_eager=True
)
@click.option("-t", "--time", help="Start date time", default=None, is_eager=True)
def calculate_hash(
    ctx, serial_number, device_id, device_name, company, store, store_number, time
):
    try:
        if (
            not serial_number
            and not device_id
            and not company
            and not store
            and not store_number
            and not device_name
        ):
            serial_number = inq.prompt(
                theme=GreenPassion(),
                raise_keyboard_interrupt=True,
                questions=[
                    inq.Text(
                        name="serial_number",
                        message="Enter serial_number",
                    ),
                ],
            )
        if not time:
            answer = inq.prompt(
                theme=GreenPassion(),
                raise_keyboard_interrupt=True,
                questions=[
                    inq.Text(
                        name="datetime",
                        message='Enter "datetime". format <YYYY-MM-DD HH:mm>',
                        default=str(
                            (datetime.now() - timedelta(days=1)).strftime(
                                "%Y-%m-%d %H:%M"
                            )
                        ),
                    )
                ],
            )
            if answer is not None:
                time = answer["datetime"] + ":00"
        backend = Backend(ctx)
        query_params = {
            "deviceId": device_id,
            "store": store,
            "storeNumber": store_number,
            "company": company,
            "serialNumber": serial_number,
            "deviceName": device_name,
        }
        result = backend.reset_hash_time(time, query_params)
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
    except Exception as e:
        exit(1)
