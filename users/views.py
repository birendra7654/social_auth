from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.views import View
from accounts.models import UserProfile
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from .serializers import UserProfileSerializer
from .forms import PasswordForm
from django.urls import reverse, resolve


class Home(View):
    def get(self, request):
        return HttpResponseRedirect('/accounts/login/')


class UserDetail(DetailView):
    model = UserProfile

    def get_context_data(self, object):
        return UserProfileSerializer(object).data

    def get(self, request, pk):
        userprofile = self.get_context_data(object=self.get_object())
        return render(request, 'users/userprofile_detail.html', {"userprofile":userprofile})


class UserList(ListView):
    model = UserProfile
    template_name = "users/userprofile_list.html"


class UserSearch(ListView):
    model = UserProfile
    template_name = "users/user_search.html"


    def get_queryset(self, *args, **kwargs):
        phone_number = self.request.GET.get('phone_number')
        if phone_number:
            return UserProfile.objects.filter(phone_number=phone_number)
        return []



class SetPassword(UpdateView):
    form_class = PasswordForm
    template_name = "users/set_password.html"
    queryset = UserProfile.objects.all()

    def get(self, request, pk):
        return render(request, self.template_name, {"form":self.form_class, "success":True if request.GET.get('success') else False})
            
    def post(self, request, pk):
        profile = self.get_object()
        form= self.form_class(data=request.POST)
        if form.is_valid():
            profile.user.set_password(form.cleaned_data["password"])
            profile.user.save()
            return HttpResponseRedirect('/user/{}/set-password/?success=1'.format(pk))
            # return HttpResponseRedirect(reverse('set-password', kwargs={'pk': pk}))
        return render(request, self.template_name, {"form":form})

