import subprocess
import time

# VPN server details
vpn_config_file = "path/to/your/config.vpn"
vpn_user_name = "your_vpn_username"
vpn_password = "your_vpn_password"

def connect_vpn(config_file, username, password):
    # Command to import the VPN configuration
    import_command = [
        'vpncmd', 'localhost', '/CLIENT', '/CMD',
        'AccountImport', 'VPN', '/FILE:', config_file
    ]

    # Command to set the password for the VPN connection
    set_password_command = [
        'vpncmd', 'localhost', '/CLIENT', '/CMD',
        'AccountPasswordSet', 'VPN', '/PASSWORD:', password
    ]

    # Command to connect to the VPN
    connect_command = [
        'vpncmd', 'localhost', '/CLIENT', '/CMD',
        'AccountConnect', 'VPN'
    ]

    try:
        # Import the VPN configuration
        subprocess.run(import_command, check=True)
        print("VPN configuration imported successfully.")

        # Set the VPN password
        subprocess.run(set_password_command, check=True)
        print("VPN password set successfully.")

        # Connect to the VPN
        subprocess.run(connect_command, check=True)
        print("Connected to the VPN successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while setting up the VPN connection: {e}")

if __name__ == "__main__":
    connect_vpn(vpn_config_file, vpn_user_name, vpn_password)
