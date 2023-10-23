from flask_restx import fields

repository_schema = {
    "id": int,
    "name": str,
    "onboarding_date": str,
    "team": str,
    "status": str
}

repository_model = {
    "id": fields.Integer,
    "name": fields.String,
    "onboarding_date": fields.String,
    "team": fields.String,
    "status": fields.String
}

repository_description = {
    "id": "A Repository's ID",
    "name": "A Repository's Name",
    "onboarding_date": "A Repository's Onboarding Date",
    "team": "A Repository's Team",
    "status": "A Repository's Status"
}