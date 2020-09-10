from config import db


def apply_leave(email, mid, reason):
    try:
        status = "Processing"
        cur = db.cursor()
        sql = "INSERT INTO meeting_leave (meeting_id,user_email,reason,status)VALUES (%s,'%s','%s','%s')" % (
        mid, email, reason, status)

        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def list_leave_apply_of_user(email):
    try:
        cur = db.cursor()
        sql = "SELECT M.meeting_title,M.meeting_date,L.status FROM meeting AS M,meeting_leave AS L " \
              "WHERE M.meeting_id =L.meeting_id AND L.user_email='%s'" % email
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
    except Exception as e:
        print(e)




    return result
