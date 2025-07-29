import logging
import os
import pathlib
import sys
from dotenv import load_dotenv

# Get environment variables from local .env file and user's home directory .env file
dotenv_current_path = os.path.join(pathlib.Path().resolve(), '.env')
dotenv_home_path = os.path.join(pathlib.Path.home().resolve(), '.env')
load_dotenv(dotenv_home_path)
load_dotenv(dotenv_current_path)

# Logging config
if sys.version_info.major >= 3 and sys.version_info.minor >= 9:
    logging.basicConfig(filename='network_automation.log',
                        encoding='utf-8',
                        level=logging.INFO,
                        format='%(levelname)s:%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
else:
    logging.basicConfig(filename='network_automation.log',
                        level=logging.INFO,
                        format='%(levelname)s:%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')

# GENERAL SETTINGS
VERBOSE = False
if 'VERBOSE' in os.environ and (
        os.environ["VERBOSE"].lower() == "true"
        or os.environ["VERBOSE"].lower() == "yes"
        or os.environ["VERBOSE"] == 1):
    VERBOSE = True

DEBUG = False
if 'DEBUG' in os.environ and (
        os.environ["DEBUG"].lower() == "true"
        or os.environ["DEBUG"].lower() == "yes"
        or os.environ["DEBUG"] == 1):
    DEBUG = True


def get_cisco_username():
    """Get username for Cisco devices from environment variables"""
    return os.environ.get("CISCO_USERNAME")


def get_cisco_password():
    """Get password for Cisco devices from environment variables"""
    return os.environ.get("CISCO_PASSWORD")


def get_netbox_url():
    """Get URL for NetBox from environment variables"""
    return os.environ.get("NETBOX_URL")


def get_netbox_token():
    """Get token for NetBox from environment variables"""
    return os.environ.get("NETBOX_TOKEN")
