# routes/main.py
from datetime import datetime
from flask import Blueprint, jsonify, render_template
from models import FoundItem, ReportItem

# 메인 화면용 Blueprint 객체
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


# 분실물 목록 API
@main_bp.route('/api/items')
def get_items():
    items = []

    # 단톡방 제보 게시글 조회
    for item in ReportItem.query.all():
        dt = datetime.combine(item.notice_date, item.notice_time)
        items.append({
            'id': item.id,
            'type': 'report',
            'type_label': '제보',
            'item_name': item.item_name,
            'date': item.notice_date.strftime('%Y-%m-%d'),
            'time': item.notice_time.strftime('%H:%M'),
            'datetime': dt,
            'chat_room_name': item.chat_room_name,
            'description': item.description
        })

    # 직접 습득 게시글 조회
    for item in FoundItem.query.all():
        dt = datetime.combine(item.found_date, item.found_time)
        items.append({
            'id': item.id,
            'type': 'found',
            'type_label': '습득',
            'item_name': item.item_name,
            'date': item.found_date.strftime('%Y-%m-%d'),
            'time': item.found_time.strftime('%H:%M'),
            'datetime': dt,
            'found_location': item.found_location,
            'storage_location': item.storage_location,
            'description': item.description
        })

    # 최신 일시순 정렬 
    items.sort(key=lambda x: x['datetime'], reverse=True)
    for item in items:
        del item['datetime']

    return jsonify(items)



