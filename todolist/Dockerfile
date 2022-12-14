FROM python:3.9-slim


WORKDIR /todolist
COPY ./ /todolist

ENV SECRETKEY=mykey

EXPOSE 8000

RUN apt update
RUN apt install net-tools -y

RUN pip install -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT ["python", "main.py"]