FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app

RUN pip install modus

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
