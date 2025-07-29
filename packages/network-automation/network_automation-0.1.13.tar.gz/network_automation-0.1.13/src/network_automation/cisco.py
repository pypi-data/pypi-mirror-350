import os
import logging
from network_automation import environment
from mydict import MyDict
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException


class CiscoSSHDevice(object):
    """
    This class defines methods for fetching data from a Cisco device using NetMiko
    """
    def __init__(self, hostname, username=None, password=None, device_type='cisco_ios'):
        if not hostname:
            raise ValueError("hostname is mandatory")

        self.hostname = hostname

        # Username and passwords can be provided as parameters or as environment variables
        self.username = username or environment.get_cisco_username()
        self.password = password or environment.get_cisco_password()

        # Only print console output if the VERBOSE environment variable is set to True or 1
        self.verbose = os.getenv("VERBOSE", "0").lower() in ["1", "true"]

        netmiko_device = {
            'device_type': device_type,
            'ip': self.hostname,
            'username': self.username,
            'password': self.password,
            'secret': self.password
        }
        try:
            self.conn = ConnectHandler(**netmiko_device)
            msg = f"Successfully connected to {hostname}"
            logging.info(msg)
            if self.verbose:
                print(msg)
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            raise ConnectionError(f"Failed to connect to {hostname}: {e}")

    def execute_show_command(self, command, parse=True, timeout=10):
        """
        This method executes a command on Cisco CLI and returns the result
        :param command: The command to run
        :param parse: Parse the output with textfsm (True)
        :param timeout: Set the timeout for executing the command and getting the result
        :return:
        """
        logging.info(f"Executing command '{command}' on {self.hostname}")

        result = self.conn.send_command(command, use_textfsm=parse, read_timeout=timeout)

        if type(result) is not str and self.verbose:
            print(f"Could not parse command result")

        return result

    def get_interface_details(self, timeout=30):
        """
        This method executes the 'show interface' command and returns the result parsed with textfsm
        :param timeout: Set the timeout for executing the command and getting the result
        :return:
        """
        interfaces = self.execute_show_command('show interface', timeout=timeout)

        return [MyDict(x) for x in interfaces]

    def get_cdp_neighbors(self, detail=False):
        """
        This method retrieves the CDP neighbors of the device
        :return:
        """
        if detail:
            command = 'show cdp neighbors detail'
        else:
            command = 'show cdp neighbors'

        return self.execute_show_command(command)

    def get_device_serial(self):
        """
        This method gets the serial number of a device
        :return:
        """
        serial = self.conn.send_command('show version | include Processor')

        return serial.split(' ')[-1]

    def get_ip_interface_brief(self):
        """
        This method gets interface IP information
        :return:
        """
        return [MyDict(x) for x in self.execute_show_command('show ip interface brief')]
