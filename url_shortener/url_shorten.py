from string import ascii_letters, digits
from random import choice

from flask import request

from flask_restful import Resource
from flask_restful import abort
from flask_restful.reqparse import RequestParser

import validators

from .app import api
from .redirect import generate_redirect_url
from .fake_database import shortened_urls


class URLShortenRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument('url', type=str, help='URL to be shortened')

    def parse_args(self, *args, **kwargs):
        args = super().parse_args(*args, **kwargs)
        if 'url' in args:
            self.validate_url(args['url'])
        return args

    @staticmethod
    def validate_url(url):
        if not validators.url(url):
            abort(400, message=f"{url} is not a valid URL")


parser = URLShortenRequestParser()


class URLShortenPost(Resource):
    valid_character_set = ascii_letters + digits

    def generate_short_url(self):
        return ''.join([choice(self.valid_character_set) for _ in range(8)])

    def post(self):
        args = parser.parse_args()
        if not args['url']:
            abort(400, message='Must provide a URL to redirect to when POSTing.')

        url_id = ''
        while not url_id or url_id in shortened_urls:
            # Generate random things until we get an unused one
            # Probably first attempt
            url_id = self.generate_short_url()

        args['id'] = url_id
        shortened_urls[url_id] = args

        response = {
            'shortened_url': generate_redirect_url(request.url_root, url_id),
            'relative_shortened_url': generate_redirect_url('', url_id),
        }
        response.update(args)
        return response, 201


class URLShorten(Resource):
    @staticmethod
    def get_entity(url_id):
        if url_id not in shortened_urls:
            abort(404, message="Shortened URL {} doesn't exist".format(url_id))

        return shortened_urls[url_id]

    def get(self, url_id):
        return self.get_entity(url_id)

    def put(self, url_id):
        return self.patch(url_id)

    def patch(self, url_id):
        shortened_url = self.get_entity(url_id)
        args = parser.parse_args()
        shortened_url.update(args)
        return shortened_urls

    def delete(self, url_id):
        if self.get_entity(url_id):
            shortened_urls.pop(url_id)

        return url_id, 204


api.add_resource(URLShorten, '/short_url/<url_id>')
api.add_resource(URLShortenPost, '/shorten_url')
