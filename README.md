# Example API

This is built as an example simple CRUD Python API, using Flask, Yoyo-migrations, Postgresql, and Pypika.

## Dev

Install Docker and Python version 3.11

**Install Python Dependencies**
`pip install -r requirements.txt`

**Activate Dev DB**
`docker-compose up`

**Run Migrations**
`yoyo apply`

**Run API locally**
`flask --app src/api run`


Use tool like Postman to test out any of the endpoints.