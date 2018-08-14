from string import ascii_letters, digits
from random import choice

from flask import request

from flask_restful import Resource
from flask_restful import abort
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import IntegrityError

import validators

from .app import api
from .app import db
from .models import ShortURL


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

    def generate_slug(self):
        return ''.join([choice(self.valid_character_set) for _ in range(8)])

    def post(self):
        args = parser.parse_args()
        if not args['url']:
            abort(400, message='Must provide a URL to redirect to when POSTing.')

        new_entity = ShortURL(
            slug='',
            original_url=args['url']
        )

        while True:
            # Generate random things until we get an unused one
            # Probably first attempt
            slug = self.generate_slug()
            new_entity.slug = slug
            try:
                new_entity.save()
            except IntegrityError:
                # Need to keep trying until we don't get one
                db.session.rollback()
            else:
                break

        return new_entity.serialise(request.url_root), 201


class URLShorten(Resource):
    @staticmethod
    def get(slug):
        return ShortURL.get_by_slug(slug).serialise(request.url_root)

    def put(self, slug):
        return self.patch(slug)

    @staticmethod
    def patch(slug):
        entity = ShortURL.get_by_slug(slug)
        args = parser.parse_args()
        if 'url' in args:
            # This is ok because there's only one field to set but there must be a nicer way.
            entity.original_url = args['url']

        entity.save()
        return entity.serialise(request.url_root), 201

    @staticmethod
    def delete(slug):
        entity = ShortURL.get_by_slug(slug)
        entity.delete()
        return slug, 204


api.add_resource(URLShorten, '/short_url/<slug>')
api.add_resource(URLShortenPost, '/shorten_url')
