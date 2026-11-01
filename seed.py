"""MVP 공용 더미 데이터 삽입: 가상환경에서 python seed.py 실행."""

import json
from datetime import date, time
from pathlib import Path

from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models import FoundItem, ReportItem


if __name__ == '__main__':
    data_path = Path(__file__).resolve().parent / 'data' / 'demo_items.json'
    data = json.loads(data_path.read_text(encoding='utf-8'))

    with app.app_context():
        for item in data['report_items']:
            item['notice_date'] = date.fromisoformat(item['notice_date'])
            item['notice_time'] = time.fromisoformat(item['notice_time'])
            db.session.add(ReportItem(
                **item, password_hash=generate_password_hash('1234')
            ))

        for item in data['found_items']:
            item['found_date'] = date.fromisoformat(item['found_date'])
            item['found_time'] = time.fromisoformat(item['found_time'])
            db.session.add(FoundItem(
                **item, password_hash=generate_password_hash('1234')
            ))

        db.session.commit()
