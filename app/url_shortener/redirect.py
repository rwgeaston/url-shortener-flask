from flask import redirect
from flask import abort

from .app import app
from .fake_database import shortened_urls

redirect_base = 'r/'


def generate_redirect_url(base_url, redirect_id):
    # Good to define this here so that if we change the /r/ above we remember to change this as well
    return f"{base_url}{redirect_base}{redirect_id}"


@app.route(f'/{redirect_base}<redirect_url>')
def redirect_endpoint(redirect_url):
    if redirect_url not in shortened_urls:
        return abort(404)

    return redirect(
        shortened_urls[redirect_url]['url'],
        code=301,  # Flask uses 302 by default but this is not temporary
    )
