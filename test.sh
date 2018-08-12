#!/bin/bash
ln -sf "$PWD/test.sh" .git/hooks/pre-commit

pylint url_shortener
rc=$?;
if [[ $rc != 0 ]];
then
    echo "Fix pylint"
    exit $rc;
fi

python -m unittest discover -p "*_tests.py"
rc=$?;
if [[ $rc != 0 ]];
then
    echo "Fix unit tests"
    exit $rc;
fi

echo "Tests pass";
exit 0;
