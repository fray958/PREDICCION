FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt

WORKDIR /app/backend

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]