# routes/main.py - 메인 대시보드 및 통계 라우트 (공통)
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # 메인 페이지 렌더링 (이후 Supabase 연동 전 기본 틀)
    return render_template('index.html')
    return render_template('index.html', items=items)