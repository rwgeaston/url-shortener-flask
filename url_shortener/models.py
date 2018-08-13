from .app import db


class ShortURL(db.Model):
    __tablename__ = 'shorturls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_url = db.Column(db.String(10), nullable=False)
    original_url = db.Column(db.String(255), nullable=False)

    def __init__(self, short_url, original_url):
        self.short_url = short_url
        self.original_url = original_url
