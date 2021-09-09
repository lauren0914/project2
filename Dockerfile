FROM python:3.9.0

WORKDIR /home/

RUN git clone https://github.com/lauren0914/project2.git

WORKDIR /home/project2/

RUN echo "SECRET_KEY=django-insecure-8(v8$esa5eq4!j$dl@z^&#2_2j7xb*vl77!hno)$#--fo#&^c%" > .env

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN python manage.py migrate

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "project2.wsgi", "--bind", "0.0.0.0:8000"]