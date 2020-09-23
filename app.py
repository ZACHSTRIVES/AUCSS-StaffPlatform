from datetime import *
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from meeting import *
from sponsor import *
from event import *
from notification import *
from time_covert import *
import random
import config
from leave import *

app = Flask(__name__)

app.config.from_object(config)

'''
代码库说明：
app.py ==> 网页框架以及所有route.
config.py ==> 数据库配置.
event.py ==> 所有活动有关的function.
leave.py ==> 所有请假有关的function.
meeting.py ==> 所有会议有关的function.
sponsor.py ==> 所有商家数据库有关的function.
signup.py ==> 所有活动报名有关的function.
test.py ==> 测试使用.

+-----Templates：
      储存所有html file
+-----static：
      储存所有静态文件--> 图片, css, javascript脚本


版本记录：
V0.0.1 Init Web------------
开发者：Zach Wang
产品经理：Dougie Feng
测试人员：Dougie Feng, Hanzheng Wang (China status), William Wu, Ariel Wu


'''


# App init====================================================================================================
@app.route('/', methods=['POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        flash("Please fill in the information completely！")
    try:
        cur = db.cursor()
        sql = "select password from user where email = '%s'" % email
        db.ping(reconnect=True)
        cur.execute(sql)
        result = cur.fetchone()
        if result is None:
            flash("User does not exist！")
            return render_template('index.html')
        if check_password_hash(result[0], password):
            session['email'] = email
            session.permanent = True
            return dashbord()
        else:
            flash("Incorrect password!")
            return render_template('index.html')
    except Exception as e:
        raise e


# Login status maintained
@app.context_processor
def login_status():
    # from session get email
    email = session.get('email')
    # If there is email information, it proves that you are logged in, and we
    # get the nickname and user type of the logon from the database to return to the global
    if email:
        try:
            cur = db.cursor()
            sql = "select name,department,type from user where email = '%s'" % email
            db.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()
            if result:
                return {'email': email, 'name': result[0], 'department': result[1], 'type': result[2]}
        except Exception as e:
            raise e
    # If email information does not exist, no login, return empty
    return {}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        code = request.form.get('code')
        type = 0
        department = ''

        # Incomplete information
        if not all([email, name, password_1, password_2]):
            flash("Incomplete information, please complete the form.")
            return redirect(url_for('register'))

        # Password inconsistent
        if password_1 != password_2:
            flash("Password entries are inconsistent.")
            return redirect(url_for('register'))

        # Hash password
        password = generate_password_hash(password_1, method="pbkdf2:sha256", salt_length=8)

        # 检查邀请码，部门分类
        if code == 'AUCSSHR2020':  # 人力资源部
            department = 'HR'
            type = 2
        elif code == 'AUCSSPR2020':  # 外联部
            department = 'PR'
            type = 3
        elif code == 'AUCSSEP2020':  # 策划部
            department = 'EP'
            type = 4
        elif code == 'AUCSSMKT2020':  # 市场部
            department = 'MKT'
            type = 5
        elif code == 'AUCSSOP2020':  # 运营支持部
            department = 'OP'
            type = 6
        elif code == 'AUCSSSUPER':  # 主席团
            department = 'SUPER'
            type = 7
        else:
            flash("Password entries are inconsistent.")
            return redirect(url_for('register'))

        try:
            cur = db.cursor()
            sql = "select * from user where email = '%s'" % email
            db.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()
            if result is not None:
                flash("This email has been registered")
                return render_template('index.html')
            else:
                sql = "insert into user(Name,email,password,department,type) VALUES ('%s','%s','%s','%s',%s)" % (
                    name, email, password, department, type)
                db.ping(reconnect=True)
                cur.execute(sql)
                db.commit()
                cur.close()
                return redirect(url_for('dashbord'))

        except Exception as e:
            raise e


@app.route('/', methods=['GET'])
def dashbord():
    login_ = login_status()
    if len(login_) == 0:
        return render_template('index.html')
    else:
        meetings = list_all_meetings()
        notification = fetch_all_notification_from_db()
        data = [login_['name'], meetings, str(len(meetings))]  # data=[0=email,1=meetings,2=len(meetings)]
        if login_['type'] == 1:  # Category 1: General Staff
            return render_template('backend.html', user_name=data[0], issue_information=data)
        if login_['type'] == 2:  # Category 2: HR Staff
            return hr(data, notification)
        if login_['type'] == 3:  # Category 3: PR Staff
            return pr(data, notification)
        if login_['type'] == 4:  # Category 4: EP Staff
            return ep(data, notification)
        if login_['type'] == 5:  # Category 4: EP Staff
            return mkt(data, notification)
        if login_['type'] == 6:  # Category 4: OP Staff
            return op(data, notification)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(('dashbord')))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/favicon.ico')
def favicon():
    return 'a'


@app.route('/meetingleave', methods=['GET'])
def meeting_leave():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    if request.method == 'GET':
        info = ''
        info1 = ''
        meetings = list_meeting_of_user(login_['email'])
        if len(meetings) == 0:
            info = "You don't have meetings at the moment where you can ask for leave."
        all_leaves = list_leave_apply_of_user(login_['email'])
        if len(all_leaves) == 0:
            info1 = "You haven't asked for leave yet!"

        if login_['type'] == 2:
            return render_template('MeetingLeave.html', info=info, info1=info1, meetings=meetings, leaves=all_leaves,
                                   user_name=login_['name'])
        elif login_['type'] == 3:
            return render_template('MeetingLeavePR.html', info=info, info1=info1, meetings=meetings, leaves=all_leaves,
                                   user_name=login_['name'])
        elif login_['type'] == 4:
            all_event = fetch_all_event_id_from_database()
            return render_template('MeetingLeaveEP.html', info=info, info1=info1, meetings=meetings, leaves=all_leaves,
                                   user_name=login_['name'], events=all_event)
        elif login_['type'] == 6:
            all_event = fetch_all_event_id_from_database()
            return render_template('MeetingLeaveOP.html', info=info, info1=info1, meetings=meetings, leaves=all_leaves,
                                   user_name=login_['name'], events=all_event)


@app.route('/meetingleave', methods=['POST'])
def apply_for_leave():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    reason = request.form.get('reason')
    meeting_id = request.form.get('radio1')
    email = login_['email']
    apply_leave(email, meeting_id, reason)
    return redirect(url_for(('meeting_leave')))


# Page for department of HR ====================================================================================
@app.route('/hr')
def hr(issu, notification):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    return render_template('HRadmin.html', user_name=issu[0], issue_information=issu, notification=notification)


@app.route('/meetings', methods=['GET'])
def manag_meeting():
    login_ = login_status()
    if len(login_) == 0:
        return dashbord()
    user = login_status()
    meetings = list_all_meetings()
    issu = [user['name'], meetings]
    return render_template('ManageMeetings.html', issue_information=issu, user_name=login_['name'])


@app.route('/meetings', methods=['POST'])
def add_meeting():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    location = request.form.get('location')
    title = request.form.get('title')
    time = request.form.get('time')
    datatime = html_format_TO_mysql_format(time)
    sql = "INSERT INTO meeting(meeting_title,meeting_location,meeting_date) " \
          "VALUES ('%s','%s','%s')" % (title, location, datatime)

    edit_meeting_to_database(sql)
    return redirect(url_for(('manag_meeting')))


@app.route('/<mid>', methods=['GET', 'POST'])
def edit_meeting(mid):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    if request.method == 'GET':
        try:
            cur = db.cursor()
            sql = "select * from meeting where meeting_id=%s" % mid
            db.ping(reconnect=True)
            cur.execute(sql)
            meeting = cur.fetchall()
            title = meeting[0][1]
            location = meeting[0][2]
            datetime = meeting[0][3]
            datetime =datetime_format_TO_html_format(datetime)
            print(date)
            return render_template('EditMeeting.html', user_name=login_['name'], mid=mid, title=title,
                                   location=location, time=datetime)
        except Exception as e:
            raise e
    elif request.method == 'POST':
        try:
            location = request.form.get('location')
            title = request.form.get('title')
            time = request.form.get('time')
            datetime =html_format_TO_mysql_format(time)
            sql = "update meeting set meeting_title='%s',meeting_location='%s',meeting_date='%s' where meeting_id=%s" % (
                title, location, datetime, mid)
            edit_meeting_to_database(sql)
            return manag_meeting()
        except Exception as e:
            raise e


@app.route('/<mid>/delmeeting', methods=['GET'])
def del_meeting(mid):
    sql = 'delete from meeting where meeting_id=%s' % mid
    edit_meeting_to_database(sql)
    return redirect(url_for(('manag_meeting')))


@app.route('/manageleaves', methods=['GET'])
def manage_leave():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    all_leaves = list_all_leave_requests()
    leaves_record = list_all_records()
    return render_template('ManageLeave.html', user_name=login_['name'], leaves=all_leaves, leaves_record=leaves_record)


@app.route('/<mid>/<email>/decline', methods=['GET'])
def decline_leave(mid, email):
    login_ = login_status()
    if len(login_) == 0:
        return redirect((url_for('dashbord')))
    decline_status(mid, email)
    return redirect(url_for('manage_leave'))


@app.route('/<mid>/<email>/approve', methods=['GET'])
def approve_leave(mid, email):
    login_ = login_status()
    if len(login_) == 0:
        return redirect((url_for('dashbord')))
    approve_status(mid, email)
    processor = login_['name']
    add_leave_to_leave_history(mid, email, processor)
    return redirect(url_for('manage_leave', ))


@app.route('/notification', methods=['GET', 'POST'])
def notification():
    login_ = login_status()
    if len(login_) == 0:
        return redirect((url_for('dashbord')))
    if request.method == 'GET':
        all_notifi = fetch_all_notification_from_db()
        return render_template('Notification.html', user_name=login_['name'], all_notifi=all_notifi)
    elif request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        sender = '人力资源部'
        add_notification_to_db(title, message, sender, login_['name'])
        return redirect(url_for('notification'))


@app.route('/recallid<id>')
def recall_notice(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect((url_for('dashbord')))
    mark_not_show_to_db(id)
    return redirect(url_for('notification'))


@app.route('/HREventSignupInfo')
def event_signup_info():
    login_ = login_status()
    if len(login_)==0:
        return redirect(url_for('dashbord'))
    else:
        events = fetch_all_event_id_from_database()
        all_member=classification_of_event(events)
        return render_template('HREventSignUpInfo.html', user_name=login_['name'], events=events,all_member=all_member)


'''
 Page for department of PR ====================================================================================
'''


@app.route('/pr', methods=['GET'])
def pr(issu, notification):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))

    return render_template('PRadmin.html', user_name=login_['name'], issue_information=issu, notification=notification)


