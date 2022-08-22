# POSTS MODELS.PY

from django.db import models
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils import timezone
import misaka

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()  # connecting the current post to whoever is logged in as a user

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)
    # time will be auto generated, no need to fill in
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(
        Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_imgs',  null=True, blank=True)

# https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django

    def __str__(self) -> str:
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    @property
    def get_image_url(self):
        if self.image:
            # print(f'SELF IMAGE URL: {self.image.url}')
            return self.image.url
        return None

    @property
    def time_diff(self):
        time_diff = timezone.now() - self.created_at
        if time_diff.days > 0:
            if time_diff.days == 1:
                return f'{time_diff.days} day ago'
            elif time_diff.days > 30:
                return self.created_at.strftime("%b %d")
            return f'{time_diff.days} days ago'
        else:
            time_diff_hrs = int(time_diff.seconds / 3600)
            if time_diff_hrs > 0:
                if time_diff_hrs == 1:
                    return f'{time_diff_hrs} hr ago'
                return f'{time_diff_hrs} hrs ago'
            else:
                return f'{int(time_diff.seconds / 60) } minutes ago'

    class Meta:
        ordering = ['-created_at']  # descending order
        # message is uniquly linked to user
        unique_together = ['user', 'message']


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)
    # author = models.CharField(max_length=200)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    # approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.post.user.username, 'pk': self.post.pk})

    def __str__(self) -> str:
        return self.comment
