# routes/main.py
from flask import Blueprint, render_template

# 메인 화면용 Blueprint 객체
main_bp = Blueprint('main', __name__)

# 여기에 /주소와 처리 함수를 연결
# 브라우저의 /요청 -> main_bp -> index() -> templates/index.html로 연결
@main_bp.route('/')
def index():
    
    # 게시글 조회 코드 추가 예정
    
    return render_template('index.html')

# 카드 구현 후 삭제 예정 dialog를 확인하는 미리보기 화면
@main_bp.route('/delete-preview')
def delete_preview():
    return render_template('temp.html')
