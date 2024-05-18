FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requiriments.txt ./requiriments.txt

RUN pip install -r requiriments.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]