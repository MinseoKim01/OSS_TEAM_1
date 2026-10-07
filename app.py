# app.py
import os

from dotenv import load_dotenv
from flask import Flask

from extensions import db, migrate
from routes.main import main_bp
from routes.register import register_bp
from routes.search import search_bp

load_dotenv()

app = Flask(__name__)

# DB 접속 정보 설정
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

# SQLAlchemy 초기화
db.init_app(app)

# 모델을 로딩해야 마이그레이션에서 테이블을 인식
import models

# 마이그레이션 초기화
migrate.init_app(app, db)

# 페이지 라우트 등록
app.register_blueprint(main_bp)
app.register_blueprint(register_bp)
app.register_blueprint(search_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)