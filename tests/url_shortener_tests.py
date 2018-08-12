import random
from unittest import TestCase

from url_shortener.app import app


class URLShortenerTests(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_post_url_check_redirect(self):
        # This should make random.choice within the app predictable
        # This only matters so we get the same redirect url every time
        # Which isn't that important, but I do not like random factors within unit tests
        random.seed(1)
        random_id = 'iK2ZWeqh'  # This won't change if seed doesn't

        response = self.app.post('/shorten_url', data={'url': 'https://rwgeaston.com'})

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

        response = self.app.get(f'/r/{random_id}')

        self.assertEqual(response.status_code, 301)
        self.assertIn(
            "https://rwgeaston.com",
            response.data.decode('utf8'),
        )
