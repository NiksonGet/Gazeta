from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='imgs/', default='image')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

from simple_history.models import HistoricalRecords

class Post(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    content = models.TextField()
    time_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='imgs/')
    tags = models.ManyToManyField(Tag)

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    content = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content



