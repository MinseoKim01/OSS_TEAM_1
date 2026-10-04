# app.py

from flask import Flask
from routes.main import main_bp

app = Flask(__name__)

# 메인 라우트 등록
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    app.run(debug=True, port=5000)