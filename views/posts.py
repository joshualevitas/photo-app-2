from multiprocessing import AuthenticationError

# from scipy.fft import idct
from flask import Response, request
from flask_restful import Resource
from models import Post, db, Following
from views import can_view_post, get_authorized_user_ids

import json

#x = 12 
#y = abc
#try:
#x = int(x)
#except: #then will pass the except block 

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):

        args = request.args
        user_ids = get_authorized_user_ids(self.current_user)
        
        try:
            limit = int(args.get('limit') or 10)     
        except: 
           return Response(json.dumps({'message':"the limit parameter is invalid"}), mimetype="application/json", status=400)
       
        if limit > 50:
            limit = 50
            return Response(json.dumps({'message':"the limit parameter is invalid"}), mimetype="application/json", status=400)
           
        posts = Post.query.filter(Post.user_id.in_(user_ids)).limit(limit).all()  #a list of post models getting returned 
        # print(posts[0].to_dict())


        posts_json = [post.to_dict() for post in posts]
        return Response(json.dumps(posts_json), mimetype="application/json", status=200)
       # return Response(json.dumps(['hello world']), mimetype="application/json", status=200)

    def post(self):
        # create a new post based on the data posted in the body 
        body = request.get_json()
        image_url = body.get('image_url')
        
        if not image_url:
            return Response(json.dumps({'message':"image doesn't exist"}),  mimetype="application/json", status=400)

        caption = body.get('caption') 
        alt_text = body.get('alt_text') 

        new_post = Post(image_url, self.current_user.id, caption, alt_text)
        db.session.add(new_post)
        db.session.commit()

        return Response(json.dumps(new_post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        

    def patch(self, id):
        # update post based on the data posted in the body 
        body = request.get_json()
        print(body)

        post = Post.query.get(id)

        if not post:
            return Response(json.dumps({'message':"id is invalid".format(id)}),  mimetype="application/json", status=404)
        
        if post.user_id != self.current_user.id:
            return Response(json.dumps({'message':"id is invalid".format(id)}), mimetype="application/json",  status=404)

        if body.get('caption'):
            post.caption = body.get('caption')
        
        if body.get('alt_text'):
            post.alt_text = body.get('alt_text')

        if body.get('image_url'):
            post.image_url = body.get("image_url")

        db.session.commit()    
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)


    def delete(self, id):
       
        post = Post.query.get(id)
        
        if not post:
            return Response(json.dumps({'message': 'id is invalid'.format(id)}),  mimetype="application/json", status=404)

        # you should only be able to edit/delete posts that are yours
        if post.user_id != self.current_user.id:
             return Response(json.dumps({'message':'id not allowed to edit this post'.format(id)}),  mimetype="application/json", status=404)


        Post.query.filter_by(id=id).delete() 
        db.session.commit()
        return Response(json.dumps({'message':'post deleted'.format(id)}), mimetype="application/json", status=200)


    def get(self, id):  
        
        try:
            id = int(id)
        except:
            return Response(json.dumps({'message':"id must be an int"}), status=404)

        post = Post.query.get(id)
        if not post:           
                return Response(json.dumps({'message':"post doesn't exist "}), status=404)

        user_ids = get_authorized_user_ids(self.current_user)
        if post.user_id not in user_ids:
            return Response(json.dumps({'message':"id is invalid"}), status=404)
        
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )