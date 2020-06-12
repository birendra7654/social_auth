from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from accounts.models import UserProfile
import json


class UserProfileSerializer(ModelSerializer):
    github = SerializerMethodField()
    linkedin = SerializerMethodField()
    twitter = SerializerMethodField()
    # meta = SerializerMethodField()
    
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def get_github(self, obj):
        return json.dumps(json.loads(obj.meta)["github"], indent=4)
    
    def get_twitter(self, obj):
        return json.dumps(json.loads(obj.meta)["twitter"], indent=4)
    
    def get_linkedin(self, obj):
        return json.dumps(json.loads(obj.meta)["linkedin"], indent=4)


class UserProfileListSerializer(ModelSerializer):
    
    class Meta:
        model = UserProfile
        exclude = ('user', 'meta',)

class UserProfileAPISerializer(ModelSerializer):
    meta = SerializerMethodField()
    
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def get_meta(self, obj):
        return json.loads(obj.meta)
    