# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
import click
import yaml

from uponu_dc_fab_inventory.resources import Config

from uponu_dc_fab_inventory.inventory.get_inventory import InventoryRenderer

@click.group()
def cli():
    pass

@cli.command()
def run():

    conf = Config("examples/config.toml")
    
    inventory_renderer = InventoryRenderer(conf)

    inventory_renderer.get_inventory()

@cli.command()
def host_vars():

    conf = Config("examples/config.toml")
    
    inventory_renderer = InventoryRenderer(conf)

    inventory_renderer.get_host_vars()


@cli.command()
def config():

    conf = Config("examples/config.toml")

    print(conf.get("fabric.device_role_name"))

    
if __name__ == '__main__':
    cli()