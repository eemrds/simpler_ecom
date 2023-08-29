
FROM python:3.10
WORKDIR /app
COPY . /app/

RUN pip install /app/packages/*
RUN pip install /app/packages/*

# RUN pip install pymongo

ENTRYPOINT ["python3", "/app/simple_api.py"]