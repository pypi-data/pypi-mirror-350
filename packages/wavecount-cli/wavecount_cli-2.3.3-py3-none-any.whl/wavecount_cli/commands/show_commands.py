import datetime

import click
import pydash as _
import inquirer as inq
from inquirer.themes import GreenPassion
from wavecount_cli.services.backend_services import Backend


@click.group(
    name="show",
    add_help_option=False,
    short_help="Subcommands: [device, company, connection]",
    help="Show commands managements",
)
def show():
    pass


@click.command(
    name="device",
    short_help="Show devices.",
    context_settings={"ignore_unknown_options": True},
)
@click.pass_context
@click.argument("args", default=None, required=False)
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
def device(
    ctx,
    args,
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
    """
    Show devices. Use options to filter devices list where [ARGS] can be:
    `test`: test mode devices
    `outup`: out-of-date devices [UNAVAILABLE]
    """
    backend_service = Backend(ctx)
    if args is not None and "test" in args:
        test_mode = "1"
    else:
        test_mode = "0"
    where = {
        "testMode": test_mode,
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
    dev_list = backend_service.get_devices_list(where)
    if dev_list and len(dev_list):
        if serial_number:
            for device in dev_list:
                comp = device["company"] if "company" in device else " "
                store = device["store"] if "store" in device else " "
                dev_name = device["deviceName"] if "deviceName" in device else " "
                store_number = device["storeNumber"] if "storeNumber" in device else " "
                sn = device["serialNumber"] if "serialNumber" in device else " "
                pn = device["partNumber"] if "partNumber" in device else " "
                inst_name = (
                    device["installerName"] if "installerName" in device else " "
                )
                inst_date = (
                    device["installingDate"] if "installingDate" in device else " "
                )
                firm_ver = (
                    device["firmwareVersion"] if "firmwareVersion" in device else " "
                )
                firm_upd = (
                    device["firmwareUpdatedDate"]
                    if "firmwareUpdatedDate" in device
                    else " "
                )
                firm_upd_state = (
                    device["updateState"] if "updateState" in device else " "
                )
                uptodate = device["uptodate"] if "uptodate" in device else " "
                dev_private_ip = device["deviceIP"] if "deviceIP" in device else " "
                dev_public_ip = device["publicIP"] if "publicIP" in device else " "
                mac_add = device["macAddress"] if "macAddress" in device else " "
                door_w = device["doorWidth"] if "doorWidth" in device else " "
                door_h = device["deviceHeight"] if "deviceHeight" in device else " "
                dist_from_door = (
                    device["distanceFromDoor"] if "distanceFromDoor" in device else " "
                )
                gat = (
                    " - ".join(device["gatingParam"].split(" "))
                    if "gatingParam" in device
                    else " "
                )
                scen = (
                    " - ".join(device["sceneryParam"].split(" "))
                    if "sceneryParam" in device
                    else " "
                )
                state = (
                    " - ".join(device["stateParam"].split(" "))
                    if "stateParam" in device
                    else " "
                )
                alloc = (
                    " - ".join(device["allocationParam"].split(" "))
                    if "allocationParam" in device
                    else " "
                )
                x1 = (
                    device["calibrationLine"]["x1"]
                    if _.has(device, "calibrationLine.x1")
                    else " "
                )
                y1 = (
                    device["calibrationLine"]["y1"]
                    if _.has(device, "calibrationLine.y1")
                    else " "
                )
                x2 = (
                    device["calibrationLine"]["x2"]
                    if _.has(device, "calibrationLine.x2")
                    else " "
                )
                y2 = (
                    device["calibrationLine"]["y2"]
                    if _.has(device, "calibrationLine.y2")
                    else " "
                )
                dev_id = device["deviceId"] if "deviceId" in device else " "
                dev_info = backend_service.get_device_info(device_id=dev_id)
                prim_key = (
                    dev_info["symmetricKeys"]["primaryKey"]
                    if _.has(dev_info, "symmetricKeys.primaryKey")
                    else " "
                )
                current_angle = (
                    device["currentAngle"] if "currentAngle" in device else " "
                )
                reference_angle = (
                    device["referenceAngle"] if "referenceAngle" in device else " "
                )
                click.secho()
                click.secho("  Company:                  {0}".format(comp))
                click.secho("  Store:                    {0}".format(store))
                click.secho("  Device:                   {0}".format(dev_name))
                click.secho("  Store Number:             {0}".format(store_number))
                click.secho("  Serial Number:            {0}".format(sn))
                click.secho("  Part Number:              {0}".format(pn))
                click.secho(
                    "  Installer:                {0} [{1}]".format(inst_name, inst_date)
                )
                click.secho(
                    "  Firmware Version:         {0} [{1}]".format(
                        click.style(
                            firm_ver,
                            fg="yellow" if not uptodate else None,
                            blink=not uptodate,
                        ),
                        firm_upd,
                    )
                )
                click.secho("  Update State:             {0}".format(firm_upd_state))
                click.secho("  Private IP:               {0}".format(dev_private_ip))
                click.secho("  Public IP:                {0}".format(dev_public_ip))
                click.secho("  Mac Address:              {0}".format(mac_add))
                click.secho("  Reference Angle:          {0}".format(reference_angle))
                click.secho("  Current Angle:            {0}".format(current_angle))
                click.secho("  Door Width:               {0}".format(door_w))
                click.secho("  Device Height:            {0}".format(door_h))
                click.secho("  Distance From Door:       {0}".format(dist_from_door))
                click.secho("  Gating Params:            {0}".format(gat))
                click.secho("  Scenery Params:           {0}".format(scen))
                click.secho("  State Params:             {0}".format(state))
                click.secho("  Allocation Params:        {0}".format(alloc))
                click.secho(
                    "  Calibration Lines:        [x1: {0} , y1: {1}] - [x2: {2} , y2: {3}]".format(
                        str(x1), str(y1), str(x2), str(y2)
                    )
                )
                click.secho("  Device Id:                {0}".format(dev_id))
                click.secho("  Primary Key:              {0}".format(prim_key))
                click.secho()
        else:
            row_len = 100
            block_len = round(row_len / 7)
            sep = "│"
            t_nom = " #   "
            t_com = " Company"
            t_sto = " Store"
            t_stn = " Storenumber"
            t_dNm = " Device"
            t_srl = " S/N"
            t_ver = " Firmware Version"
            t_upd = " Updating State"
            click.secho("╭" + "─" * (row_len + 30) + "╮")
            click.secho(
                sep
                + t_nom
                + sep
                + t_com
                + " " * (block_len - len(t_com) + 2)
                + sep
                + t_sto
                + " " * (block_len - len(t_sto) + 5)
                + sep
                + t_stn
                + " " * (block_len - len(t_stn) - 4)
                + sep
                + t_dNm
                + " " * (block_len - len(t_dNm))
                + sep
                + t_srl
                + " " * (block_len - len(t_srl))
                + sep
                + t_ver
                + " " * (block_len - len(t_ver) + 5)
                + sep
                + t_upd
                + " " * (block_len - len(t_upd) + 10)
                + sep
            )
            click.secho("╞" + "═" * (row_len + 30) + "╡")
            count = 0
            for device in dev_list:
                dev_name = device["deviceName"] if "deviceName" in device else " "
                serial_number = (
                    device["serialNumber"] if "serialNumber" in device else " "
                )
                comp = device["company"] if "company" in device else " "
                store = device["store"] if "store" in device else " "
                store_number = device["storeNumber"] if "storeNumber" in device else " "
                dev_name = device["deviceName"] if "deviceName" in device else " "
                uptodate = device["uptodate"] if "uptodate" in device else " "
                firm_ver = (
                    device["firmwareVersion"] if "firmwareVersion" in device else " "
                )
                firm_upd_state = (
                    device["updateState"] if "updateState" in device else " "
                )
                count += 1
                if len(comp) < len(t_com + " " * (block_len - len(t_com) + 2)):
                    company = " {0}".format(comp)
                else:
                    company = " {0}..".format(
                        comp[0 : (len(t_com + " " * (block_len - len(t_com) + 4)) - 5)]
                    )
                if len(store) < len(t_sto + " " * (block_len - len(t_sto) + 5)):
                    store = " {0}".format(store)
                else:
                    store = " {0}..".format(
                        store[0 : (len(t_sto + " " * (block_len - len(t_sto) + 5)) - 3)]
                    )
                store_number = " {0}".format(store_number)
                if len(firm_ver) < len(t_ver + " " * (block_len - len(t_ver) + 5)):
                    firm_ver = "{0}".format(firm_ver)
                else:
                    firm_ver = "{0}..".format(
                        firm_ver[
                            0 : (len(t_ver + " " * (block_len - len(t_ver) + 2)) - 3)
                        ]
                    )
                if firm_upd_state == "successfully updated":
                    firm_upd_state = " "
                if len(firm_upd_state) < len(
                    t_upd + " " * (block_len - len(t_upd) + 10)
                ):
                    firm_upd_state = " {0}".format(firm_upd_state)
                else:
                    firm_upd_state = " {0}..".format(
                        firm_upd_state[
                            0 : (len(t_upd + " " * (block_len - len(t_upd) + 10)) - 3)
                        ]
                    )

                device_name = " {0}".format(dev_name)
                serial_number = " {0}".format(serial_number)
                click.secho(
                    sep
                    + " "
                    + str(count)
                    + " " * (4 - len(str(count)))
                    + sep
                    + company
                    + " " * (block_len - len(company) + 2)
                    + sep
                    + store
                    + " " * (block_len - len(store) + 5)
                    + sep
                    + store_number
                    + " " * (block_len - len(store_number) - 2)
                    + sep
                    + device_name
                    + " " * (block_len - len(device_name))
                    + sep
                    + serial_number
                    + " " * (block_len - len(serial_number))
                    + sep
                    + " "
                    + click.style(firm_ver, fg="yellow" if not uptodate else None)
                    + " " * (block_len - len(firm_ver) + 4)
                    + sep
                    + click.style(firm_upd_state)
                    + " " * (block_len - len(firm_upd_state) + 10)
                    + sep
                )
            click.secho("╰" + "─" * (row_len + 30) + "╯")
            click.echo()
    else:
        click.secho("  NO DEVICE WAS FOUND!", fg="yellow")


@click.command(name="company", help="Show company information.")
@click.pass_context
@click.option("-c", "--company", help="Company name", default=None, is_eager=True)
def company(ctx, company):
    backend_service = Backend(ctx)
    result = backend_service.sync_cache()
    companies = result["companies"]
    company_choices = _.map_(companies, "company")
    if not company:
        answer = inq.prompt(
            questions=[
                {
                    "type": "list",
                    "name": "company",
                    "message": 'Wich "company"',
                    "choices": company_choices,
                }
            ],
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )
        if answer is not None:
            company = answer["company"]
    customer_info = backend_service.get_company_info(company)
    contract_title = _.find(
        result["contracts"], {"contractID": customer_info["contractID"]}
    )
    click.secho("")
    click.secho("  Contract:         {0}".format(contract_title), fg="yellow")
    click.secho(
        "  Device Count:     {0}".format(str(customer_info["deviceCount"])), fg="yellow"
    )
    click.secho(
        "  Store Count:      {0}".format(str(customer_info["storeCount"])), fg="yellow"
    )
    click.secho("")


@click.command(
    name="connection", help="Get a device connections. Use options to filter device"
)
@click.option("-sn", "--serial-number", help="Device serial number")
@click.option("-id", "--device-id", help="Device id", default=None)
@click.option("-li", "--limit", help="How many events?", default=None)
@click.pass_context
def connection(ctx, serial_number, device_id, limit):
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
        if not limit:
            answer = inq.prompt(
                questions=[inq.Text(message="How many events?", name="limit")],
                theme=GreenPassion(),
                raise_keyboard_interrupt=True,
            )
            if answer is not None:
                limit = int(answer["limit"])
        backend = Backend(ctx)
        events = backend.get_connectivity_events(
            device_id=device_id, serial_number=serial_number, limit=limit
        )

        if len(events) == 0:
            click.secho("  NOT FOUND", fg="green")
            click.echo()
            exit(1)
        else:
            click.echo()
            row_num = 1
            for ef in events:
                sep = "│"
                com = " {0}".format(ef["Company"])
                sto = " {0}".format(ef["Store"])
                devName = " Device {0}".format(ef["DeviceName"])
                dte = " {0}".format(
                    get_timestamp(ef["EventDateKey"], ef["EventTimeKey"])
                )
                event = " {0}".format(ef["UniqueKey"]).split(".")[1]
                click.secho(
                    sep
                    + " "
                    + str(row_num)
                    + (4 - len(str(row_num))) * " "
                    + " "
                    + sep
                    + " "
                    + com
                    + " "
                    + sep
                    + " "
                    + sto
                    + " "
                    + sep
                    + " "
                    + devName
                    + " "
                    + sep
                    + " "
                    + dte
                    + " "
                    + "├"
                    + " "
                    + event
                )
                row_num += 1
            click.echo()
    except Exception as e:
        exit()


def get_timestamp(date_key, time_key):
    # Convert DateKey and TimeKey to strings
    date_str = str(date_key)
    time_str = str(time_key)

    # Parse the strings to create datetime objects
    date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
    time_obj = datetime.datetime.strptime(time_str, "%H%M%S")

    # Combine date and time objects to create the timestamp
    timestamp = datetime.datetime.combine(date_obj.date(), time_obj.time())
    return timestamp


show.add_command(device)
show.add_command(company)
show.add_command(connection)
