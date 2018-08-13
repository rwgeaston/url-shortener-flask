from .app import db

redirect_base = 'r/'


class ShortURL(db.Model):
    __tablename__ = 'shorturls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(10), nullable=False)
    original_url = db.Column(db.String(255), nullable=False)

    def __init__(self, slug, original_url):
        self.slug = slug
        self.original_url = original_url

    def serialise(self, url_root):
        return {
            'id': self.slug,
            'url': self.original_url,
            'shortened_url': self.generate_redirect_url(url_root),
            'relative_shortened_url': self.generate_redirect_url(''),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).first_or_404()

    def generate_redirect_url(self, base_url):
        # Good to define this here so that if we change the /r/ above we remember to change this as well
        return f"{base_url}{redirect_base}{self.slug}"
