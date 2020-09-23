from config import *


def fetch_all_artical():
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
