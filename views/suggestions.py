from flask import Response, request
from flask_restful import Resource
from models import User, db
from views import get_authorized_user_ids
import json


class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        #suggestions should be any user with an ID that's not in this list:
        print(get_authorized_user_ids(self.current_user))
        user_ids_tuples = (
            db.session
            .query(User.id)
            .all()
        )

       
        user_ids = [id for (id,) in user_ids_tuples]
        users = []

        for id in user_ids:
            if id not in get_authorized_user_ids(self.current_user):
                user_profile = User.query.get(id)
                users.append(user_profile)


        users_json = [user.to_dict() for user in users][:7]

        return Response(json.dumps(users_json), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
