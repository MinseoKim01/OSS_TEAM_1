# routes/search.py

from flask import Blueprint, render_template, request

from models import FoundItem, ReportItem

# 검색 화면용 Blueprint 객체
search_bp = Blueprint('search', __name__)


def remove_whitespace(value):
    """검색 키워드와 분실물 이름의 공백, 탭, 줄바꿈을 제거한다."""
    return ''.join(value.split())


def matches_keyword(keyword, item_name):
    """공백을 제거한 키워드가 분실물 이름에 포함되는지 반환한다."""
    return remove_whitespace(keyword) in remove_whitespace(item_name)


# 여기에 /search 주소와 처리 함수를 연결
# 브라우저의 /search요청 -> search_bp -> search() -> templates/search.html로 연결
@search_bp.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    searched = 'keyword' in request.args
    results = []

    if searched:
        for model, item_type in ((ReportItem, 'report'), (FoundItem, 'found')):
            for item in model.query.all():
                if matches_keyword(keyword, item.item_name):
                    results.append((item, item_type))

    return render_template(
        'search.html',
        keyword=keyword,
        searched=searched,
        results=results,
    )
