from config import *


def add_notification_to_db(title, message, sender,staff):
    try:
        cur = db.cursor()
        sql = "INSERT INTO notification(notification_title,message,sender,staff) " \
              "VALUES ('%s','%s','%s','%s')" % (title, message, sender,staff)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def fetch_all_notification_from_db():
    try:
        cur = db.cursor()
        sql = "SELECT * FROM notification WHERE is_show='Y' ORDER BY notification_id DESC;"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def mark_not_show_to_db(id):
    try:
        cur = db.cursor()
        sql = "UPDATE notification SET is_show='N' WHERE notification_id=%s"%id
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)