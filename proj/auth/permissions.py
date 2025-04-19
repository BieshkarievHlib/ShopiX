from functools import wraps

from flask import abort
from flask_login import current_user
from flask_principal import Permission, RoleNeed

admin_need = RoleNeed('admin')
user_need = RoleNeed('user')

admin_permission = Permission(admin_need)
user_permission = Permission(user_need)

def roles_required(*role_names):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_anonymous or current_user.role.name not in role_names:
                abort(403) 
            return f(*args, **kwargs)
        return decorated_function
    return decorator
