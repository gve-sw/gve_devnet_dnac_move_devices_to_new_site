# GVE DevNet DNAC Move Devices to New Site
This prototype automates the process of moving Cisco Wireless LAN Controllers WLCs and Access Points APs from one DNAC site to another. 

The work flow is the following:
1. Delete the WLC from the inventory (this deletes the associated APs automatically).
2. Add the WLC back to the inventory (this adds the associated APs automatically as well). 
3. Provision the WLC.
4. Provision the APs.

## Contacts
* Roaa Alkhalaf
* Martin Jensen

## Solution Components
* DNAC
* DNAC REST APIs
* Python


## Installation/Configuration

The following commands are executed in the terminal.

1. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). 

2. (Optional) Set up a Python virtual environment. Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html). 

    2a. Access the created virtual environment folder

        $ cd your_venv

3. Clone this repository

        $ git clone https://wwwin-github.cisco.com/gve/gve_devnet_dnac_move_devices_to_new_site.git


4. Access the folder `gve_devnet_dnac_move_devices_to_new_site`

        $ cd gve_devnet_dnac_move_devices_to_new_site

5. Install the dependencies:

        $ pip3 install -r requirements.txt


## Pre-requistes 
1. In the `wlc_creds.json` file with the following credentials for the WLC that needs to be assigned to the new site: 
```
{
    "type":"NETWORK_DEVICE",
    "snmp_version": <string>,
    "snmp_ro_community": <string>,
    "snmp_rw_community": <string>,
    "snmp_retry": <integer>,
    "snmp_timeout": <integer>,
    "cli_transport": <string>,
    "username": <string>,
    "password": <string>,
    "enable_password": <string>,
    "netconf_port": <string>
}
```
2. In the `.env` file, fill out the following:

```
USERNAME= <DNAC username>
PASSWORD= <DNAC password>
BASE_URL= <DNAC IP address>

WLC_IP= <WLC IP address>
NEW_SITE= <New site hierarchy>
PROFILE= <AP RF-Profile name>

```
## Usage
1. To test the protype, type the following command in your terminal:

        $ python3 main.py

#
# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.