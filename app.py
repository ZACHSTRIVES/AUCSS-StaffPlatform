from flask import *
from werkzeug.security import generate_password_hash
from config import db
import config

app = Flask(__name__)

app.config.from_object(config)


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        print('post成功')
        name = request.form.get('name')
        email = request.form.get('email')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')

        #Incomplete information
        if not all([email, name, password_1, password_2]):
            flash("Incomplete information, please complete the form.")
            return render_template('index.html')

        #Password inconsistent
        if password_1 != password_2:
            flash("Password entries are inconsistent.")
            return render_template('index.html')

        #Hash password
        password = generate_password_hash(password_1, method="pbkdf2:sha256", salt_length=8)

        # try:
        #     cur=db.cursor()

        return '注册成功！！！！！'

@app.route('/backend')
def backend():
    return render_template('backend.html')
if __name__ == '__main__':
    app.run()
