from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        body = request.get_json()
        print(body)
        
        text = body.get('text')
        post_id = body.get('post_id')

        post = Post.query.get(post_id)
        
        if not text and not post_id:
            return Response(json.dumps({"need a caption and id".format(id)}),  mimetype="application/json", status=400)
    
        new_comment = Comment(text, self.current_user.id, post.id)
        db.session.add(new_comment)
        db.session.commit()

        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # delete "Comment" record where "id"=id
        print(id)
        comment = Comment.query.get(id)
        
        if not comment:
            return Response(json.dumps({'id is invalid'}.format(id)),  mimetype="application/json", status=400)

        # you should only be able to edit/delete posts that are yours
        if comment.user_id != self.current_user.id:
             return Response(json.dumps({'not allowed to edit this post'.format(id)}),  mimetype="application/json", status=400)

        Comment.query.filter_by(id=id).delete() 
        db.session.commit()
        return Response(json.dumps({'comment deleted'.format(id)}), mimetype="application/json", status=201)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
