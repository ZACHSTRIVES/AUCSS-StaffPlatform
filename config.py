# encoding:utf-8
import os
import pymysql

DEBUG = False

SECRET_KEY = os.urandom(24)

db = pymysql.connect(host='localhost', user='root',
                     password='02131997', db='aucss', port=3306)