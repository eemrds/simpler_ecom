
FROM python:3.9
WORKDIR /app
COPY . /app/

RUN pip install /app/packages/*

EXPOSE 8080

CMD ["uvicorn", "simple_api:app", "--host", "0.0.0.0", "--port", "8080"]