import csv
import json
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def writer():
    data = { k : v[0] for (k,v) in dict(request.form).items() }
    fieldnames = data.keys()
    rfile = open('output.csv')
    csvreader = csv.reader(rfile)

    """ If csv file empty, writer will append headers and information. Otherwise only information """
    try:
        # Check if product already exists in database
        for row in csvreader:
            if row[0] == list(data.values())[0]:
                rfile.close()
                return "Already exists", 400
        rfile.close()
        with open('output.csv', 'a', newline='') as cfile:
            csvwriter = csv.DictWriter(cfile, delimiter=',', fieldnames=fieldnames)
            csvwriter.writerow(data)
    except StopIteration:
        rfile.close()
        with open('output.csv', 'a', newline='') as cfile:
            csvwriter = csv.DictWriter(cfile, delimiter=',', fieldnames=fieldnames)
            csvwriter.writeheader()
            csvwriter.writerow(data)
    return 'OK', 200


@app.route('/list', methods=['GET'])
def reader():
    params =  {k : v[0] for (k,v) in dict(request.args).items() }
    name = params.get('name', None)
    print('name=', name)
    csv_rows = []
    with open('output.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        if name:
            for row in reader:
                if row[title[0]] == name:
                    print(row)
                    csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
        else:
            for row in reader:
                csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
        json_file = json.dumps(csv_rows, indent=4, separators=(',', ': '))
    return json_file

app.run(port=9000)
