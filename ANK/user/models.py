from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Userdata(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.FileField(upload_to='userfiles/', null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.owner.username
