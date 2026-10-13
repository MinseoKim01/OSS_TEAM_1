# Flask에 DB 관련 기능을 추가하는 확장

# extensions.py (공통 객체 정의 파일)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 공통 DB 객체 / 마이그레이션 객체 생성
# app.py에서 앱과 연결 (models.py에서 같은 객체를 사용)
db = SQLAlchemy()
migrate = Migrate()