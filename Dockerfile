FROM python:alpine

WORKDIR /django

COPY . .

RUN pip install -r requirements.txt

CMD ["python","manage.py","runserver"]

EXPOSE 8000:8000


