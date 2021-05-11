#!/usr/bin/env python3

import json
import upnpclient
from linode_api4 import LinodeClient
from pathlib import Path

# Make sure we have the configuration
config_path = Path.home() / ".linode" / "linode-dynamic-dns.json"

if not config_path.exists():
    raise Exception(f"Could not find configuration file '{config_path}'")

with open(config_path) as file:
    config = json.load(file)

required_config_keys = ["domain", "subdomain", "token"]

for key in required_config_keys:
    if not key in config:
        raise Exception(f"Missing required configuration key: {key}")

domain_name    = config["domain"]
subdomain_name = config["subdomain"]
device_name    = config["device"] if "device" in config else None

# Trawl UPnP for the external IP address
external_ips = []

for device in upnpclient.discover():
    if device_name is not None and device_name != device.friendly_name:
        continue

    for service in device.services:
        if service.find_action("GetExternalIPAddress"):
            external_ips.append(service.GetExternalIPAddress()["NewExternalIPAddress"])

if len(external_ips) < 1:
    raise Exception("Found no external IP addresses")

if len(external_ips) > 1:
    raise Exception("Found more than one external IP address")

external_ip = external_ips[0]

# Find our domain and record
linode_client = LinodeClient(config["token"])

for domain in linode_client.domains():
    if domain.domain != domain_name:
        continue

    for record in domain.records:
        if record.name == subdomain_name:
            record.target=external_ip
            record.save()
            break
    else:
        domain.record_create(
            record_type="A",
            name=subdomain_name,
            target=external_ip
        )
