FROM python:3.6.10-buster

WORKDIR /api

COPY app.py config.py requirements.txt  /api/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","app.py"]


