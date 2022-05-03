from flask import Response, request
from flask_restful import Resource
from models import LikePost, db, Post
from views import can_view_post, get_authorized_user_ids
import json

from views import can_view_post

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "like_post" based on the data posted in the body 

        body = request.get_json()
        print(body)

        #check for post_id 
        post_id = body.get('post_id')

        if not post_id:
            return Response(json.dumps({'message':"need an id".format(id)}),  mimetype="application/json", status=404)
        
        #need to check if post id is an integer: 
        try:
            post_id = int(post_id)
        except:
            return Response(json.dumps({'message':"id must be an int"}), status=400)

        #check if the post exists 
        post = Post.query.get(post_id)
        if not post:
            return Response(json.dumps({'message':"post doesn't exist".format(id)}),  mimetype="application/json", status=404)

        #authorized users:
        user_ids = get_authorized_user_ids(self.current_user)
        if post.user_id not in user_ids:
            return Response(json.dumps({'message':"id is invalid"}), status=404)
    
        likeposts = LikePost.query.filter(LikePost.post_id == post_id)
        for likepost in likeposts:
            if likepost.user_id == self.current_user:
                return Response(json.dumps({'message': "youve already liked this post"}), mimetype="application/json", status=400) 

        new_like = LikePost(self.current_user.id, post_id)
        db.session.add(new_like)
        db.session.commit()
        return Response(json.dumps(new_like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "like_post" where "id"=id
        print(id)
        likepost = LikePost.query.get(id)
        
        if not likepost:
            return Response(json.dumps({'message':'id is invalid'}),  mimetype="application/json", status=404)

        # you should only be able to edit/delete posts that are yours
        if likepost.user_id != self.current_user.id:
             return Response(json.dumps({'message':'not allowed to edit this post'}),  mimetype="application/json", status=404)

        LikePost.query.filter_by(id=id).delete() 
        db.session.commit()
        return Response(json.dumps({'message':'like deleted'}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
