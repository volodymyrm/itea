import re

inp = '192.168.1.1:1020'

socket = re.split(r':', inp)
if len(socket) == 2:
    host = socket[0]
    port = socket[1]

    print(re.match(r'[0-9].[0-9].[0-9].[0-9]', host))