# Network Automation Libray

Python library for network automation

This contains various functions for network automation


## Installation

```shell
$ pip install network_automation
```

## Modules

### Cisco
This module provides various functions for working with Cisco devices using [netmiko](https://pypi.org/project/netmiko/) library.

### NetBox

This module extends the [pynetbox](https://pypi.org/project/pynetbox/) library with additional functions.

## Testing

The tests passed successfully with **Python 3.9**.

```shell
$ pip install pytest
$ pytest network_automation -v
```