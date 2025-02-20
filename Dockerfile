FROM python:3.9-alpine

WORKDIR /app

COPY src/app.py .

RUN pip install flask requests

EXPOSE 80

CMD ["python", "app.py"]
