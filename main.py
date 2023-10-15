import eel
from pathlib import Path
import os,sys

@eel.expose
def generator(count:int, name, endname, endpoint, port, interface, ip_mask:int, allowed_ips, dns, path_keys, path_conf, path_server):
    
    if int(ip_mask) <= 0 or int(ip_mask) > 255:
        print('''Data generation error:
        Network start address parameter is not specified correctly
        The program has stopped!''')
        return '''Data generation error:
        Network start address parameter is not specified correctly
        The program has stopped!'''
        #exit()

    os.umask(0o077) # removing permissions to work with files for everyone except the owner

# generating a new server key. if a new key is not required, comment out the next five lines
    print('Server keys are being generated')
    os.system(f'mkdir {path_server}')
    os.system(f'wg genkey > {path_server}/private.key') 
    os.system(f'wg pubkey < {path_server}/private.key > {path_server}/public.pub')
    print('Server key generation has been completed successfully!')

# generating client keys
    os.system(f'mkdir {path_keys}')
    print('Client keys are being generated: ')
    i = 1
    while i<=int(count):
        print(name +'-'+ str(i))
        os.system(f'wg genkey > {path_keys}/{name}-{i}.key') 
        os.system(f'wg pubkey < {path_keys}/{name}-{i}.key > {path_keys}/{name}-{i}.pub')
        os.system(f'wg genpsk > {path_keys}/{name}-{i}.psk')
        i+=1
    print('Generation of client keys has been successfully completed!')

# compiling a server configuration file
    os.system(f'mkdir {path_conf}')
    print('VPN client profiles are being generated: ')
    os.system(f'echo "[Interface]" >> {path_server}/{endname}.conf')
    os.system(f'echo "Address = {ip_mask}.0.0.1/22" >> {path_server}/{endname}.conf')
    os.system(f'echo "SaveConfig = false" >> {path_server}/{endname}.conf')
    os.system(f'echo "PostUp = ufw route allow in on {endname} out on {interface}" >> {path_server}/{endname}.conf')
    os.system(f'echo "PostUp = iptables -t nat -I POSTROUTING -o {interface} -j MASQUERADE" >> {path_server}/{endname}.conf')
    os.system(f'echo "PostUp = ip6tables -t nat -I POSTROUTING -o {interface} -j MASQUERADE" >> {path_server}/{endname}.conf')
    os.system(f'echo "PreDown = ufw route delete allow in on {endname} out on {interface}" >> {path_server}/{endname}.conf')
    os.system(f'echo "PreDown = iptables -t nat -D POSTROUTING -o {interface} -j MASQUERADE" >> {path_server}/{endname}.conf')
    os.system(f'echo "PreDown = ip6tables -t nat -D POSTROUTING -o {interface} -j MASQUERADE" >> {path_server}/{endname}.conf')
    os.system(f'echo "ListenPort = {port}" >> {path_server}/{endname}.conf')
    os.system(f'echo "PrivateKey = $(cat {path_server}/private.key)" >> {path_server}/{endname}.conf')
    os.system(f'echo "DNS = {dns} 2001:4860:4860::8888" >> {path_server}/{endname}.conf')
# generation of client configuration files (profiles)
    def vpn_peer_conf(i, ip):
        print(name +'-'+ str(i) + '@' + endname + '.conf')
        os.system(f'echo "[Interface]" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "Address = {ip}" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "PrivateKey = $(cat {path_keys}/{name}-{i}.key)" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "DNS = {dns}" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "[Peer]" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "Endpoint = {endpoint}:{port}" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "AllowedIPs = {allowed_ips}" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "PublicKey = $(cat {path_server}/public.pub)" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'echo "PresharedKey = $(cat {path_keys}/{name}-{i}.psk)" >> {path_conf}/{name}-{i}@{endname}.conf')
        os.system(f'qrencode  -r "{path_conf}/{name}-{i}@{endname}.conf" -o {path_conf}/{name}-{i}@{endname}.png') # creating a QR code for the client from the client configuration file
        print(name +'-'+ str(i) + '@' + endname + '.png')
    # supplementing the server configuration file with generated data from client configuration files (keys, IP address)
        os.system(f'echo " " >> {path_server}/{endname}.conf')
        os.system(f'echo "[Peer]" >> {path_server}/{endname}.conf')
        os.system(f'echo "AllowedIPs = {ip}" >> {path_server}/{endname}.conf')
        os.system(f'echo "PublicKey = $(cat {path_keys}/{name}-{i}.pub)" >> {path_server}/{endname}.conf')
        os.system(f'echo "PresharedKey = $(cat {path_keys}/{name}-{i}.psk)" >> {path_server}/{endname}.conf')
# main loop for generating the required number of client configuration files with assignment of a unique IP address
    def main_cirle_run():
        i = 1
        max_ip = 253
        x = 0
        while i < int(count):
 
         while x <= max_ip and i<=int(count):
                y = 0
                while y <= max_ip and i<=int(count):
                    if y == 0:
                        z = 2
                    else:
                        z = 1
                    while z <= max_ip and i<=int(count):
                        ip = str (f'{ip_mask}.{x}.{y}.{z}/32')
                        vpn_peer_conf(i,ip)
                        z +=1
                        i +=1
                        if i > int(count):
                            return # exit the cycle when the total number of client profiles reaches the parameter specified in the options
                 
                    ip = str (f'{ip_mask}.{x}.{y}.{z}/32')
                    vpn_peer_conf(i,ip)
                    y +=1
                    i +=1
        
                ip = str (f'{ip_mask}.{x}.{y}.{z}/32')
                vpn_peer_conf(i,ip)
                x +=1
                i +=1 
    main_cirle_run()
    print("Finished")
    return f'''Data generation completed successfully'''


eel.init("web")
eel.start("main.html", size = (1024, 800), mode = "chrome")

