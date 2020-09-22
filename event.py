from config import *


def fetch_all_event_id_from_database():
    try:
        cur = db.cursor()
        sql = "SELECT event_id, event_title FROM event"
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def get_event(id):
    try:
        cur = db.cursor()
        sql = "SELECT * FROM event WHERE event_id=%s" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
        db.commit()
        cur.close()
        event = [result[0], result[1], result[2], [result[3].strftime("%x"), result[3].strftime("%X")[:-3]], result[4]]
        #      [0]:id    [1]:title  [2]:目标人数               [3]: Date,Time                  [4]:Sign Up Status
        return event
    except Exception as e:
        print(e)


def sign_up_to_database(eventid, name, email, wechat, contact):
    try:
        cur = db.cursor()
        sql = "INSERT INTO event_sign_up(event_id,name,email,wechat_id,contact)" \
              "VALUES (%s,'%s','%s','%s','%s')" % (eventid, name, email, wechat, contact)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def sign_up_start(id):
    try:
        cur = db.cursor()
        sql = "UPDATE event SET sign_up_status='STARTED' WHERE event_id=%s" % id
        print(sql)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def sign_up_end(id):
    try:
        cur = db.cursor()
        sql = "UPDATE event SET sign_up_status='NOT_START' WHERE event_id=%s" % id
        print(sql)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def get_all_member_sign_for_the_event(id):
    try:
        cur = db.cursor()
        sql = "SELECT* FROM event_sign_up WHERE event_id=%s" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def update_event(id, title, target, time, date):
    try:
        cur = db.cursor()
        date = date.split('/')
        date = "20" + date[2] + "-" + date[0] + "-" + date[1]
        time = time + ":00"
        datetime = date + " " + time
        sql = "UPDATE event SET event_title='%s',target_member='%s',event_time='%s' WHERE event_id=%s" % (
            title, target, datetime, id)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def add_need_item(eventid, item, qty, comment):
    try:
        cur = db.cursor()
        sql = "INSERT INTO event_need_items(item,qty,comment,event_id) VALUES ('%s',%s,'%s',%s)" % (
            item, qty, comment, eventid)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def get_unsent_items(id):
    try:
        cur = db.cursor()
        sql = "SELECT* FROM event_need_items WHERE event_id=%s AND sent='N'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def remove_item_from_db(id):
    try:
        cur = db.cursor()
        sql = 'DELETE FROM event_need_items WHERE item_id=%s' % id
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def get_sent_items(id):
    try:
        cur = db.cursor()
        sql = "SELECT* FROM event_need_items WHERE event_id=%s AND sent='Y'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def change_sent_status(id):
    try:
        cur = db.cursor()
        sql = "UPDATE event_need_items SET sent='Y' WHERE event_id=%s AND sent='N'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def get_sent_items_not_buy(id):
    try:
        cur = db.cursor()
        sql = "SELECT * FROM event_need_items WHERE event_id=%s AND sent='Y' AND buy='N'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def get_sent_items_have_bought(id):
    try:
        cur = db.cursor()
        sql = "SELECT * FROM event_need_items WHERE event_id=%s AND sent='Y' AND buy='Y'" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def finish_buy_item(id,staff):
    try:
        cur = db.cursor()
        sql = "UPDATE event_need_items SET buy='Y',staff='%s' WHERE item_id=%s" % (staff,id)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)

def classification_of_event(events):
    try:
        cur = db.cursor()
        sql = "SELECT * FROM event_sign_up"
        db.ping(reconnect=True)
        cur.execute(sql)
        result=cur.fetchall()
        db.commit()
        cur.close()

        member_list=[]
        count=0
        for i in events:
            member_list.append([i[0]])
            for j in result:
                if j[0]==i[0]:
                    member_list[count].append(j)
            count+=1


        return member_list

    except Exception as e:
        print(e)


# def test():
#     events=fetch_all_event_id_from_database()
#     print(classification_of_event(events))
#
# test()