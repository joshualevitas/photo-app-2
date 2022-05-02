from flask import Response, request
from flask_restful import Resource
from models import Following
import json
from views import can_view_post, get_authorized_user_ids
from models import Post, db, Following, User

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        id = self.current_user.id
       
        #1 get every user id 
        #2 for every user id, check if they are follwoing the current user 
        user_ids_t = (
            db.session
            .query(User.id)
            .all()
        )

        user_ids = []

        for user in user_ids_t:
            if id in get_authorized_user_ids(user): 
                user_ids.append(user)

        followers_json = [user.to_dict for user in user_ids]  

        '''
        People who are following the current user.
        In other words, select user_id where following_id = current_user.id
        '''
        return Response(json.dumps(followers_json), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
