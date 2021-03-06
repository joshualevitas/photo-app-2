from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
from views import can_view_post, get_authorized_user_ids
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):

        following = Following.query.filter_by(user_id = self.current_user.id)
        following_json = [follower.to_dict_following() for follower in following]

        # return all of the "following" records that the current user is following
        return Response(json.dumps(following_json), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "following" record based on the data posted in the body 
        body = request.get_json()
        print(body)

        #check if given user id 
        new_user_id = body.get('user_id')
        if not new_user_id:
            return Response(json.dumps({'message': 'not a valid id'}), mimetype="application/json", status=400)

        #check if id is integer
        try:
            new_user_id = int(new_user_id)
        except: 
            return Response(json.dumps({'message': 'not a valid id'}), mimetype="application/json", status=400)

        #check if user is in user ids 
        user = User.query.get(new_user_id)
        if not user:
            return Response(json.dumps({'message': 'not a valid id'}), mimetype="application/json", status=404)

        # #check already following 
        following = Following.query.filter_by(user_id = self.current_user.id)
        for follower in following:
            if follower.following_id == new_user_id:
                return Response(json.dumps({'message': "already exists in following"}), mimetype="application/json", status=400) 


        new_following = Following(user_id = self.current_user.id, following_id = new_user_id)
        db.session.add(new_following)
        db.session.commit()
        return Response(json.dumps(new_following.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "following" record where "id"=id
        print(id)
        follower = Following.query.get(id)
        
        if not follower:
            return Response(json.dumps({'message':'id is invalid'}),  mimetype="application/json", status=404)

        # you should only be able to edit/delete posts that are yours
        if follower.user_id != self.current_user.id:
             return Response(json.dumps({'message':'not allowed to delete'}),  mimetype="application/json", status=404)

        Following.query.filter_by(id=id).delete() 
        db.session.commit()
        return Response(json.dumps({'message':'follower delete'}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )