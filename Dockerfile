FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask flask-sqlalchemy flask-jwt-extended bcrypt python-dotenv flask-swagger-ui

EXPOSE 5000

CMD ["python3", "app.py"]
