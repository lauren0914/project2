FROM python:3.9.0

WORKDIR /home/

RUN echo 'lksmaoidmf'

RUN git clone https://github.com/lauren0914/project2.git

WORKDIR /home/project2/

RUN echo "SECRET_KEY=django-insecure-8(v8$esa5eq4!j$dl@z^&#2_2j7xb*vl77!hno)$#--fo#&^c%" > .env

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient


EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=project2.settings.deploy && python manage.py migrate --settings=project2.settings.deploy && gunicorn --env DJANGO_SETTINGS_MODULE=project2.settings.deploy project2.wsgi --bind 0.0.0.0:8000"]