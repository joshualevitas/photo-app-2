from flask import Response, request
from flask_restful import Resource
from models import Following
import json
from views import can_view_post, get_authorized_user_ids
from models import Post, db, Following, User
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        id = self.current_user.id
       
        #1 get every user id 
        #2 for every user id, check if they are follwoing the current user 
        followers = Following.query.filter_by(following_id = self.current_user.id)
        followers_json = [follower.to_dict_follower() for follower in followers]

        # return all of the "following" records that the current user is following
        return Response(json.dumps(followers_json), mimetype="application/json", status=200)

        '''
        People who are following the current user.
        In other words, select user_id where following_id = current_user.id
        '''

def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )