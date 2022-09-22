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
- create a `.env` file inspired from `.env.example`
- run `docker compose up`
- run `uvicorn sql_app.main:app --reload` and the app is up and running 👍

### Testing the app
- run `pytest` 🧪