FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask google-generativeai

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
