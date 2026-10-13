# app.py
import os

from dotenv import load_dotenv
from flask import Flask

from extensions import db, migrate
from routes.main import main_bp
from routes.register import register_bp
from routes.search import search_bp

# 개인 환경 설정 (.env) 로딩
load_dotenv()

# 앱 생성
app = Flask(__name__)

# DB 접속 정보 설정 (DATABASE_URL을 Flask의 SQLALCHEMY_DATABASE_URI에 전달)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

# DB 객체와 앱 연결
db.init_app(app)

# 테이블 정의 로딩 (마이그레이션에서 테이블을 인식하기 위함)
import models

# 마이그레이션 도구 연결
migrate.init_app(app, db)

# 페이지 라우트 등록
# Blueprint : 주소별 처리 함수를 묶는 Flask 구성 단위
# app.py에서 각 객체를 가져와 앱에 등록하는 것
app.register_blueprint(main_bp)
app.register_blueprint(register_bp)
app.register_blueprint(search_bp)

# 직접 실행 시 서버 시작
if __name__ == "__main__":
    app.run(debug=True, port=5000)
