from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):

        following = Following.query.filter_by(user_id = self.current_user.id)
        following_json = [follower.to_dict_following() for follower in following]

        # return all of the "following" records that the current user is following
        return Response(json.dumps(following_json), mimetype="application/json", status=200)

    def post(self):
        # create a new "following" record based on the data posted in the body 
        body = request.get_json()
        print(body)

        new_user_id = body.get('user_id')

        curr = body.get('user_id')
        try:
            curr = int(curr)
        except: 
            return Response(json.dumps({'message': 'not a valid id'}), mimetype="application/json", status=400)

        users_ids = User.query.all(id) 
        if new_user_id not in users_ids.id: 
            return Response(json.dumps({'message': 'not a valid id'}), mimetype="application/json", status=404)



        following = Following.query.filter_by(user_id = self.current_user.id)
        for follower in following:
            if follower.following_id == body.get('user_id'):
                return Response(json.dumps({'message': "already exists in following"}), mimetype="application/json", status=400) 


        new_following = Following(user_id = self.current_user.id, following_id = new_user_id)

        # #check if already follows -- this doesn't work fix this 
        # following = Following.query.filter_by(user_id = self.current_user.id)
        # if new_following in following:
        #     return Response(json.dumps({'message':'already following'}),  mimetype="application/json", status=400)

        db.session.add(new_following)
        db.session.commit()

        return Response(json.dumps(new_following.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
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
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
