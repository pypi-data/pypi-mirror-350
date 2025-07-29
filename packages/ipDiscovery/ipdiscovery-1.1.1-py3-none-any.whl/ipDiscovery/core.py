import json
import os
import base64
import subprocess
import re
from typing import List, Dict, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import paramiko

CONFIG_FILE = "dhcp_servers.json"
PBKDF2_SALT = b"ipdiscovery_salt"
PBKDF2_ITERATIONS = 100_000
KEY_LENGTH = 32


def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=PBKDF2_SALT,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(data: str, key: bytes) -> str:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data.encode(), None)
    return base64.b64encode(nonce + ct).decode()


def decrypt_data(encrypted: str, key: bytes) -> str:
    data = base64.b64decode(encrypted.encode())
    nonce = data[:12]
    ct = data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None).decode()


def configure_dhcp_servers(servers: List[Dict], password: str):
    key = derive_key(password)
    encrypted_servers = []
    for server in servers:
        encrypted = {
            "id": server["id"],
            "ip": server["ip"],
            "type": server["type"],
            "username": encrypt_data(server["username"], key),
            "password": encrypt_data(server["password"], key)
        }
        encrypted_servers.append(encrypted)
    with open(CONFIG_FILE, "w") as f:
        json.dump(encrypted_servers, f, indent=4)


def list_dhcp_servers(password: str) -> List[Dict]:
    if not os.path.exists(CONFIG_FILE):
        return []
    key = derive_key(password)
    with open(CONFIG_FILE, "r") as f:
        servers = json.load(f)
    result = []
    for server in servers:
        result.append({
            "id": server["id"],
            "ip": server["ip"],
            "type": server["type"],
            "username": decrypt_data(server["username"], key),
            "password": decrypt_data(server["password"], key),
        })
    return result


def remove_dhcp_server(server_id: str) -> bool:
    if not os.path.exists(CONFIG_FILE):
        return False
    with open(CONFIG_FILE, "r") as f:
        servers = json.load(f)
    filtered = [s for s in servers if s["id"] != server_id]
    if len(servers) == len(filtered):
        return False
    with open(CONFIG_FILE, "w") as f:
        json.dump(filtered, f, indent=4)
    return True


def _check_arp_cache(mac: str) -> Optional[str]:
    try:
        output = subprocess.check_output(["arp", "-a"], encoding='utf-8')
        for line in output.splitlines():
            if mac.lower().replace(":", "-") in line.lower():
                match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if match:
                    return match.group(1)
    except Exception:
        return None


def _query_linux_dhcp(mac: str, server: Dict, key: bytes) -> Optional[str]:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server['ip'],
            username=decrypt_data(server['username'], key),
            password=decrypt_data(server['password'], key)
        )
        stdin, stdout, stderr = ssh.exec_command("cat /var/lib/dhcp/dhcpd.leases")
        leases = stdout.read().decode()
        for block in leases.split("lease"):
            if mac.lower() in block.lower():
                match = re.search(r"(\d+\.\d+\.\d+\.\d+)", block)
                if match:
                    return match.group(1)
    except Exception:
        return None
    return None


def _query_windows_dhcp(mac: str, server: Dict, key: bytes) -> Optional[str]:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server['ip'],
            username=decrypt_data(server['username'], key),
            password=decrypt_data(server['password'], key)
        )
        script = f"powershell -Command \"Get-DhcpServerv4Lease | Where-Object {{$_.ClientId -eq '{mac}'}} | Select-Object -ExpandProperty IPAddress\""
        stdin, stdout, stderr = ssh.exec_command(script)
        output = stdout.read().decode()
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
    except Exception:
        return None
    return None


def get_host_ip(mac_addresses: List[str], password: str) -> Dict[str, str]:
    print("-------------------------------")
    key = derive_key(password)
    if not os.path.exists(CONFIG_FILE):
        return {mac: 'config missing' for mac in mac_addresses}
    with open(CONFIG_FILE, "r") as f:
        servers = json.load(f)
    results = {}
    for mac in mac_addresses:
        ip = _check_arp_cache(mac)
        if ip:
            results[mac] = ip
            continue
        found = False
        for server in servers:
            if server['type'] == 'linux':
                ip = _query_linux_dhcp(mac, server, key)
            else:
                ip = _query_windows_dhcp(mac, server, key)
            if ip:
                results[mac] = ip
                found = True
                break
        if not found:
            results[mac] = 'not found'
    return results


# if __name__ == "__main__":
#     # Store DHCP server info securely
#     servers = [
#         {
#             "id": "dhcp-linux",
#             "ip": "192.168.1.100",
#             "type": "linux",
#             "username": "admin",
#             "password": "linuxpass"
#         },
#         {
#             "id": "dhcp-win",
#             "ip": "192.168.1.101",
#             "type": "windows",
#             "username": "Administrator",
#             "password": "Win@12345"
#         }
#     ]
#
#     config_password = "StrongMasterKey!"
#     configure_dhcp_servers(servers, config_password)
#
#     servers = list_dhcp_servers(config_password)
#     for s in servers:
#         print(s)
#
#     success = remove_dhcp_server("dhcp-linux")
#     print("Removed:", success)
#
#     servers = list_dhcp_servers(config_password)
#     for s in servers:
#         print(s)
#
#     # Try to resolve MACs
#     macs_to_lookup = ["00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF"]
#     results = get_host_ip(macs_to_lookup, config_password)
#     print(json.dumps(results, indent=4))
