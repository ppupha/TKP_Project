from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
    # the relationship between class UserInfo and class User is one-to-one
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Info")

    user_fullname = models.CharField(max_length=30, blank=False, null=True)

    # user_description is required
    user_description = models.TextField(max_length=218, blank=False, null=True)
    # user_avatar is not required
    user_avatar = models.ImageField(upload_to='user_avatar', default='user_avatar/default-avatar.png', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create UserInfo if not created
User.Info = property(lambda u: UserInfo.objects.get_or_create(user=u)[0])
