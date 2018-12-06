import xlrd
import json
import csv
import pickle
import datetime
import re
import shelve
import os


class ValidationError(Exception):
    """
    Self defined Base exception class
    """
    pass

class EmailValidationError(ValidationError):
    """
    Exception, raises when email validation failed
    """
    pass


class NameValidationError(ValidationError):
    """
    Exception, raises when name validation failed
    """
    pass


class DateValidationError(ValidationError):
    """
    Exception, raises when date validation failed
    """
    pass


class FileConverter:
    """
    Class uses for reading xls files and convetring it to following data formats:
        - csv
        - json
        - binary
        - shelve
    """

    def __init__(self, filename):
        self.filename = filename
        self.book = xlrd.open_workbook(filename)
        self.sh = self.book.sheet_by_index(0)
        if os.path.exists("errors.log"):
            f = open('errors.log', 'r+')
            f.truncate(0)

    def read_line(self, number):
        """
        Read line with given number from spreadsheet.
        Important: only first 3 rows processing, regarding to class purpose.
        :param number: index of line to read
        :return: line converted to list of string values (only if
                 all it cells passes validation. Otherwise string writes to
                 errors.log file )
        """
        sh = self.book.sheet_by_index(0)
        line = []
        c0 = sh.cell(rowx=number, colx=0).value
        c1 = sh.cell(rowx=number, colx=1).value
        c2 = sh.cell(rowx=number, colx=2).value
        if number == 0:
            line = [c0, c1, c2]
        else:
            try:
                self.name_valid(c0)
                line.append(c0)
                self.email_valid(c1)
                line.append(c1)
                line.append(self.date_transform(c2))

            except Exception as e:
                print(e)
                errors = [c0.encode('utf-8'), c1, c2]
                with open('errors.log', 'a') as file:
                    file.write(str(errors) + '\n')
                line = []
        return line


    def date_transform(self, d):
        """
        Validate given date and transform it to 'American style' date,
        otherwise raises exception
        :param d: xls float date
        :return: string value of date in mm/dd/yyyy format
        """
        try:
            d = datetime.datetime(*xlrd.xldate_as_tuple(d, self.book.datemode)).date().isoformat()
            d = datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d/%Y")
        except Exception:
            raise DateValidationError('Date validation error occurred')
        return d


    def convert_sheet(self):
        """
        Parse xls spreadsheet to list of dictionaries
        :return: xls spreadsheet data converted to list of dicts
        """
        output = []
        for i in range(1, self.sh.nrows):
            if self.read_line(i):
                d = dict(zip(self.read_line(0), self.read_line(i)))
                output.append(d)
        return output


    @staticmethod
    def write_data(data):
        """
        Write parsed data to output files
        :param data: in list of dicts format
        :return: output files in following formats:
            - csv
            - json
            - binary
            - shelve
        """
        with open('output.json', 'w') as jfile:
            jfile.write(json.dumps(data, indent=4))

        with open('output.csv', 'w', newline='') as cfile:
            csvwriter = csv.writer(cfile, delimiter=',')
            csvwriter.writerow(data[0].keys())
            for row in data:
                csvwriter.writerow(row.values())

        with open('output.bin', 'wb') as bfile:
            pickle.dump(data, bfile)

        with shelve.open('shelve', flag='n') as sfile:
            for i in range(len(data)):
                sfile[str(i)] = data[i]


    @staticmethod
    def email_valid(email):
        """
        Validate email
        :param email: email to validate
        :return: None if valid, raises exception otherwise
        """
        reg = re.compile(r'^[A-Za-z0-9\.\+_]+@[A-Za-z0-9\._]+\.[a-zA-Z]*$')
        if reg.match(email) is None or email.split('@')[1].count('.') > 2:
            raise EmailValidationError('Email validation error occurred')


    @staticmethod
    def name_valid(name):
        """
        Check if name contains only latin chars
        :param name: name to validate
        :return: None if valid, raises exception otherwise
        """
        reg = re.compile('^[a-zA-Z]+$')
        if reg.match(name) is None:
            raise NameValidationError('Name validation error occurred')

