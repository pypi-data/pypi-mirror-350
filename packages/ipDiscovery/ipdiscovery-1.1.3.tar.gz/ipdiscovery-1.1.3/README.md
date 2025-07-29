# 🛡️ ipDiscovery

ipDiscovery is an open-source Python library designed to enhance automation workflows across a wide range of operating
systems, including RHEL, SLES, Ubuntu, VMware, Windows, Oracle, etc by enabling fully automated post-deployment IP
discovery.

It is a secure, cross-platform tool for retrieving IP addresses from MAC addresses using local ARP or remote
DHCP servers. It supports automated environments with built-in encryption `(AES-256-GCM)`

## Key Benefits of the `ipDiscovery` Library

### `Solves a Critical Deployment Problem`

Automatically retrieves OS-assigned IP addresses during deployment workflows, eliminating the need for manual steps.

---

### `No Dependency on External Agents`

Works without requiring external agents like **HPE AMS** — truly agentless.

---

### `Uses DHCP Lease Data for IP Mapping`

Securely determines assigned IPs by leveraging MAC-to-IP mapping from DHCP lease data.

---

### `Streamlines Post-Deployment Automation`

- Eliminates a key bottleneck in OS validation pipelines, allowing automation to proceed smoothly.

---

### `Enhances Scalability and Reliability`

- Supports scalable, reliable test environments with minimal human intervention.

---

### `Secure and Easy Integration`

- Features secure data handling and is easy to integrate into CI/CD or automation workflows.

---

### `Transforms Manual to Automated Workflows`

- Converts traditionally manual processes into fully automated, high-performance solutions.

---

## 📁 1. Configuration & Initialization

### `configure_dhcp_servers(servers: List[Dict])`

- One-time setup to register Linux/Windows DHCP servers.
- Credentials are **securely encrypted** using AES-256-GCM.

### `list_dhcp_servers() -> List[Dict]`

- Returns a list of registered DHCP servers.
- Sensitive data (like credentials) is **masked** in the output.

### `remove_dhcp_server(server_id: str)`

- Removes a DHCP server configuration by its ID or IP address.

---

## 🌐 2. IP Retrieval Workflow

### `get_host_ip(mac_addresses: List[str]) -> Dict[str, str]`

- Attempts to resolve MAC addresses via:
    1. Local ARP cache.
    2. Remote DHCP servers (fallback).
- Returns a dictionary of `{ mac: ip }` or `'not found'`.

### `_check_arp_cache(mac: str) -> Optional[str]`

- Internal helper to parse the local ARP table for IP resolution.

### `_query_linux_dhcp(mac: str, server: Dict) -> Optional[str]`

- SSH into Linux DHCP server.
- Parses `dhcpd.leases` or inspects the ARP table.

### `_query_windows_dhcp(mac: str, server: Dict) -> Optional[str]`

- SSH into Windows server.
- Executes PowerShell `Get-DhcpServerv4Lease`.

---

## 🔐 3. Security Functions

### `encrypt_data(data: str) -> str`

- Internally used to encrypt data using **AES-256-GCM**.

### `decrypt_data(encrypted: str) -> str`

- Secure in-memory decryption of data.

---

## 💡 Flow Secured By: **AES-256-GCM**

Every sensitive operation, including credentials and lease data, is protected using **AES-256-GCM**, ensuring
confidentiality, integrity, and authenticity.
