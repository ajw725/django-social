import misaka

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from groups.models import Group

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null=False, blank=False)
    message_html = models.TextField(null=False, blank=False, editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username,
                                               'pk': self.pk})
