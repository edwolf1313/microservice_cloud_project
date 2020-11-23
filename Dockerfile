FROM python:3.7.9

ENV PYTHONDONTWRITEBYTHECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /home/ec-user/session_user_service/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./


