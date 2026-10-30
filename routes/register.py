# routes/register.py

from datetime import date, time
import re
import bcrypt

from sqlalchemy.exc import SQLAlchemyError

from storage import save_item

from flask import (
    Blueprint, current_app, redirect,
    render_template, request, url_for,
)

# 등록 화면용 Blueprint 객체
register_bp = Blueprint('register', __name__)

# /register 요청을 처리하고 등록 화면 출력 및 입력값 검증 수행
# GET: 등록 화면 열기 / POST: 사용자가 제출한 입력값 검사
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    values = {'type': 'report'}
    errors = []
    # DB에 저장할 bcrypt 해시값
    password_hash = None
    storage_failed = False

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

        # 비밀번호를 화면에 다시 전달하지 않도록 values에서 제거
        password = values.pop('password', '')

        if not password:
            errors.append('삭제 비밀번호를 입력해 주세요.')
        elif not re.fullmatch(r'[0-9]+', password):
            errors.append('삭제 비밀번호는 숫자만 입력해 주세요.')
        elif len(password) != 4:
            errors.append('삭제 비밀번호는 정확히 4자리로 입력해 주세요.')

        # 모든 입력값이 정상일 때 비밀번호 해싱
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

        del password

        # 검증과 해싱이 성공한 경우에만 해시값을 저장
        if not errors:
            try:
                save_item(values, password_hash)
            except SQLAlchemyError as error:
                detail = getattr(
                    getattr(error, 'orig', None), 'diag', None
                )

                current_app.logger.error(
                    '저장 오류: %s / 테이블: %s / 컬럼: %s',
                    type(error).__name__,
                    getattr(detail, 'table_name', None),
                    getattr(detail, 'column_name', None),
                )

                storage_failed = True
                errors.append(
                    '저장 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
                )
            else:
                # 저장 성공 후 목록으로 이동
                return redirect(url_for('main.index'), code=303)

        # 해싱 처리 이후에는 평문 비밀번호를 더 사용하지 않음
        del password

        # 입력 검증과 해싱이 모두 성공한 경우에만 저장
        if not errors:
            try:
                save_item(values, password_hash)
            except SQLAlchemyError:
                # 롤백은 storage.py에서 수행하고 화면에는 일반 안내만 표시
                storage_failed = True
                errors.append(
                    '저장 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
                )

    # 입력값과 검사 결과를 HTML에 전달
    # 저장소 오류는 HTTP 500, 잘못된 입력은 HTTP 400으로 구분
    if storage_failed:
        status_code = 500
    elif errors:
        status_code = 400
    else:
        status_code = 200

    return render_template(
        'register.html',
        values=values,
        errors=errors,
    ), status_code