from datetime import time

from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

import config

app = Flask(__name__)

app.config.from_object(config)


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST' and len(request.form) == 5:
        name = request.form.get('name')
        email = request.form.get('email')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        department = request.form.get('department')

        # Incomplete information
        if not all([email, name, password_1, password_2]):
            flash("Incomplete information, please complete the form.")
            return render_template('index.html')

        # Password inconsistent
        if password_1 != password_2:
            flash("Password entries are inconsistent.")
            return render_template('index.html')

        # Hash password
        password = generate_password_hash(password_1, method="pbkdf2:sha256", salt_length=8)

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
                sql = "insert into user(Name,email,password,department) VALUES ('%s','%s','%s','%s')" % (
                    name, email, password, department)
                db.ping(reconnect=True)
                cur.execute(sql)
                db.commit()
                cur.close()
                return render_template('backend.html')

        except Exception as e:
            raise e
    elif request.method == 'POST' and len(request.form) == 2:
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
            sql = "select name,department from user where email = '%s'" % email
            db.ping(reconnect=True)
            cur.execute(sql)
            result = cur.fetchone()
            if result:
                return {'email': email, 'name': result[0], 'department': result[1]}
        except Exception as e:
            raise e
    # If email information does not exist, no login, return empty
    return {}


@app.route('/backend',methods=['GET'])
def dashbord():
    login_=login_status()
    print(login_)
    if len(login_)==0:
        return render_template('index.html')
    else:
        return render_template('backend.html',issue_information=login_['name'])









if __name__ == '__main__':
    app.run()
