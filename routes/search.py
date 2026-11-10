# routes/search.py

from datetime import date

from flask import Blueprint, abort, render_template, request

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
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    searched = any(
        field in request.args for field in ('keyword', 'start_date', 'end_date')
    )
    results = []

    if searched:
        try:
            start_date = date.fromisoformat(start_date) if start_date else None
            end_date = date.fromisoformat(end_date) if end_date else None
        except ValueError:
            abort(400, description='날짜 형식이 올바르지 않습니다.')

        for model, item_type, date_field in (
            (ReportItem, 'report', ReportItem.notice_date),
            (FoundItem, 'found', FoundItem.found_date),
        ):
            query = model.query
            if start_date is not None:
                query = query.filter(date_field >= start_date)
            if end_date is not None:
                query = query.filter(date_field <= end_date)

            for item in query.all():
                if matches_keyword(keyword, item.item_name):
                    results.append((item, item_type))

    return render_template(
        'search.html',
        keyword=keyword,
        searched=searched,
        results=results,
    )
