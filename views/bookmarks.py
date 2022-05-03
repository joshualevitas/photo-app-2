from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db, Post
from views import can_view_post, get_authorized_user_ids
import json

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):

        bookmarks = Bookmark.query.filter(Bookmark.user_id == self.current_user.id)
        bookmarks_json = [bookmark.to_dict() for bookmark in bookmarks]

        return Response(json.dumps(bookmarks_json), mimetype="application/json", status=200)

    def post(self):
        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        post_id = body.get('post_id')
        if not body.get('post_id'):
            return Response(json.dumps({'message': "need id"}), mimetype="application/json", status=400)

        bookmarks = Bookmark.query.filter(Bookmark.user_id == self.current_user.id)
        for bookmark in bookmarks:
            if bookmark.post_id == body.get('post_id'):
                return Response(json.dumps({'message': "already exists in bookmarks"}), mimetype="application/json", status=400) 

        curr = body.get('post_id')
        try:
            curr = int(curr)
        except: 
            return Response(json.dumps({'message': 'not a valid id'}), mimetype="application/json", status=400)
        

        post = Post.query.get(post_id)
        if not post:
            return Response(json.dumps({'message':"post doesn't exist".format(id)}),  mimetype="application/json", status=404)

        #need to get authorized users 
        user_ids = get_authorized_user_ids(self.current_user)
        if post.user_id not in user_ids:
            return Response(json.dumps({'message':"id is invalid"}), status=404)

        book = Post.query.filter_by(id = curr).filter(Post.user_id.in_(user_ids)).all()

        if not book:
            return Response(json.dumps({'message': 'not a bookmark'}), mimetype="application/json", status=201)
        
        # follwoing = Bookmark.query.filter_by(user_id = self.current_user.id).filter_by(post_id = curr)
        # if len(follwoing) > 0:
        #     return Response(json.dumps({}), mimetype="application/json", status=400)
        
        new_book = Bookmark(self.current_user.id, curr)

        db.session.add(new_book)
        db.session.commit()

        return Response(json.dumps(new_book.to_dict()), mimetype="application/json", status=201)
        

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "bookmark" record where "id"=id
        print(id)
        bookmark = Bookmark.query.get(id)
        
        if not bookmark:
            return Response(json.dumps({'message': 'not a bookmark'}),  mimetype="application/json", status=404)

        # you should only be able to edit/delete posts that are yours
        if bookmark.user_id != self.current_user.id:
             return Response(json.dumps({'message': 'cannot delete this bookmark'}),  mimetype="application/json", status=404)

        Bookmark.query.filter_by(id=id).delete() 
        db.session.commit()
        return Response(json.dumps({'message':'bookmark deleted'}), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
