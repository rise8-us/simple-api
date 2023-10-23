# Example API

This is built as an example simple CRUD Python API, using Flask, Yoyo-migrations, Postgresql, and Pypika.

## Features
- Comprehensive Swagger docs for each endpoint and Swagger UI at root url
- Query the database and use exact search
- Insert new records into database using JSON
- Modify existing rows in db
- URL Query arg validation
- Request Body validation for PUT and POST requests
- Runs db migrations on app startup, if any need to be run
- tracks db migrations and makes it easy to add new ones using Pypika

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


## To Start

Start by navigating to `localhost:5000` in the browser and using the Swagger UI to test out the endpoints.