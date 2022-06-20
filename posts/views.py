from braces.views import SelectRelatedMixin

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic

from . import forms, models

User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
    post_user = None

    def get_queryset(self):
        try:
            username = self.kwargs.get('username')
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=username)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        username = self.kwargs.get('username')
        return super().get_queryset().filter(user__username__iexact=username)


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Post
    fields = ('message', 'group')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted')
        return super().delete(request, *args, **kwargs)
