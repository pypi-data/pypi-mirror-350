import click
from wavecount_cli.services.backend_services import Backend

dev_list_test = [
        {"company": "SDKJASHDJKSAHDKLJSHDKJSD",
        "store": "oaiuyqw8yeqiuyweuiwqe",
        "storeNumber": 1243,
        "serialNumber": "FDQ#WIOEUWQOIEUJW",
        "deviceName": "jflaiwhyerio7uew"},
            {"company": "asd",
        "store": "asd",
        "storeNumber": 1243,
        "serialNumber": "FDQ",
        "deviceName": "da"}
]


@click.command(name='update-fail', help='Show devices at failed update status')
@click.pass_context
def failed_update(ctx):
    try:
        backend = Backend(ctx)
        dev_list = backend.failed_update_devices()
        click.secho("")

        if not len(dev_list):
            click.secho(" Not Found ")
        else:
            row_len = 80
            block_len = round(row_len / 7)
            sep = '│'
            t_nom = ' #   '
            t_com = ' Company'
            t_sto = ' Store'
            t_stn = ' Storenumber'
            t_dNm = ' Device'
            t_srl = ' S/N'
            click.secho('╭' + '─' * (row_len + 5) + '╮')
            click.secho(sep + t_nom +
                        sep + t_com + ' ' * (block_len - len(t_com) + 8) +
                        sep + t_sto + ' ' * (block_len - len(t_sto) + 4) +
                        sep + t_stn + ' ' * (block_len - len(t_stn) + 4) +
                        sep + t_dNm + ' ' * (block_len - len(t_dNm)) +
                        sep + t_srl + ' ' * (block_len - len(t_srl) + 4) +
                        sep
                        )
            click.secho('╞' + '═' * (row_len + 5) + '╡')
            count = 0
            for device in dev_list:
                dev_name = device['deviceName'] if 'deviceName' in device else ' '
                serial_number = device['serialNumber'] if 'serialNumber' in device else ' '
                comp = device['company'] if 'company' in device else ' '
                store = device['store'] if 'store' in device else ' '
                store_number = device['storeNumber'] if 'storeNumber' in device else ' '
                dev_name = device['deviceName'] if 'deviceName' in device else ' '
                count += 1
                if len(comp) < len(t_com + ' ' * (block_len - len(t_com) + 8)):
                    company = ' {0}'.format(comp)
                else:
                    company = ' {0}..'.format(comp[0:(len(t_com + ' ' * (block_len - len(t_com) + 10)) - 5)])
                if len(store) < len(t_sto + ' ' * (block_len - len(t_sto) + 4)):
                    store = ' {0}'.format(store)
                else:
                    store = ' {0}..'.format(store[0:(len(t_sto + ' ' * (block_len - len(t_sto) + 4)) - 3)])
                store_number = ' {0}'.format(store_number)
                if len(dev_name) < len(t_dNm + ' ' * (block_len - len(t_dNm) + 4)):
                    device_name = ' {0}'.format(dev_name)
                else:
                    device_name = ' {0}..'.format(dev_name[0:(len(t_dNm + ' ' * (block_len - len(t_dNm))) - 3)])
                if len(serial_number) < len(t_srl + ' ' * (block_len - len(t_srl) + 4)):
                    serial_number = ' {0}'.format(serial_number)
                else:
                    serial_number = ' {0}..'.format(serial_number[0:(len(t_srl + ' ' * (block_len - len(t_srl) + 4)) - 3)])
                click.secho(sep + ' ' + str(count) + ' ' * (4 - len(str(count))) +
                            sep + company + ' ' * (block_len - len(company) + 8) +
                            sep + store + ' ' * (block_len - len(store) + 4) +
                            sep + store_number + ' ' * (block_len - len(store_number) + 4) +
                            sep + device_name + ' ' * (block_len - len(device_name)) +
                            sep + serial_number + ' ' * (block_len - len(serial_number) + 4) +
                            sep
                            )
            click.secho('╰' + '─' * (row_len + 5) + '╯')
            click.echo()
    except Exception as e:
        exit()
