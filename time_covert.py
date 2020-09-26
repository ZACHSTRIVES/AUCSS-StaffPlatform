from datetime import *


def html_format_TO_mysql_format(html):
    date = html.split("T")[0].split("-")
    time = html.split("T")[1]
    datetime = date[0] + "-" + date[1] + "-" + date[2] + " " + time + ":00"
    return datetime


def datetime_format_TO_html_format(date_time):
    date = date_time.strftime("%x").split("/")
    time = date_time.strftime("%X")[:-3]
    res = "20" + date[2] + "-" + date[0] + "-" + date[1] + "T" + time
    return res


def after_covert_local_time():
    '''
    Dougie Implementation
    server time **EEST**
    TODO:
         Use Datetime get current time, then covert to NZT and database format...

    :return: YYYY-MM-DD HH:MM:SS'  <--Database Format
    '''
    return

