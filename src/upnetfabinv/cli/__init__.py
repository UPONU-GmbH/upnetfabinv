# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import click
import os

from upnetfabinv.resources import Config

from upnetfabinv.inventory.get_inventory import InventoryRenderer
from .netbox import netbox


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from click import Context


@click.group()
@click.pass_context
@click.option(
    "--config",
    help="Config file path.",
)
def cli(ctx: Context, config: str| None):
    ctx.ensure_object(dict)

    if config:
        config_path = config
    else:
        if os.path.exists(
            os.path.join(".upnetfabinv", "config.toml")):
            config_path = os.path.join(".upnetfabinv", "config.toml")
        elif  os.path.exists("config.toml"):
            config_path = "config.toml"

    ctx.obj["conf"] = Config(config_path)


@cli.group()
@click.option(
    "--out-path",
    required=True,
    help="Output for renderd files (inventory with host and group vars)",
)
@click.option("--override-path", default="override", help="Path to overrides")
@click.pass_context
def ansible_inventory(ctx: Context, out_path: str, override_path: str):
    ctx.obj["out_path"] = out_path
    ctx.obj["override_path"] = override_path


@ansible_inventory.command()
@click.pass_context
def all(ctx: Context):
    ctx.invoke(inventory)
    ctx.invoke(host_vars)


@ansible_inventory.command()
@click.pass_context
def inventory(ctx: Context):
    conf = ctx.obj["conf"]
    out_path = ctx.obj["out_path"]
    override_path = ctx.obj["override_path"]

    inventory_renderer = InventoryRenderer(conf)

    inventory_renderer.get_inventory(out_path, override_path)


@ansible_inventory.command()
@click.pass_context
def host_vars(ctx: Context):
    conf = ctx.obj["conf"]
    out_path = ctx.obj["out_path"]
    override_path = ctx.obj["override_path"]

    inventory_renderer = InventoryRenderer(conf)

    inventory_renderer.get_host_vars(out_path, override_path)


@ansible_inventory.command()
@click.pass_context
def group_vars(ctx: Context):
    conf = ctx.obj["conf"]
    out_path = ctx.obj["out_path"]
    override_path = ctx.obj["override_path"]

    inventory_renderer = InventoryRenderer(conf)

    inventory_renderer.get_group_vars(out_path, override_path)


cli.add_command(netbox)

if __name__ == "__main__":
    cli()
