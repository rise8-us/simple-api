from flask import Flask
from flask_restx import Api, Resource, fields
from flask import request
from . import schema
from . import db
from .validation import verify, to_search_schema

app = Flask(__name__)
api = Api(app)

repository_model = api.model('Resource', schema.repository_model)

@api.route('/repositories', endpoint='Repositories')
class Repositories(Resource):
    @api.doc(params=schema.repository_description)
    @api.marshal_list_with(repository_model)
    @api.response(200, 'Success')
    @api.response(409, 'Validation Error')
    def get():
        request_args = request.args.to_dict()
        if (errors := verify(request_args, to_search_schema(schema.repository_schema), exclusive=True)):
            return {"validation errors": errors}, 409
        return db.select("repositories", search=request_args)

    @api.expect(repository_model)
    @api.response(200, 'Success')
    @api.response(409, 'Validation Error')
    def post():
        request_body = request.get_json()
        if (errors := verify(request_body, schema.repository_schema, exclusive=True)):
            return {"validation errors": errors}, 409
        return db.insert("repositories", request_body)

    @api.expect(repository_model)
    @api.response(200, 'Success')
    @api.response(409, 'Validation Error')
    def put():
        request_body = request.get_json()
        if (errors := verify(request_body, schema.repository_schema, exclusive=True)):
            return {"validation errors": errors}, 409
        return db.update("repositories", request_body, {"name": request_body["name"]})