@app.route('/sponsordatabase', methods=['GET', 'POST'])
def sponsor_database():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    if request.method == 'GET':
        sponsors = list_all_sponsors()
        return render_template('SponsorsDatabase.html', user_name=login_['name'], sponsors=sponsors)

    if request.method == 'POST':
        sponsor_name = request.form.get('sponsor_name')
        sponsor_add = request.form.get('sponsor_add')
        contact_name = request.form.get('contact_name')
        contact = request.form.get('contact')
        contact_type = request.form.get('contact_type')
        staff = request.form.get('staff')
        sponsor_comment = request.form.get('sponsor_comment')
        sql = "INSERT INTO sponsors (sponsor_name,sponsor_add,contact_name,contact,contact_type,staff,sponsor_comment)" \
              "VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                  sponsor_name, sponsor_add, contact_name, contact, contact_type, staff, sponsor_comment)
        add_sponsor(sql)
        return redirect(url_for('sponsor_database'))


@app.route('/editsponsorsid<sid>', methods=['GET', 'POST'])
def edit_sponsor(sid):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    if request.method == 'GET':
        that_sponsor = get_sponsor(sid)
        return render_template('EditSponsor.html', user_name=login_['name'], sponsor=that_sponsor)
    elif request.method == 'POST':
        try:
            sponsor_name = request.form.get('sponsor_name')
            sponsor_add = request.form.get('sponsor_add')
            contact_name = request.form.get('contact_name')
            contact = request.form.get('contact')
            contact_type = request.form.get('contact_type')
            staff = request.form.get('staff')
            sponsor_comment = request.form.get('sponsor_comment')
            sql = "UPDATE sponsors " \
                  "SET sponsor_name='%s',sponsor_add='%s',contact_name='%s',contact='%s',contact_type='%s',staff='%s',sponsor_comment='%s'" \
                  "WHERE sponsor_id=%s" % (
                      sponsor_name, sponsor_add, contact_name, contact, contact_type, staff, sponsor_comment, sid)
            add_sponsor(sql)
            return redirect(url_for("sponsor_database"))
        except Exception as e:
            raise e


