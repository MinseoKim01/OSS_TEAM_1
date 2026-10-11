# routes/search.py

from flask import Blueprint, render_template

# 검색 화면용 Blueprint 객체
search_bp = Blueprint('search', __name__)

# 여기에 /search 주소와 처리 함수를 연결
# 브라우저의 /search요청 -> search_bp -> search() -> templates/search.html로 연결
@search_bp.route('/search')
def search():
    return render_template('search.html')
