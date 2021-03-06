
To run locally, you need recent versions of docker and docker-compose. Run 

    docker-compose up

from root folder. Once it's set up you can either kill this temporarily or go to another window to run

    docker-compose run web python manage.py recreate_db

to make the database table needed.

You can also use ./test.sh to check pylint and unit tests are working. Note that running this the first time will add itself to the git pre-commit hooks, so that one does not forget to run the unit tests before committing :) You need a python3.6 virtualenv + pip install -r local_requirements.txt for this.

POST to /shorten_url with {"URL": "some valid URL"} to create a short URL to this. Response will include:

    url - same one you sent
    slug - some short random string which will be used in the redirect link
    shortened_url - full URL to call to get the redirect including root of this server
    relative_shortened_url - link like r/slug which can be used relative to this server

GET the shortened_url from this response will return a 301 Permanent redirect to your original URL. There are two approaches a URL shortener service could take here - returning the redirect or returning the actual response data from the original URL (acting as a proxy).

The proxy option would create far more load on this service by both having bigger response data and adding the latency of waiting for the response of the original URL. I would probably also mess up your headers and therefore (assuming it's some kind of responsive web page) you would not get an appropriate response for your system/browser. So only redirect is offered.

There are also some REST endpoints for modifying the redirects already created - send GET, PUT/PATCH (behaves the same in this case) and DELETE requests to /short_url/slug using the random_id you got back from the original POST. In a public facing system, it would be sensible to require an admin token on these endpoints whilst the POST and GET/redirect endpoints could be fully public.
