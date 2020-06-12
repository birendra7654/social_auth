from .models import UserProfile
from django.contrib.auth import get_user_model
import requests
from urllib.parse import parse_qs
from requests_oauthlib import OAuth1Session
import os
import json

def create_update_user(email, platform, meta_data, name):
    user,created = get_user_model().objects.get_or_create(username=email)
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        profile.name = name
        profile.email = email
    meta = json.loads(profile.meta)
    meta[platform] = meta_data
    profile.meta = json.dumps(meta)
    profile.save()
    return user
    
def get_linkedin_meta(access_token):
    user_meta = requests.get('https://api.linkedin.com//v2/me/', headers={"Authorization" : "Bearer {}".format(access_token)})
    user_email = requests.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))', headers={"Authorization" : "Bearer {}".format(access_token)})
    email = user_email.json()["elements"][0]["handle~"]["emailAddress"]
    user_meta = user_meta.json()
    return user_meta, email
    


def get_twitter_token():
    request_token = OAuth1Session(client_key=os.environ["twitter_key"],
            client_secret=os.environ["twitter_secret"])
    url = 'https://api.twitter.com/oauth/request_token'
    data = request_token.get(url)
    data_token = parse_qs(data.text)
    return data_token["oauth_token"][0]
    
