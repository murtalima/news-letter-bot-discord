FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]