@app.route('/deletesponsor<sid>', methods=['GET'])
def delete_sponsor(sid):
    sql = 'delete from sponsors where sponsor_id=%s' % sid
    add_sponsor(sql)
    return redirect(url_for(('sponsor_database')))


# Page for department of EP ====================================================================================
@app.route('/ep', methods=['GET'])
def ep(issu, notification):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    all_event = fetch_all_event_id_from_database()

    return render_template('EPadmin.html', user_name=login_['name'], issue_information=issu, events=all_event,
                           notification=notification)


@app.route('/EventDashboard-id=<id>', methods=['GET', 'POST'])
def event_dashboard(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    if request.method == 'GET':
        all_event = fetch_all_event_id_from_database()
        event = get_event(id)
        member = get_all_member_sign_for_the_event(id)

        return render_template('EventDashboard.html', user_name=login_['name'], events=all_event, event=event,
                               count=len(member))
    elif request.method == 'POST':
        title = request.form.get('title')
        target = request.form.get('targetMember')
        date = request.form.get('date')
        time = request.form.get('time')
        update_event(id, title, target, time, date)
        return redirect(url_for('event_dashboard', id=id))


@app.route('/SignUpManage=id=<id>', methods=['GET'])
def sign_up_manage(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    all_event = fetch_all_event_id_from_database()
    event = get_event(id)
    if event[4] == 'NOT_START':
        return render_template('EventSignUpManageEP.html', user_name=login_['name'], events=all_event, event=event)
    elif event[4] == 'STARTED':
        member = get_all_member_sign_for_the_event(id)
        return render_template('EventSignUpManageStatsEP.html', user_name=login_['name'], events=all_event, event=event,
                               member=member, count=len(member))


@app.route('/SingUpManage/startid<id>')
def start_sign_up(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    sign_up_start(id)
    return redirect(url_for('sign_up_manage', id=id))


@app.route('/SingUpManage/endid<id>')
def end_sign_up(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    sign_up_end(id)
    return redirect(url_for('sign_up_manage', id=id))


@app.route('/EventSignUpid<id>', methods=['GET', 'POST'])
def sign_up(id):
    if request.method == 'GET':
        event = get_event(id)
        if event[4] == 'NOT_START':
            return render_template('EventSignUp404.html')
        else:
            return render_template('EventSignUp.html', event=event[1])

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        wechat = request.form.get('wx')
        contact = request.form.get('contact')
        sign_up_to_database(id, name, email, wechat, contact)
        return render_template('EventSignUpFinished.html', name=name)


@app.route('/EventNeedsId<id>', methods=['GET', 'POST'])
def event_needs(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    event = get_event(id)
    all_event = fetch_all_event_id_from_database()
    if request.method == 'GET':
        all_items = get_unsent_items(id)
        sent_items = get_sent_items(id)
        return render_template('EventNeedList.html', events=all_event, event=event, items=all_items,
                               sent_items=sent_items)
    if request.method == 'POST':
        item = request.form.get('item')
        qty = request.form.get('qty')
        comment = request.form.get('comment')
        add_need_item(id, item, qty, comment)
        return redirect(url_for('event_needs', id=id))


@app.route('/DelectNeedsItem<eventid><id>')
def del_item(eventid, id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    remove_item_from_db(id)
    return redirect(url_for('event_needs', id=eventid))


@app.route('/sentitemid<id>')
def sent_item(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    change_sent_status(id)
    return redirect(url_for('event_needs', id=id))


# Page for department of OP 运营支持部====================================================================================
@app.route('/op', methods=['GET'])
def op(issu, notification):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    all_event = fetch_all_event_id_from_database()

    return render_template('OPadmin.html', user_name=login_['name'], issue_information=issu, events=all_event,
                           notification=notification)


@app.route('/eventNeedslistid<id>')
def event_needs_op_page(id):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    all_event = fetch_all_event_id_from_database()
    event = get_event(id)
    need = get_sent_items_not_buy(id)
    bought = get_sent_items_have_bought(id)
    return render_template('OPEventNeedsList.html', user_name=login_['name'], events=all_event, event=event, need=need,
                           bought=bought)


@app.route('/boughtitem<id><eid>')
def complete_buy(id, eid):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for(('dashbord')))
    finish_buy_item(id, login_['name'])
    return redirect(url_for('event_needs_op_page', id=eid))

'''
 Page for department of MKT 市场部===================================================================================================================
'''
@app.route('/mkt',methods=['GET'])
def mkt(issu,notification):
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for('dashbord'))
    all_event = fetch_all_event_id_from_database()

    return render_template('MKTadmin.html', user_name=login_['name'], issue_information=issu,
                           notification=notification)
@app.route('/WechatArticle',methods=['GET'])
def article():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for('dashbord'))
    return render_template('MKTArticle.html',user_name=login_['name'])

@app.route('/AddAriticle',methods=['GET','POST'])
def add_article():
    login_ = login_status()
    if len(login_) == 0:
        return redirect(url_for('dashbord'))
    return render_template('MKTAddNewArticle.html', user_name=login_['name'])


if __name__ == '__main__':
    app.run()

'''
BUG反馈===================================================================================================================
'''
@app.route('/bugfeedback', methods=['GET', 'POST'])
def bug_feedback():
    if request.method == 'GET':
        return render_template('BugFeedback.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        feedback = request.form.get('feedback')
        try:
            cur = db.cursor()
            sql = "INSERT INTO feedback(name,feedback) VALUES ('%s','%s')" % (name, pymysql.escape_string(feedback))
            db.ping(reconnect=True)
            cur.execute(sql)
            db.commit()
            cur.close()
            return redirect(url_for('dashbord'))
        except Exception as e:
            print(e)
