# Dockerfile, Image, Container
# Dockerfile = blueprint
# Image = template to run container
# Container = runs the server

FROM python:3.9-slim

ADD . .

RUN pip install -r requirements.txt

RUN pip install gunicorn

EXPOSE 8000

CMD ["./startserver.sh"]
