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
    try:
        items = []

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

        items.sort(key=lambda x: x['datetime'], reverse=True)

        for item in items:
            del item['datetime']

        return jsonify(items)

    except Exception as e:
        print(f'분실물 목록 조회 오류: {e}')

        return jsonify({
            'error': 'DB 조회에 실패했습니다.',
            'message': '잠시 후 다시 시도해주세요.'
        }), 500


# 전체 및 유형별(type: report / found) 등록 건수 카운트(count) 집계 API
@main_bp.route('/api/stats')
def get_stats():
    try:
        report_count = ReportItem.query.count()
        found_count = FoundItem.query.count()
        total_count = report_count + found_count

        return jsonify({
            'total': total_count,
            'report': report_count,
            'found': found_count
        })

    except Exception as e:
        print(f'통계 조회 오류: {e}')

        return jsonify({
            'error': '통계 데이터를 불러오지 못했습니다.',
            'message': '잠시 후 다시 시도해주세요.'
        }), 500
