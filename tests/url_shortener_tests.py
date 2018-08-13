import random
from flask_testing import TestCase

from url_shortener.app import app
from url_shortener.app import db


class URLShortenerTests(TestCase):
    def setUp(self):
        db.create_all()
        db.session.commit()

    def create_app(self):
        app.config.from_object('url_shortener.config.TestingConfig')
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_url_check_redirect(self):
        # This should make random.choice within the app predictable
        # This only matters so we get the same redirect url every time
        # Which isn't that important, but I do not like random factors within unit tests
        random.seed(1)
        random_id = 'iK2ZWeqh'  # This won't change if seed doesn't

        response = self.client.post('/shorten_url', data={'url': 'https://rwgeaston.com'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                'url': 'https://rwgeaston.com',
                'id': random_id,
                'shortened_url': f'http://localhost/r/{random_id}',
                'relative_shortened_url': f'r/{random_id}',
            }
        )

        response = self.client.get(f'/r/{random_id}')

        self.assertEqual(response.status_code, 301)
        self.assertIn(
            "https://rwgeaston.com",
            response.data.decode('utf8'),
        )

    def test_rest_endpoints(self):
        random.seed(2)
        random_id = '9382dffx'

        response = self.client.post('/shorten_url', data={'url': 'https://rwgeaston.com'})
        expected_response = {
            'url': 'https://rwgeaston.com',
            'id': random_id,
            'shortened_url': f'http://localhost/r/{random_id}',
            'relative_shortened_url': f'r/{random_id}',
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), expected_response)

        response = self.client.get(f'/short_url/{random_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_response)

        expected_response['url'] = 'https://rwgeaston.com/admin/'

        response = self.client.patch(f'/short_url/{random_id}', data={
            'url': 'https://rwgeaston.com/admin/',

            # Note we did NOT change this in expected response
            'shortened_url': 'complete nonsense, thankfully will be ignored',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), expected_response)

        response = self.client.delete(f'/short_url/{random_id}')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/short_url/{random_id}')
        self.assertEqual(response.status_code, 404)
