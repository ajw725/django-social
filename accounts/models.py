from django.db import models
from django.contrib.auth import models as auth_models


class User(auth_models.User, auth_models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)
