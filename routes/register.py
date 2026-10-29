# routes/register.py

from datetime import date, time
import re
import bcrypt

from flask import Blueprint, render_template, request

# 등록 화면용 Blueprint 객체
register_bp = Blueprint('register', __name__)

# /register 요청을 처리하고 등록 화면 출력 및 입력값 검증 수행
# GET: 등록 화면 열기 / POST: 사용자가 제출한 입력값 검사
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    values = {'type': 'report'}
    errors = []
    validated = False
    # 후속 DB 저장에 사용할 해시값. 평문 대신 이 값만 저장한다.
    password_hash = None

    if request.method == 'POST':
        # HTML input의 name을 키로 사용해 제출값을 사전으로 변환
        values = request.form.to_dict()
        kind = values.get('type')

        # 두 유형에서 공통으로 필요한 입력값
        fields = {
            'date': '날짜',
            'time': '시간',
            'name': '물건 이름',
            'description': '특징',
        }

        # 선택한 유형에 따라 필수 항목 추가
        if kind == 'report':
            fields['chat_name'] = '단톡방 이름'
        elif kind == 'found':
            fields.update(place='습득 장소', storage='보관 위치')
        else:
            errors.append('등록 유형을 선택해 주세요.')

        # 앞뒤 공백을 제거하고, 빈 값이나 공백뿐인 값 검사
        for key, label in fields.items():
            values[key] = values.get(key, '').strip()
            if not values[key]:
                errors.append(f'{label} 항목을 입력해 주세요.')

        # 날짜와 시간이 존재할 때 실제 형식과 범위를 검사
        for key, parser, label in [
            ('date', date.fromisoformat, '날짜'),
            ('time', time.fromisoformat, '시간'),
        ]:
            if values.get(key):
                try:
                    parser(values[key])
                except ValueError:
                    errors.append(f'{label} 형식이 올바르지 않습니다.')

        # 비밀번호는 꺼낸 뒤 values에서 제거해 화면에 다시 전달하지 않음
        password = values.pop('password', '')

        if not password:
            errors.append('삭제 비밀번호를 입력해 주세요.')
        elif not re.fullmatch(r'[0-9]+', password):
            errors.append('삭제 비밀번호는 숫자만 입력해 주세요.')
        elif len(password) != 4:
            errors.append('삭제 비밀번호는 정확히 4자리로 입력해 주세요.')

        # 모든 입력값이 정상일 때만 비밀번호를 해싱
        if not errors:
            try:
                password_hash = bcrypt.hashpw(
                    password.encode('utf-8'),
                    bcrypt.gensalt(),
                ).decode('utf-8')
            except (ValueError, TypeError, OverflowError):
                errors.append(
                    '비밀번호 처리 중 오류가 발생했습니다. 다시 시도해 주세요.'
                )

        # 해싱 처리 이후에는 평문 비밀번호를 더 사용하지 않음
        del password

        # 해싱 오류가 있어도 성공 처리를 하지 않음
        validated = not errors

        # shortcut: DB 저장 미연결, 저장 구현 시 password_hash만 저장.

    # 입력값과 검사 결과를 HTML에 전달
    # 오류가 있으면 HTTP 400, 정상 화면이나 검증 성공이면 HTTP 200 응답
    return render_template(
        'register.html',
        values=values,
        errors=errors,
        validated=validated,
    ), 400 if errors else 200