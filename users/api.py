from django.shortcuts import render, get_object_or_404
from django.views import View
from accounts.models import UserProfile
import json
from .serializers import UserProfileAPISerializer, UserProfileListSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView




class UserDetailAPI(RetrieveAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileAPISerializer
    lookup_field = 'pk'
    # def get_object(self, object):
    #     return UserProfileSerializer(object).data

    # def get(self, request, pk):
    #     userprofile = self.get_context_data(object=self.get_object())
    #     return render(request, 'users/userprofile_detail.html', {"userprofile":userprofile})


class UserListAPI(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    # lookup_field = "pk"

    # def get_queryset(self):
    #     return UserProfile.objects.all()
