from app import *


buleprint = Blueprint('management', __name__, template_folder='templates', static_folder='static')


@buleprint.route('/admin')
def admin(issu):
    return render_template('HRadmin.html', issue_information=issu)


@buleprint.route('/meetings')
def manag_meeting():
    return render_template('ManageMeetings.html',issue_information='zach' )
