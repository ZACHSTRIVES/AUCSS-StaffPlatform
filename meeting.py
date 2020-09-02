from config import db


def list_meeting_of_user(user_email):
    try:
        cur = db.cursor()
        sql = "select N.meeting_id,meeting_title,meeting_date,meeting_time,meeting_location from meeting AS M,need_to_meeting AS N where user_email='%s' and M.meeting_id = N.meeting_id" % user_email
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print(e)


print(list_meeting_of_user('wangziqi0325@gmail.com'))