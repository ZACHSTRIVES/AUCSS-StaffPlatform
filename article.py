from config import *


def fetch_all_article():
    try:
        cur = db.cursor()
        sql = "SELECT * FROM article WHERE article_status='N'"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def add_article_to_db(title, due):
    try:
        cur = db.cursor()
        sql = "INSERT INTO article(article_title,article_dueday)VALUES ('%s','%s')" % (title, due)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def fetch_all_mkt_staff():
    try:
        cur = db.cursor()
        sql = "SELECT Name,email FROM user WHERE type=5"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def get_article_id(title):
    try:
        cur = db.cursor()
        sql = "SELECT article_id FROM article WHERE article_title='%s' AND article_status='N'" % title
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def add_works_to_db(article_id,type,staff, work_due):
    try:
        cur = db.cursor()
        sql = "INSERT INTO article_works(works_type,works_article,works_dueday,works_staff)VALUES (%s,%s,'%s','%s');" %(type,article_id,work_due,staff)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)
