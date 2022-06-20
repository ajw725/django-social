from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Group, GroupMember


class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroupView(generic.DetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(slug=self.kwargs.get('slug'))
        user = request.user
        return super().get(request, *args, **kwargs)


class GroupListView(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(group=group, user=self.request.user)
        except IntegrityError:
            messages.warning(self.request, 'You are already a member of this group.')
        else:
            messages.success(self.request, 'You are now a member of this group.')
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=request.user, group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(request, 'You are not a member of this group.')
        else:
            membership.delete()
            messages.success(request, 'You are no longer a member of this group.')
        return super().get(request, *args, **kwargs)
