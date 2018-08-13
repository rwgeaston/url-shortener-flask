from flask.cli import FlaskGroup

from url_shortener.app import app
from url_shortener.app import db


cli = FlaskGroup(app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
