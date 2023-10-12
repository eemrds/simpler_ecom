
FROM python:3.10
WORKDIR /app
COPY . /app/

RUN pip install /app/packages/*

EXPOSE 8080

CMD ["uvicorn", "your_filename:app", "--host", "0.0.0.0", "--port", "80"]