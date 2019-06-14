import platform
import netifaces


def get_interfaces(AF=netifaces.AF_INET):
    info_dict = {'hostname': None, 'addresses': None}
    address_list = []

    info_dict['hostname'] = platform.node()
    for iface in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(iface)[AF]
        except KeyError:
            continue
        for address in addresses:
            if '127.0.0.1' not in address['addr']: 
                address_list.append(address['addr'])

    info_dict['addresses'] = address_list
    return info_dict
