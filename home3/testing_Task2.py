from Task2 import FileConverter
import json
import csv
import pickle
import shelve

print ('---Custom errors during processing---')
f = FileConverter('Input.xlsx')
f.write_data(f.convert_sheet())
print('\n')
print('---output files validation---')
etalon_json = [
    {
        "Username": "banan",
        "Email": "asdj@asfasd.xc.xc",
        "Joined": "01/01/1997"
    },
    {
        "Username": "ann",
        "Email": "ann@ukr.net",
        "Joined": "10/29/1999"
    }
]

with open('output.json', 'r') as jfile:
    print('JSON test:', etalon_json == json.loads(jfile.read()))


etalon_csv = [
    ['Username', 'Email', 'Joined'],
    ['banan', 'asdj@asfasd.xc.xc', '01/01/1997'],
    ['ann', 'ann@ukr.net', '10/29/1999']
]

actual_csv = []
with open('output.csv', 'r') as cfile:
    cfile = csv.reader(cfile, delimiter=',')
    for row in cfile:
        actual_csv.append(row)
    print('CSV test:', etalon_csv == actual_csv)

etalon_bin = etalon_json
with open('output.bin', 'rb') as bfile:
    actual_bin = pickle.loads(bfile.read())
    print ('BIN test: ', etalon_bin == actual_bin)

etalon_shel = etalon_json
actual_shel = []
with shelve.open('shelve') as sfile:
    for keys, values in sfile.items():
        actual_shel.append(values)
    print('Shelve test:', actual_shel == etalon_shel)

etalon_log = ["[b'Petya', 'wong@gmail.com', '2017-31-12']",
"[b'\\xd0\\x92\\xd0\\xb8\\xd1\\x82\\xd0\\xb5\\xd0\\xba', 'victor@gmail.com', '2015-02-29']",
"[b'wow', 'wow@goog.go.uk.us', '2015-02-28']"]

with open('errors.log', 'r') as efile:
    actual_log = efile.read().splitlines()
    print('Log test:', actual_log == etalon_log)