# loud-stream-api
### Description
Api for loud-stream project : a SoundCloud like application

### Framework
FastApi

### Running the app
- install python:3.10
- run `pip install --no-cache-dir --upgrade -r requirements.txt`
- create an `aws s3 bucket`
- install [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and run `aws config` to authenticate yourself
- create a `.env.example` file where you have to override empty values from `.env`
- run `docker-compose up` to run the `postgreSQL` database container
- run `uvicorn sql_app.main:app --reload` and the app is up and running 👍

### Testing the app
- run `ENV=test pytest` 🧪

### Migrations
- run `alembic revision --autogenerate -m "<revision message>"` to create a revision file
- run `alembic upgrade head` or `alembic upgrade +<N>` or `alembic upgrade <revision tag>` to migrate
- run `alembic downgrade -<N>` or `alembic downgrade <revision tag>` to rollback