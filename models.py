from extensions import db


class ReportItem(db.Model):
    """학과 단톡방 공지로 접수한 제보형 게시글."""

    __tablename__ = "report_items"

    id = db.Column(db.Integer, primary_key=True)
    notice_date = db.Column(db.Date, nullable=False)
    notice_time = db.Column(db.Time, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    chat_room_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text, nullable=False) 
    


class FoundItem(db.Model):
    """오프라인에서 직접 습득한 물건의 게시글."""

    __tablename__ = "found_items"

    id = db.Column(db.Integer, primary_key=True)
    found_date = db.Column(db.Date, nullable=False)
    found_time = db.Column(db.Time, nullable=False)
    found_location = db.Column(db.String(200), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    storage_location = db.Column(db.String(200), nullable=False)
    password_hash = db.Column(db.Text, nullable=False) 
