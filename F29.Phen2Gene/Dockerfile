FROM python:3.6

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app

EXPOSE 8080

WORKDIR /app

RUN ls

ENTRYPOINT ["python", "app.py"]
