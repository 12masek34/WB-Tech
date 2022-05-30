from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.CharField(max_length=250, null=False)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    read_by = models.ManyToManyField(User, related_name='who_readed', blank=True)

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='who')
    user_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'user_to',)

