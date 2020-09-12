from config import db


def list_meeting_of_user(user_email):
    try:
        cur = db.cursor()
        sql = "select N.meeting_id,meeting_title,meeting_date,meeting_location from meeting AS M,need_to_meeting AS N where user_email='%s' and M.meeting_id = N.meeting_id" % user_email
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print(e)


def list_all_meetings():
    try:
        cur = db.cursor()
        sql = "select * from meeting"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print(e)


def get_all_meeting_id():
    try:
        cur = db.cursor()
        sql = "select meeting_id from meeting"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print(e)


def edit_meeting_to_database(sql):
    try:
        cur = db.cursor()
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()


    except Exception as e:
        print(e)


def get_all_users():
    cur = db.cursor()
    sql = "select email from user"
    db.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    db.commit()
    cur.close()
    return result


def add_all_staff_to_meeting(id):
    users = get_all_users()
    sql = "INSERT INTO need_to_meeting (user_email,meeting_id) VALUES"
    for email in users:
        sql += "('%s',%s)," % (email[0], id)
    sql = sql[:-1] + ";"
    cur = db.cursor()
    db.ping(reconnect=True)
    cur.execute(sql)
    db.commit()
    cur.close()

