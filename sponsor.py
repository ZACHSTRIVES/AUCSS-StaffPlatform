from config import db


def list_all_sponsors():
    try:
        cur = db.cursor()
        sql = "select * from sponsors"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print(e)


def add_sponsor(sql):
    try:

        cur = db.cursor()
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()

    except Exception as e:
        print(e)


def get_sponsor(sid):
    try:
        cur = db.cursor()
        db.ping(reconnect=True)
        sql = 'SELECT * FROM sponsors WHERE sponsor_id=%s' % sid
        cur.execute(sql)
        result = cur.fetchone()
        return result
    except Exception as e:
        print(e)
