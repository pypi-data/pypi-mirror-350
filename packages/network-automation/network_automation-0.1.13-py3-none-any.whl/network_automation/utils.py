def ip_reachable(host):
    """
    Checks if a host responds to a ping request.
    :param host: Hostname or IP address to be checked
    :return: True if the host is alive, false otherwise
    """
    import platform
    import subprocess

    # Option for the number of packets as a function of
    count = '-n' if platform.system().lower() == 'windows' else '-c'
    wait = '-w' if platform.system().lower() == 'windows' else '-W'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', count, '2', wait, '5', host]

    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0
