# routes/register.py

from flask import Blueprint, render_template

# 등록 화면용 Blueprint 객체
register_bp = Blueprint('register', __name__)

# 여기에 /register 주소와 처리 함수를 연결
# 브라우저의 /register요청 -> register_bp -> register() -> templates/register.html로 연결
@register_bp.route('/register')
def register():
    return render_template('register.html', values={'type': 'report'}, errors=[], validated=False)
