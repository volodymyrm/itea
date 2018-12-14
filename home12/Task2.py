import re


test_list = ['localhost:5000', '127.0.0.1:5000', '12.44.33.255:9800', 'ukr.net:8080']

def parse_socket(socket):
    template = re.compile(
        r'^((?:(?:(?:\d|[1-9]\d|1\d{2}|2[0-5]{2}|2[0-4]\d)\.){3}'
        r'(?:\d|[1-9]\d|1\d{2}|2[0-5][0-4]|2[0-4]\d))'
        r'|(?:[a-zA-Z]+(?:\.[a-zA-Z]*)*)):(\d+)$'
    )
    result = re.match(template, socket)
    return result.groups() if result else None


if __name__ == '__main__':
    for socket in test_list:
        print(parse_socket(socket))


