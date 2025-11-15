from .imports import *


adminbp = Blueprint('admin', __name__, url_prefix='/dashboard/admin')


@adminbp.route('/')
@x.login_required('admin')
def admin_db():
    pass