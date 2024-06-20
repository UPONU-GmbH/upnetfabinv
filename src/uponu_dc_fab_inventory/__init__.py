import pynetbox

def main():

    # Replace with your NetBox URL and API token
    NETBOX_URL = 'http://127.0.0.1:8000'
    NETBOX_API_TOKEN = '115ace3a67cf5015dbdb31d647ffbd04340af7bb'

    # Initialize the pynetbox API
    nb = pynetbox.api(NETBOX_URL, token=NETBOX_API_TOKEN)

    # Specify the site and role you are interested in
    site_name = 'SI03'
    role_name = 'Spine-Leaf Network'

    # Get the site ID by filtering the sites by name
    site = nb.dcim.sites.get(name=site_name)
    if not site:
        print(f"No site found with the name {site_name}")
        exit()

    # Get the role ID by filtering the device roles by name
    role = nb.dcim.device_roles.get(name=role_name)
    if not role:
        print(f"No role found with the name {role_name}")
        exit()

    # Get devices by site ID and role ID
    devices = nb.dcim.devices.filter(site_id=site.id, role_id=role.id)

    # Print the devices
    for device in devices:
        print(f"Device Name: {device.name}, Device ID: {device.id}, Role: {device.device_role.name}, Site: {device.site.name}")

if __name__ == "__main__":
    main()