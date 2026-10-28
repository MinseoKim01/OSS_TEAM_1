# routes/register.py

from datetime import date, time
import re

from flask import Blueprint, render_template, request

# 등록 화면용 Blueprint 객체
register_bp = Blueprint('register', __name__)

# /register 요청을 처리하고 등록 화면 출력 및 입력값 검증 수행
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    values = {'type': 'report'}
    errors = []
    validated = False

    if request.method == 'POST':
        values = request.form.to_dict()
        kind = values.get('type')

        fields = {
            'date': '날짜',
            'time': '시간',
            'name': '물건 이름',
            'description': '특징',
        }

        if kind == 'report':
            fields['chat_name'] = '단톡방 이름'
        elif kind == 'found':
            fields.update(place='습득 장소', storage='보관 위치')
        else:
            errors.append('등록 유형을 선택해 주세요.')

        for key, label in fields.items():
            values[key] = values.get(key, '').strip()
            if not values[key]:
                errors.append(f'{label} 항목을 입력해 주세요.')

        for key, parser, label in [
            ('date', date.fromisoformat, '날짜'),
            ('time', time.fromisoformat, '시간'),
        ]:
            if values.get(key):
                try:
                    parser(values[key])
                except ValueError:
                    errors.append(f'{label} 형식이 올바르지 않습니다.')

        password = values.pop('password', '')
        if not password:
            errors.append('삭제 비밀번호를 입력해 주세요.')
        elif not re.fullmatch(r'[0-9]+', password):
            errors.append('삭제 비밀번호는 숫자만 입력해 주세요.')
        elif len(password) != 4:
            errors.append('삭제 비밀번호는 정확히 4자리로 입력해 주세요.')

        validated = not errors
        # shortcut: 입력 검증만 수행, DB 저장은 후속 저장 이슈에서 연결.

    return render_template(
        'register.html',
        values=values,
        errors=errors,
        validated=validated,
    ), 400 if errors else 200