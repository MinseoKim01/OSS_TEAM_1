# routes/delete.py

import bcrypt

from flask import Blueprint, redirect, request, url_for

# 삭제 기능용 Blueprint 객체
delete_bp = Blueprint('delete', __name__)

# 삭제 dialog에서 입력한 비밀번호를 등록 시와 같은 방법으로 해싱
@delete_bp.route('/delete', methods=['POST'])
def delete():
    password = request.form.get('password', '')

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(),
    ).decode('utf-8')

    del password

    return redirect(url_for('main.index'), code=303)
