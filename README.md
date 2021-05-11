# linode-dynamic-dns
Tiny script to set a Linode DNS domain record to point to the external IP address of the machine on which the script is run.

_No guarantees are made as to whether this will work as expected, or at all. **Use at your own risk.**_

## Limitations

* Only handles one IP
* Only handles one domain
* Only handles one subdomain
* Only handles A record
* ...

# Requirements
* [upnpclient](https://pypi.org/project/upnpclient/)
* [linode_api4](https://pypi.org/project/linode-api4/)

# Configuration

The script looks for its configuration in `~/.linode/linode-dynamic-dns.json`, and expects:

```
{
    "domain":"example.com",
    "subdomain":"dynamic",
    "token": "<personal access token>",
    "device": null
}
```

* The token must have read/write permission for Domains. No other permissions are required.
* The device is optional - it's mostly there in case you have a lot of UPnP devices to iterate, or ones that misbehave.
