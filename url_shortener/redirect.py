from flask import redirect

from .app import app
from .models import ShortURL
from .models import redirect_base


@app.route(f'/{redirect_base}<slug>')
def redirect_endpoint(slug):
    entity = ShortURL.get_by_slug(slug)

    return redirect(
        entity.original_url,
        code=301,  # Flask uses 302 by default but this is not temporary
    )
