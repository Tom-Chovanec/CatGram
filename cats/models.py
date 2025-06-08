from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CatImage(models.Model):
    image = models.ImageField(upload_to='cats/')
    title = models.CharField(max_length=100, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_cats', blank=True)
    favorites = models.ManyToManyField(
        User, related_name='favorited_cats', blank=True)

    def __str__(self):
        return self.title if self.title else f'Cat Image {self.id}'

    def like_count(self):
        return self.likes.count()

    def liked(self, user):
        return user in self.likes.all()
