from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('user/all/', views.UserList.as_view(), name="users"),
    path('user/search/', views.UserSearch.as_view(), name="users"),
    path('user/<int:pk>', views.UserDetail.as_view(), name="user-detail"),
    path('user/<int:pk>/set-password/', views.SetPassword.as_view(), name="set-password"),
    
    # APIS
    path('api/users/', api.UserListAPI.as_view(), name="users-api"),
    path('api/user/<int:pk>', api.UserDetailAPI.as_view(), name="user-detail-api"),
]

