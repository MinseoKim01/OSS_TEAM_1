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