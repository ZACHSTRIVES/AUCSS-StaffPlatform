from app import *
import app

buleprint = Blueprint('hr', __name__, template_folder='templates', static_folder='static')


@buleprint.route('/admin')
def admin(issu):
    return render_template('HRadmin.html', issue_information=issu)


@buleprint.route('/meetings',method=['GET'])
def manag_meeting():
    user=app.login_status()
    meetings=list_all_meetings()
    issu=[user['name'],meetings]
    return render_template('ManageMeetings.html',issue_information=issu )
