import platform
import netifaces
import socket


def get_interfaces(host=None):
    if not isinstance(host, str):
        raise TypeError("host must be a string")

    AF = netifaces.AF_INET

    info_dict = {'hostname': None, 'ip_list': None}
    address_list = []

    info_dict['hostname'] = platform.node()
    for iface in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(iface)[AF]
        except KeyError:
            continue
        for address in addresses:
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
                    address_list.append(ip)

    info_dict['ip_list'] = address_list
    return info_dict
