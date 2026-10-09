# app.py

from flask import Flask
from routes.main import main_bp
from routes.register import register_bp
from routes.search import search_bp

app = Flask(__name__)

# 페이지 라우트 등록
app.register_blueprint(main_bp)
app.register_blueprint(register_bp)
app.register_blueprint(search_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
