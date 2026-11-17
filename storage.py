# storage.py

from datetime import date, time

from extensions import db
from models import FoundItem, ReportItem


def save_item(values, password_hash):
    """등록 정보와 bcrypt 해시를 저장하고 게시글 ID를 반환한다."""

    # 두 유형에서 공통으로 저장하는 정보
    common = {
        'item_name': values['name'],
        'description': values['description'],
        'password_hash': password_hash,
    }

    if values['type'] == 'report':
        item = ReportItem(
            notice_date=date.fromisoformat(values['date']),
            notice_time=time.fromisoformat(values['time']),
            chat_room_name=values['chat_name'],
            **common,
        )
    elif values['type'] == 'found':
        item = FoundItem(
            found_date=date.fromisoformat(values['date']),
            found_time=time.fromisoformat(values['time']),
            found_location=values['place'],
            storage_location=values['storage'],
            **common,
        )
    else:
        raise ValueError('지원하지 않는 등록 유형입니다.')

    try:
        db.session.add(item)
        db.session.commit()
    except Exception:
        # 저장 실패 시 세션을 복구하고 호출한 쪽에서 오류를 처리하도록 전달
        db.session.rollback()
        raise

    return item.id


def delete_item(item_type, item_id):
    """유형과 게시글 ID로 해당 게시글을 삭제하고, 삭제 여부를 반환한다."""

    model = {'report': ReportItem, 'found': FoundItem}.get(item_type)
    if model is None:
        raise ValueError('지원하지 않는 게시글 유형입니다.')

    item = db.session.get(model, item_id)

    # 삭제할 게시글이 없으면 False 반환
    if item is None:
        return False

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        # 삭제 실패 시 세션을 복구하고 호출한 쪽에서 오류를 처리하도록 전달
        db.session.rollback()
        raise

    return True