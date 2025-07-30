import os

import click

from ..scenario.configurator import Configurator
from ..scenario.scenario import Scenario
from ..util.config_util import get_config_files, load_configs


def list_scenarios(configs):
    default_path = os.path.abspath(
        os.path.join(__file__, "..", "..", "scenario", "config")
    )

    files = get_config_files(configs, default_path)

    click.echo("Found the following scenarios:")

    for fil in files:
        configs = load_configs([fil])

        for key in configs:
            click.echo(f"* '{key}'  -->  {fil}")


def show(
    scenario_name,
    configs,
    sensors,
    actuators,
    keyword,
    negative_keywords,
    prefix,
):
    keywords = []
    if keyword:
        for kw in keyword:
            if "&" in kw:
                kws = kw.split("&")
                keywords.append(kws)
            else:
                keywords.append([kw])
        # click.echo(keywords)
        # return

    if configs is not None:
        if isinstance(configs, str):
            configs = (configs,)
        configs = [os.path.abspath(c) for c in configs]
    params = {}
    if sensors or actuators:
        params["with_arl"] = True
    configurator = Configurator()
    scenario = configurator.configure(
        scenario_name, params, configs, True, True
    )

    if sensors:
        to_print = []
        for sensor in scenario.sensors:
            uid = sensor["uid"]
            add_to_print = True
            if keywords:
                add_to_print = False
                for kwl in keywords:
                    add_to_print = add_to_print or _contains_all_keywords(
                        uid, kwl
                    )
                    if add_to_print:
                        break
            if negative_keywords:
                for kw in negative_keywords:
                    if kw in uid:
                        add_to_print = False
                        break

            if add_to_print:
                to_print.append(uid)
        for v in to_print:
            click.echo(f"{prefix}{v}")

    if actuators:
        to_print = []
        for actuator in scenario.actuators:
            uid = actuator["uid"]
            add_to_print = True
            if keywords:
                add_to_print = False
                for kwl in keywords:
                    add_to_print = add_to_print or _contains_all_keywords(
                        uid, kwl
                    )
                    if add_to_print:
                        break
            if negative_keywords:
                for kw in negative_keywords:
                    if kw in uid:
                        add_to_print = False
                        break

            if add_to_print:
                to_print.append(uid)
        for v in to_print:
            click.echo(f"{prefix}{v}")


def _contains_all_keywords(text, keywords):
    for kw in keywords:
        if kw not in text:
            return False
    return True
