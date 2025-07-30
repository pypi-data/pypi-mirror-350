import click
import pydash as _
import inquirer as inq
from inquirer.themes import GreenPassion
from wavecount_cli.services.backend_services import Backend


@click.command(name="new", help="Register a new device.")
@click.pass_context
def new(ctx):
    try:
        answer = {}
        request_payload = {}
        roles: str = ctx.obj["roles"]
        backend_service = Backend(context=ctx)
        result = backend_service.sync_cache()
        companies = result["companies"]
        company_choices = ["new", *_.map_(companies, "company")]
        part_numbers = result["partNumbers"]
        part_numbers_choices = []
        contracts_list = result["contracts"]
        if roles == "admin":
            part_numbers_choices.extend(["new"])
        part_numbers_choices.extend(part_numbers)
        answer = inq.prompt(
            questions=[
                inq.Text(
                    name="serial_number",
                    message="Enter serial",
                ),
                inq.List(
                    name="part_number",
                    message='Wich "part number"',
                    choices=part_numbers_choices,
                ),
            ],
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )

        if answer is not None:
            serial_number: str = answer["serial_number"]
            request_payload["serialNumber"] = serial_number
            part_number: str = answer["part_number"]
            request_payload["partNumber"] = part_number
            if part_number == "new":
                answer = inq.prompt(
                    theme=GreenPassion(),
                    raise_keyboard_interrupt=True,
                    questions=[
                        inq.Text(
                            name="part_number",
                            message="Enter part_number",
                        ),
                    ],
                )
                if answer is not None:
                    part_number: str = answer["part_number"]
                request_payload["partNumber"] = part_number
        answer = inq.prompt(
            questions=[
                inq.List(
                    name="company", message='Wich "company"', choices=company_choices
                )
            ],
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )
        if answer is not None:
            company: str = answer["company"]
            request_payload["company"] = company
            if company == "new":
                answers = inq.prompt(
                    theme=GreenPassion(),
                    raise_keyboard_interrupt=True,
                    questions=[
                        inq.Text(
                            name="company",
                            message="Enter company",
                        ),
                        inq.List(
                            name="contract",
                            message='Wich "contract"',
                            choices=_.map_(contracts_list, "title"),
                        ),
                        inq.Text(
                            name="store",
                            message="Enter store",
                        ),
                        inq.Text(
                            name="store_number",
                            message='Enter "store number"',
                        ),
                    ],
                )
                if answers is not None:
                    company: str = answers["company"]
                    request_payload["company"] = company
                    contract: str = answers["contract"]
                    contractId = _.find(contracts_list, {"title": contract})[
                        "contractID"
                    ]
                    request_payload["contractID"] = contractId
                    store: str = answers["store"]
                    store_number: int = int(answers["store_number"])
                    request_payload["store"] = store
                    request_payload["storeNumber"] = store_number
            else:
                store_choices = ["new"]
                company_item = _.find(companies, {"company": company})

                if company_item is not None:
                    stores_items = company_item["stores"]
                    stores = _.uniq(_.map_(stores_items, "store"))
                    store_choices.extend(stores)
                answer = inq.prompt(
                    theme=GreenPassion(),
                    raise_keyboard_interrupt=True,
                    questions=[
                        inq.List(
                            name="store", message="Enter store", choices=store_choices
                        )
                    ],
                )
                if answer is not None:
                    store: str = answer["store"]
                    request_payload["store"] = store
                    if store == "new":
                        answer = inq.prompt(
                            theme=GreenPassion(),
                            raise_keyboard_interrupt=True,
                            questions=[
                                inq.Text(
                                    name="store",
                                    message="Enter store",
                                ),
                                inq.Text(
                                    name="store_number",
                                    message="Enter store number",
                                ),
                            ],
                        )
                        if answer is not None:
                            store: str = answer["store"]
                            store_number: int = int(answer["store_number"])
                            request_payload["store"] = store
                            request_payload["storeNumber"] = store_number
                    else:
                        store_item = _.find(stores_items, {"store": store})
                        if store_item is not None:
                            store_number: int = store_item["storeNumber"]
                            request_payload["storeNumber"] = store_number
        device = backend_service.register_device(request_payload)
        dev_id = device["deviceId"]
        prim_key = device["symmetricKey"]["primaryKey"]
        comp = device["company"]
        store = device["store"]
        store_num = device["storeNumber"]
        sn = device["serialNumber"]
        pn = device["partNumber"]
        click.secho(" Part Number:    {}".format(pn), fg="green")
        click.secho(" Serial Number:  {}".format(sn), fg="green")
        click.secho(" Device Id:      {}".format(dev_id), fg="green")
        click.secho(" Primary Key:    {}".format(prim_key), fg="green")
        click.secho(" Company:        {}".format(comp), fg="green")
        click.secho(" Store:          {}".format(store), fg="green")
        click.secho(" Store Number:   {}".format(store_num), fg="green")
        click.secho()
    except Exception as e:
        exit(1)
