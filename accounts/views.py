from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from urllib.parse import parse_qs
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from requests_oauthlib import OAuth1Session
import requests
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import LoginForm
import os
from .utils import (
    create_update_user,
    get_twitter_token,
    get_linkedin_meta,
)

class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/profile/')
        return render(request, 'login.html', {"form": self.form_class(), 
                "linkedin_key":os.environ["linkedin_key"], "github_key":os.environ["github_key"]})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data["email"])
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/')
        return render(request, 'login.html', {"form":form})


class LogOutView(LoginRequiredMixin, View):
    
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/accounts/login/')


class LinkedInLoginCallbackView(View):
    
    def get(self, request):
        payload = {
            "grant_type":"authorization_code",
            "code":request.GET.get('code'),
            "redirect_uri":'http://localhost:8000/accounts/login/linkedin/callback/',
            "client_id":os.environ["linkedin_key"] ,
            "client_secret":os.environ["linkedin_secret"]
        }
        r = requests.get('https://www.linkedin.com/uas/oauth2/accessToken', params=payload, headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            user_meta, email = get_linkedin_meta(r.json()["access_token"])
            user = create_update_user(email, "linkedin", user_meta, "{} {}".format(user_meta["localizedFirstName"], user_meta["localizedLastName"]))
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/')

        return HttpResponse(r.text)


class TwitterLoginView(View):
    
    def get(self, request):
        token = get_twitter_token()
        return HttpResponseRedirect('https://api.twitter.com/oauth/authenticate?oauth_token={}'.format(token))
        

class TwitterLoginCallbackView(View):
    
    def get(self, request):
        url = 'https://api.twitter.com/oauth/access_token'
        data = {"oauth_verifier": request.GET.get('oauth_verifier') ,  "oauth_token":request.GET.get('oauth_token')}
        
        access_token_data = requests.post(url, params=data)
        if access_token_data.status_code == 200:
            data = parse_qs(access_token_data.text)
            oauth_user = OAuth1Session(client_key=os.environ["twitter_key"],
                                       client_secret=os.environ["twitter_secret"],
                                       resource_owner_key=data["oauth_token"][0],
                                       resource_owner_secret=data["oauth_token_secret"][0])
            url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
            params = {"include_email": 'true'}
            user_data = oauth_user.get(url_user, params=params)
            if user_data.status_code == 200:
                user_data = user_data.json()        
                user = create_update_user(user_data["email"], "twitter", user_data, user_data["name"])
                login(request, user)
                return HttpResponseRedirect('/accounts/profile/')
            return HttpResponse(user_data.text)
        return HttpResponse(access_token_data.text)



class ProfileView(LoginRequiredMixin, View):    
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'profile.html', {"name":profile.name})


class GitHubLoginCallBackView(View):
    
    def get(self, request):
        if request.GET.get('code'):
            r = requests.post('https://github.com/login/oauth/access_token',
              {"client_id": os.environ["github_key"],
               "client_secret": os.environ["githum_secret"],
               "code": request.GET.get('code')}, 
               headers={"Contet-Type":"application/json"}
            )
            if r.status_code == 200:
                data = parse_qs(r.text)
                if data.get("access_token"):
                    emails = requests.get('https://api.github.com/user/emails', params={"access_token": data["access_token"][0]})
                    auth_result = requests.get('https://api.github.com/user', params={"access_token": data["access_token"][0]})
                    # [{'email': 'ankushv.1106@gmail.com', 'primary': True, 'verified': True, 'visibility': 'private'}, {'email': '50256848+ank1106@users.noreply.github.com', 'primary': False, 'verified': True, 'visibility': None}]
                    if auth_result.status_code == emails.status_code == 200:
                        email = [email["email"] for email in emails.json() if email["primary"] and email["verified"]]
                        auth_result = auth_result.json()
                        if email:
                            user = create_update_user(email[0], "github", auth_result, auth_result["login"])
                            login(request, user)
                            return HttpResponseRedirect('/accounts/profile/')
                    return JsonResponse({"error":"Something went wrong"}, status=400)
        return JsonResponse({"error":"Invalid request"}, status=400) 



