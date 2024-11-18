# UPONU DC Fabric python netbox inventory - upnetfabinv

Project to generate an invetory file, host vars and group vars from netbox.

It is possible to add additional variables and overrides.

## Installation

```
pip install -r requirements-dev.txt
```

## Config (example)

### config.toml
```toml
[fabric]

name = ""
device_role_name = "Spine-Leaf Network" # Devie role
availability_zones = [
    # Sites in netbox
    "Site1",
]

[netbox]

NETBOX_URL = "http://127.0.0.1:8001"
NETBOX_API_TOKEN = ""
NETBOX_VERIFY_SSL = false # do not verify ssl if using local instance

[netbox.dcim_devices_default_filter]
status= "active" # use only active devices
```


## Usage

```
Usage: upnetfabinv [OPTIONS] COMMAND [ARGS]...

Options:
  --config TEXT  Config file path.
  --help         Show this message and exit.

Commands:
  ansible-inventory     Build ansible inventory
  netbox                Setup netbox
```

```
Usage: upnetfabinv ansible-inventory [OPTIONS] COMMAND [ARGS]...

Options:
  --out-path TEXT       Output for renderd files (inventory with host and
                        group vars)  [required]
  --override-path TEXT  Path to overrides
  --help                Show this message and exit.

Commands:
  all                   Generate group_vars, host_vars and inventory.yml
  group-vars            Generates group_vars
  host-vars             Generates host_vars
  inventory             Generates inventory.yml
```
