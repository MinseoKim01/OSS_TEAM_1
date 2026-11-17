# routes/delete.py

import bcrypt

from flask import Blueprint, redirect, request, url_for

from extensions import db
from models import FoundItem, ReportItem
from storage import delete_item

# 삭제 기능용 Blueprint 객체
delete_bp = Blueprint('delete', __name__)

# 삭제 dialog에서 입력한 비밀번호가 해당 게시글에 저장된 비밀번호와 같은지 확인하고, 같으면 삭제
@delete_bp.route('/delete', methods=['POST'])
def delete():
    password = request.form.get('password', '')
    item_id = request.form.get('id', type=int)
    model = {'report': ReportItem, 'found': FoundItem}.get(request.form.get('type'))

    # 유형과 id로 해당 게시글 레코드 조회
    item = db.session.get(model, item_id) if model and item_id is not None else None

    # 저장된 해시의 salt로 입력값을 해싱해 비교
    is_match = item is not None and bcrypt.checkpw(
        password.encode('utf-8'),
        item.password_hash.encode('utf-8'),
    )

    del password

    # 비밀번호 불일치 시 삭제를 중단하고, 재시도할 수 있도록 게시글 id와 유형을 함께 돌려보냄
    if not is_match:
        return redirect(url_for('main.index', password='mismatch', id=item_id, type=request.form.get('type')), code=303)

    # 비밀번호 인증을 통과한 경우에만 게시글 삭제
    try:
        is_deleted = delete_item(request.form.get('type'), item_id)
    except Exception as e:
        print(f'게시글 삭제 오류: {e}')
        is_deleted = False

    # 삭제 결과를 메인 화면에 전달해 임시 메시지로 표시
    return redirect(url_for('main.index', deleted='success' if is_deleted else 'fail'), code=303)
