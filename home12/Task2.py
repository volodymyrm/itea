import re

inp = '254.168.1.254:1020'

# socket = re.split(r':', inp)
# if len(socket) == 2:
#     host = socket[0]
#     port = socket[1]

result = re.match(r'(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)', inp)
print(result)
if result:
    print(result.group(0))