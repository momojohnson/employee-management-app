from flask import render_template, abort
from flask_login import login_required

from . import home

@home.route("/")
def homepage():
    """
    Render homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")
    
@home.route("/dashboard")
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashborad route
    
    """
    return render_template('home/dashboard.html', title="Dashboard")


from flask import render_template, abort
from flask_login import current_user, login_required


@home.route('/admin/dasboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    
    return render_template('home/admin_dashboard.html', title="Dashboard")