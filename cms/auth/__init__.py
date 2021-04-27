import hashlib


def make_token(password):
    salt = b'cms_token'
    if isinstance(password, str):
        password = password.encode('utf-8')
    md5 = hashlib.md5(salt + password)
    return md5.hexdigest()


def login(request, role, user_id):
    request.session['user'] = {
        'role': role,
        'id': user_id
    }


def logout(request):
    request.session.clear()
    request.session.flush()
