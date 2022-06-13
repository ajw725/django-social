from django.shortcuts import render

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic as generic_views

from .models import Group, GroupMember


class CreateGroupView(LoginRequiredMixin, generic_views.CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroupView(generic_views.DetailView):
    model = Group


class GroupListView(generic_views.ListView):
    model = Group
