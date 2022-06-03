# Dockerfile, Image, Container
FROM python:3.8

WORKDIR /code
COPY . /code/
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
ADD . /code
CMD ["python", "./main.py"]
