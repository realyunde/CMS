import hashlib
from .models import Admin, Teacher, Student

_SESSION_KEY = '_cms_user'
_ROLE_ADMIN = 'admin'
_ROLE_TEACHER = 'teacher'
_ROLE_STUDENT = 'student'


def make_token(password):
    salt = b'cms_token'
    if isinstance(password, str):
        password = password.encode('utf-8')
    md5 = hashlib.md5(salt + password)
    return md5.hexdigest()


#
# auth
#
def auth_admin(userid, password):
    user = Admin.get_by_id(userid)
    token = make_token(password)
    if user is None:
        return False
    if token != user.token:
        return False
    return True


def auth_teacher(userid, password):
    user = Teacher.get_by_id(userid)
    token = make_token(password)
    if user is None:
        return False
    if token != user.token:
        return False
    return True


def auth_student(userid, password):
    user = Student.get_by_id(userid)
    token = make_token(password)
    if user is None:
        return False
    if token != user.token:
        return False
    return True


#
# login
#
def login_admin(request, userid):
    request.session[_SESSION_KEY] = {
        'id': userid,
        'role': _ROLE_ADMIN,
    }


def login_teacher(request, userid):
    request.session[_SESSION_KEY] = {
        'id': userid,
        'role': _ROLE_TEACHER,
    }


def login_student(request, userid):
    request.session[_SESSION_KEY] = {
        'id': userid,
        'role': _ROLE_STUDENT,
    }


#
# is?
#
def is_admin(request):
    user = request.session.get(_SESSION_KEY)
    if user is None:
        return False
    if user['role'] != _ROLE_ADMIN:
        return False
    return True


def is_teacher(request):
    user = request.session.get(_SESSION_KEY)
    if user is None:
        return False
    if user['role'] != _ROLE_TEACHER:
        return False
    return True


def is_student(request):
    user = request.session.get(_SESSION_KEY)
    if user is None:
        return False
    if user['role'] != _ROLE_STUDENT:
        return False
    return True


def logout(request):
    request.session.clear()
    request.session.flush()
