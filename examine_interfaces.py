import platform
import netifaces
import socket


def get_interfaces(host=None):
    if not isinstance(host, str):
        raise TypeError("host must be a string")

    info_dict = {'hostname': None,
                 'os': None,
                 'addresses': {'ip': None, 'mac': None}
                 }

    ip_list = []
    mac_list = []

    info_dict['hostname'] = platform.node()
    info_dict['os'] = platform.system()

    for iface in netifaces.interfaces():
        try:
            ip4_addresses = netifaces.ifaddresses(iface)[netifaces.AF_INET]
            ip6_addresses = netifaces.ifaddresses(iface)[netifaces.AF_INET6]
            mac_addresses = netifaces.ifaddresses(iface)[netifaces.AF_LINK]
        except KeyError:
            continue
        for address in ip4_addresses:
            ip = address['addr']
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.bind((ip, 0))
                try:
                    sock.connect((host, 80))
                except OSError:
                    pass
                except socket.timeout:
                    pass
                else:
                    ip_list.append(ip)
        mac_list.extend([mac['addr'] for mac in mac_addresses if 'peer' not in mac.keys()])

    info_dict['addresses']['ip'] = ip_list
    info_dict['addresses']['mac'] = mac_list
    return info_dict
