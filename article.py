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


def add_works_to_db(article_id, type, staff, work_due):
    try:
        cur = db.cursor()
        sql = "INSERT INTO article_works(works_type,works_article,works_dueday,works_staff)VALUES (%s,%s,'%s','%s');" % (
            type, article_id, work_due, staff)
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def get_article_s_work(id):
    try:
        cur = db.cursor()
        sql = "SELECT * FROM article_works WHERE works_article=%s ORDER BY works_type" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def get_user_name(email):
    try:
        cur = db.cursor()
        sql = "SELECT Name FROM user WHERE email='%s'" % email
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def get_works_list(articles):
    res = {}
    for i in range(0, len(articles)):
        id = articles[i][0]
        work = []
        works = get_article_s_work(id)
        for w in works:
            my_list = [w[0], w[1], w[3], get_user_name(w[5])[0]]
            work.append(my_list)
        res[id] = work
    return res


def get_your_task_with_article(email, id):
    try:
        cur = db.cursor()
        sql = "SELECT * FROM article_works WHERE works_staff='%s' AND works_article=%s" % (email, id)
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        cur.close()
        return result
    except Exception as e:
        print(e)


def get_task_list(email, articles):
    res = {}
    for a in articles:
        id = a[0]
        tasks = get_your_task_with_article(email, id)
        res[id] = tasks
    return res


def update_finish_status(type, id):
    try:
        type=int(type)
        cur = db.cursor()
        sql = ''
        if type == 1:
            sql = "UPDATE article SET banner_status='Y' WHERE article_id=%s" % id
        elif type == 2:
            sql = "UPDATE article SET text_status='Y' WHERE article_id=%s" % id
        elif type==3:
            sql = "UPDATE article SET style_status='Y' WHERE article_id=%s" % id

        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def update_task_status(id):
    try:
        cur = db.cursor()
        sql = "UPDATE article_works SET is_finished='Y' WHERE works_num=%s" % id
        db.ping(reconnect=True)
        cur.execute(sql)
        db.commit()
        cur.close()
    except Exception as e:
        print(e)


def finish_task_in_db(task, article, type):
    update_task_status(task)
    update_finish_status(type, article)
