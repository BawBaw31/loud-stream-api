FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./sql_app /app/sql_app

EXPOSE 8000

CMD ["uvicorn", "sql_app.main:app", "--host", "0.0.0.0", "--reload"]
