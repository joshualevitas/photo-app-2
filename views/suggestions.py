from flask import Response, request
from flask_restful import Resource
from models import User, db
from views import get_authorized_user_ids
import json
import sys


##ec

male_set = []
female_set = []


with open("other-files/male.txt","r") as males:
    male_names = males.readlines() # returns only the first line as string and iterates over this string

for name in range(len(male_names)):
    male_names[name] = male_names[name][:-1]

with open("other-files/female.txt","r") as females:
    female_names = females.readlines() # returns only the first line as string and iterates over this string

for name in range(len(female_names)):
    female_names[name] = female_names[name][:-1]



def get_gender(user): #gets user dict
    if user["first_name"] in male_names:
        return "male"
    elif user["first_name"] in female_names:
        return "female"
    else: return "unsure"


##


class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # suggestions should be any user with an ID that's not in this list:
        # print(get_authorized_user_ids(self.current_user))
        user_ids_tuples = (
            db.session
            .query(User.id)
            .all()
         )

        user_ids = [id for (id,) in user_ids_tuples]
        users = []

        # current_gender = get_gender(self.current_user)


        for id in user_ids:
            if id not in get_authorized_user_ids(self.current_user):
                user_profile = User.query.get(id)
                users.append(user_profile)

        users_json = [user.to_dict() for user in users][:7]
        
        # ret = []
        # for u in users_json:
        #     if get_gender(u['first_name']) == current_gender:
        #         ret.append(u)
        #     if len(ret) > 7:
        #         break
        
        # ret = ret[:7]
        


        return Response(json.dumps(users_json), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
