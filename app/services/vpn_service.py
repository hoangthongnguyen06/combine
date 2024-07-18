import subprocess
import requests
# Path to your OpenVPN configuration file
ovpn_file_path = "/path/to/your/config.ovpn"
# Path to your VPN credentials file (if needed)
vpn_creds_path = "/path/to/your/creds.txt"

def connect_vpn(ovpn_file, creds_file=None):
    command = ['openvpn', '--config', ovpn_file]
    if creds_file:
        command.extend(['--auth-user-pass', creds_file])
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


