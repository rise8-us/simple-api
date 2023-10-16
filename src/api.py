from flask import Flask
from flask import request
from . import schema
from . import db
from .validation import verify, optional, to_search_schema

app = Flask(__name__)

@app.get("/repositories")
def get_repositories():
    request_args = request.args.to_dict()
    if (errors := verify(request_args, to_search_schema(schema.repository_schema), exclusive=True)):
        return {"validation errors": errors}, 409
    return db.select("repositories", search=request_args)

@app.get("/teams")
def get_teams():
    return db.select("teams", search=request.args.to_dict())

@app.post("/repositories")
def add_repository():
    request_body = request.get_json()
    if (errors := verify(request_body, schema.repository_schema, exclusive=True)):
        return {"validation errors": errors}, 409
    return db.insert("repositories", request_body)

@app.put("/repositories")
def update_repository():
    request_body = request.get_json()
    if (errors := verify(request_body, schema.repository_schema, exclusive=True)):
        return {"validation errors": errors}, 409
    return db.update("repositories", request_body, {"name": request_body["name"]})
