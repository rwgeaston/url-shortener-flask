FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
