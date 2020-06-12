from django.db import models
from django.contrib.auth import get_user_model
import json
from django.urls import reverse


class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    # image_url = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    meta = models.TextField(default=json.dumps({"github":{}, "twitter":{}, "linkedin":{}}))

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['phone_number',]),
        ]

        
    def get_absolute_url(self): # new
        return reverse('user-detail', args=[str(self.id)])
