from email import message
import click
import inquirer as inq
from inquirer.themes import GreenPassion
from wavecount_cli.services.backend_services import Backend


@click.command(name="delete", help="Delete devices. Use options to filter devices")
@click.pass_context
@click.option("-sn", "--serial-number", help="Device serial number")
@click.option("-id", "--device-id", help="Device id", default=None)
def delete(ctx, serial_number, device_id):
    try:
        if not serial_number and not device_id:
            answer = inq.prompt(
                questions=[
                    inq.Text(name="serial_number", message="Enter serial_number")
                ],
                theme=GreenPassion(),
                raise_keyboard_interrupt=True,
            )
            if answer is not None:
                serial_number = answer["serial_number"]
        backend = Backend(ctx)
        where = {
            "deviceId": device_id,
            "serialNumber": serial_number,
        }
        dev = backend.get_devices_list(where)
        if len(dev) == 0:
            click.secho("  DEVICE NOT FOUND!", fg="yellow")
            exit(1)
        confirm = False
        answer = inq.prompt(
            questions=[
                inq.Confirm(
                    name="confirm",
                    default=False,
                    message='Are you sure to delete the "{0}" device ?'.format(
                        dev[0]["store"]
                    ),
                )
            ],
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )
        if answer is not None:
            confirm = answer["confirm"]
        if confirm:
            backend.delete_device(device_id=dev[0]["deviceId"])
    except Exception as e:
        exit(1)
