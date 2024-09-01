FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/ .

RUN mkdir /repo
ENV REPO_PATH=/repo

CMD ["python", "./main.py"]