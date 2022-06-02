from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post
from views import can_view_post, get_authorized_user_ids
import flask_jwt_extended

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        print(body)
        
        text = body.get('text')
        post_id = body.get('post_id')

        if not post_id:
            return Response(json.dumps({'message':"need an id".format(id)}),  mimetype="application/json", status=400)
        
        if not text:
             return Response(json.dumps({'message':"need a text".format(id)}),  mimetype="application/json", status=400)

        try:
            post_id = int(post_id)

        except: 
             return Response(json.dumps({'message':"post id needs to be an int".format(id)}),  mimetype="application/json", status=400)

        #check if the post exists 
        post = Post.query.get(post_id)
        if not post:
            return Response(json.dumps({'message':"post doesn't exist".format(id)}),  mimetype="application/json", status=404)
        
        #need to get authorized users 
        user_ids = get_authorized_user_ids(self.current_user)
        if post.user_id not in user_ids:
            return Response(json.dumps({'message':"id is invalid"}), status=404)
    
        new_comment = Comment(text, self.current_user.id, post.id)
        db.session.add(new_comment)
        db.session.commit()

        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "Comment" record where "id"=id
        print(id)
        comment = Comment.query.get(id)
        
        if not comment:
            return Response(json.dumps({'message':'id is invalid'}),  mimetype="application/json", status=404)

        # you should only be able to edit/delete posts that are yours
        if comment.user_id != self.current_user.id:
             return Response(json.dumps({'message':'not allowed to edit this post'}),  mimetype="application/json", status=404)

        Comment.query.filter_by(id=id).delete() 
        db.session.commit()
        return Response(json.dumps({'message':'comment deleted'}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )