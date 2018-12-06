import time
import json
import pickle
import csv
import keyword
import flask
import tkinter

def str_tuple(st):
    lst = []
    for i in range(len(st)):
        lst.append(ord(st[i]))
    return tuple(lst)


def foo(n):
    if n == 1:
        return 1
    return n*foo(n-1)


def clock(fn):
    def wrapper(n):
        start = time.clock()
        fn(n)
        end = time.clock()
        print ('delay= ', end-start)
        return fn(n)
    return wrapper


@clock
def foo1(n):
    if n == 1:
        return 1
    return n*foo(n-1)


def unpacker(*args, **kwargs):
    result = []
    lst = list(args) + list(kwargs.keys())
    for arg in lst:
        if not hasattr(arg, '__iter__'):
            result.append(arg)
        else:
            result += unpacker(*arg)
    return result


def power(x):
    def internal(y):
        return x**y
    return internal

# p = power(4) #- fabric
# print p(2)


def exporter():
    f = open('input.json', 'r')
    j = json.loads(f.read())
    out = open('output.bin', 'wb')
    pickle.dump(j, out)

    out.close()
    f.close()


def importer():
    f = open('output.bin', 'rb')
    print (pickle.load(f))
    f.close()


def privet(hello):
    def internal(name, surname):
        return '{}, {} {}'.format(hello, name, surname)
    return internal


def foo():
    with open('input.csv', 'r') as file:
        j = open('output.json', 'w')
        sfile = csv.reader(file, delimiter=',')
        d = dict()
        i = 0
        for row in sfile:
            d[i] = max(row)
            i += 1
        print(d)
        j.write(json.dumps(d,indent=4))
        j.close()

def process(string):
    def internal(path):
        file = open(path, 'w')
        file.write(string)
        file.close()
    return internal


class Language:
    _words = []
    def lexicon(self):
        return self._words


class Proglanguage(Language):
    _keywords = []
    def lexicon(self):
        return self._keywords


class Python(Proglanguage):
    _keywords = keyword.kwlist

#
# p = Python()
# print(p.lexicon())

# print('Start')

class A:

    def __init__(self):

        print('Constructor A')

class B(A):

    def __init__(self):
        super(B, self).__init__()
        print('Constructor B')

class C(B):
    def __init__(self):
        super(C, self).__init__()
        print('Constructor C')

class D(B):
    def __init__(self):
        super(D, self).__init__()
        print('Constructor D')

    def zzz(self):
        print('I am D')

class E(C):
    def __int__(self):
        print('int E')
        self.zzz()

# import  socket
#
# sock = socket.socket()
#
# sock.bind('localhost', 9000)
# sock.listen()

# Task 11
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def writer():
    with open('output.csv', 'a', newline='') as cfile:
        csvwriter = csv.writer(cfile, delimiter=',')
        data = dict(request.form)

        csvwriter.writerow(data.get('product_name')[0]) #+ ',' + str(data.get('amount')[0]))
        # print(data.get('product_name')[0])
              # +',' + str(data.get('amount')))
    return 'OK', 200

@app.route('/list', methods=['GET'])
def reader():
    if request.method == 'GET':
        with open('output.csv', 'r', newline='') as cfile:
            csvreader = csv.reader(cfile, delimiter=',')
            data = []
            for row in csvreader:
                data.append({row[0]: row[1]})
        print(data)
    return 'OK', 200

# app.run()


# libs for html
# Beautiful Soup
# requests
# lxml
# Scrapy


# Car:
# count_wheel
# VIN
# created
# changed
# issued
# model  (related to CarModel)
# body_type (related to CarBodyType)
# color
#
# CarModel:
# created
# changed
# name
# vendor
#
# CarBodyType:
# created
# changed
# name

# Vendor;
# changed
# created
# name

from peewee import *

DATABASE = 'tweepee.db'
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database

    created = DateTimeField()
    changed = DateTimeField()


class Vendor(BaseModel):
    name = CharField()


class CarModel(BaseModel):

    name = CharField()
    vendor = ForeignKeyField(Vendor)


class CarBodyType(BaseModel):

    name = CharField()


class Car(BaseModel):

    count_wheel = CharField()
    issued = DateTimeField()
    model = ForeignKeyField(CarModel)
    body_type = ForeignKeyField(CarBodyType)
    color = CharField()


def create_tables():
    with database:
        database.create_tables([Vendor, CarModel, CarBodyType, Car])


# create_tables()

# class AbstractEnv:
#     def __init__(self, backend=None):
#         raise NotImplementedError()
#
#     def __getattr__(self, item):
#         raise NotImplementedError()
#
#     def __setattr__(self, key, value):
#         raise NotImplementedError()

import os


class BaseBackend:
    def set_item(self, key, value):
        raise NotImplementedError

    def get_item(self, key):
        raise NotImplementedError


class FakeRedisBackend(BaseBackend):
    def __init__(self):
        import fakeredis
        self.r = fakeredis.FakeStrictRedis()

    def set_item(self, key, value):
        self.r.set(key, value)

    def get_item(self, key):
        return self.r.get(key)


class OS_ENV(BaseBackend):
    def set_item(self, key, value):
        os.environ[key] = value

    def get_item(self, key):
        return os.environ[key]


class Env:
    def __init__(self, backend=None):
        if backend == 'Redis':
            __class__.env = FakeRedisBackend()
        if backend == 'OS_ENV':
            __class__.env = OS_ENV()

    def __getattr__(self, key):
        return bytes.decode(__class__.env.get_item(key))

    def __setattr__(self, key, value):
        return __class__.env.set_item(key, value)


# ENV = Env(backend='Redis')
# # ENV = Env(backend='OS_ENV')
# ENV.path = 'root'
# print(ENV.path)

"""
master.py - run 3 slave.py , every 3 seconds check who finished
print <pid> = <sum>
slave.py
- argv
start, end, step (3 digits)

calculate sum(start, end with step) and print it"""