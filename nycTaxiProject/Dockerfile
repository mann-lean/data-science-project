FROM python:3.11-slim

RUN apt-get update -y && apt-get install -y awscli
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["python3","app.py"]