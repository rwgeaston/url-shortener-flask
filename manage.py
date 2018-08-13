import unittest

from flask.cli import FlaskGroup

from url_shortener.app import app
from url_shortener.app import db


cli = FlaskGroup(app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    tests = unittest.TestLoader().discover('tests', pattern='*tests.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return not result.wasSuccessful()


if __name__ == '__main__':
    cli()
