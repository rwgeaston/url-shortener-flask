#!/bin/bash
ln -sf "$PWD/test.sh" .git/hooks/pre-commit

pylint url_shortener
rc=$?;
if [[ $rc != 0 ]];
then
    echo "Fix pylint"
    exit $rc;
fi

docker-compose run web python manage.py test
rc=$?;
if [[ $rc != 0 ]];
then
    echo "Fix unit tests"
    exit $rc;
fi

echo "Tests pass";
exit 0;
