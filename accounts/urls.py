from django.urls import path
from . import views
# from allauth.account.views import LoginView
urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogOutView.as_view()),
    path('login/twitter/', views.TwitterLoginView.as_view()),
    path('login/twitter/callback/', views.TwitterLoginCallbackView.as_view()),
    path('login/linkedin/callback/', views.LinkedInLoginCallbackView.as_view()),
    path('login/github/callback/', views.GitHubLoginCallBackView.as_view()),
    path('profile/', views.ProfileView.as_view(), name="profile"),

]

