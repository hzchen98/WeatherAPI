from json import JSONEncoder


def add_url_parameter(original_url: str, new_params) -> str:
    '''
    Build a URL with new parameters
    :param original_url: original URL
    :param new_param: names and values of the param in dict, e.g. {'first_name': 'Mario', 'last_name': 'Lopez'}
    :return:
    '''
    import urllib

    query_char = '?'
    if query_char not in original_url:
        original_url += query_char
    return original_url + urllib.parse.urlencode(new_params)

def is_valid_ipv4(ip: str) -> bool:
    '''
    check if IPv address is valid
    :param ip: IPv4 address
    :return: validation result
    '''
    import socket

    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__