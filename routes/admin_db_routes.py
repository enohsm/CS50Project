from .imports import *


adminbp = Blueprint('admin', __name__, url_prefix='/dashboard/admin')


@adminbp.route('/')
@x.login_required('admin')
def admin_db():
    return render_template('admin_dashboard.html')


@adminbp.route('/roles')
@x.login_required('admin')
def set_roles():
    return render_template('roles.html')


@adminbp.route('/get_roles')
@x.login_required('admin')
def get_roles():
    username = request.args.get('username', '')
    if username.upper() == 'ALL':
        roles = DataBase.execute('SELECT users.id, users.username, users.name, users.surname, roles.role FROM users JOIN roles ON users.id = roles.user_id')
    
    else:
        roles = DataBase.execute('SELECT users.id, users.username, users.name, users.surname, roles.role FROM users JOIN roles ON users.id = roles.user_id WHERE users.username LIKE ?', '%' + username + '%')
    return jsonify(roles)


@adminbp.route('/set_roles', methods = ['GET', 'POST'])
@x.login_required('admin')
def update_roles():
    if request.method == 'POST':
        user_id = request.args.get('id')
        if not user_id or not user_id.isdigit():
            return jsonify({'status':'error'})
        
        is_exist_user = DataBase.execute('SELECT users.id, roles.role FROM users JOIN roles ON users.id = roles.user_id WHERE users.id = ? AND role = 0', user_id)
        if not is_exist_user:
            flash('The user could not found or already updated.')
            return jsonify({'status':'error'})
        
        try:
            DataBase.execute('UPDATE roles SET role = 1 WHERE user_id = ? AND role = 0', user_id)
            return jsonify({'status':'ok'})
        
        except ValueError:
            return jsonify({'status':'error'})
    
    else:
        return redirect(url_for('admin.set_roles'))