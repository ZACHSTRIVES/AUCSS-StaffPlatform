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
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def list_all_leave_requests():
    try:
        cur = db.cursor()
        sql = "select L.meeting_id,U.Name,M.meeting_title,M.meeting_date,L.reason,L.user_email,L.status " \
              "from meeting_leave as L, meeting as M, user as U " \
              "where U.email=L.user_email and M.meeting_id=L.meeting_id"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        leaves = []
        for i in result:
            if i[6] == 'Processing':
                leaves.append(i)
        return leaves

    except Exception as e:
        print(e)


def decline_status(mid, email):
    try:
        cur = db.cursor()
        sql = "update meeting_leave set status='Declined' " \
              "where meeting_id=%s and user_email='%s'" % (mid, email)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()

    except Exception as e:
        print(e)


def approve_status(mid, email):
    try:
        cur = db.cursor()
        sql = "update meeting_leave set status='Approved' " \
              "where meeting_id=%s and user_email='%s'" % (mid, email)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()

    except Exception as e:
        print(e)


def add_leave_to_leave_history(mid, email, processor):
    try:
        cur = db.cursor()
        sql = "INSERT INTO leave_history(user_email, meeting_id, processor) VALUES ('%s',%s,'%s')" % (
            email, mid, processor)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def list_all_records():
    try:
        cur = db.cursor()
        sql = "SELECT U.Name,M.meeting_title,M.meeting_date,L.processor " \
              "FROM user AS U, meeting AS M, leave_history AS L " \
              "WHERE M.meeting_id=L.meeting_id AND U.email=L.user_email"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()

    except Exception as e:
        print(e)


