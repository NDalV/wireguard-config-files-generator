# WireGuard Configuration Files Generator with GUI
### Description:

Automatic generation of data for setting up the server and connecting WireGuard clients.
You can create tens of thousands of unique configuration files in minutes.

### Advantages:
+ all the main script settings are placed in GUI
+ all configuration files necessary for WireGuard to start are generated automatically
+ all necessary iptables rules are generated automatically
+ after successful completion of the script, the only thing required is to copy the server configuration file to your server at the directory /etc/wireguard/

### Features:
+ generates PrivateKey and PublicKey for the WireGuard server configuration file
+ generates a specified numbers of unique PrivateKey, PublicKey and PresharedKey for client configuration files
+ based on the generated keys and parameters specified in GUI, separate unique configuration files are created for each client and a configuration file for the WireGuard server
+ based on the client configuration file, creates a QR code for connection for each client
+ client addresses are generated using the subnet mask 255.0.0.0


### Requirements & Dependencies:
+ Python v.3.11 with Eel library
+ qrencode v.4.1.1
+ wireguard-tools v1.0.20210914

### How to use:
1. install all Requirements & Dependencies
2. git clone https://github.com/NDalV/wireguard-config-files-generator
3. cd wireguard-config-files-generator/
4. edit options.py settings file with any text editor and change the values of the parameters from section 1.Main settings (required) to yours
5. python3 main.py
6. upload the server configuration file (your_name.conf) from the "wireguard" directory to your server at the directory /etc/wireguard/
7. upload the client configuration file (or scan the qr code) from the "confs" directory into the WireGuard client app




