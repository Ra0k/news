import datetime

from django.db import models
from django.utils.translation import pgettext_lazy

from users.models import User
#from feedbacks.models import Like


class Site(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=15)
    description = models.CharField(max_length=5000)
    lang = models.CharField(max_length=10)

    url = models.CharField(unique=True, max_length=200)

    published = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ['name']
        permissions = (
            (
                'select_site', pgettext_lazy(
                    'Permission description', 'Select site.')),
            (
                'manage_site', pgettext_lazy(
                    'Permission description', 'Manage site.'))
        )

    def __str__(self):
        return self.name

class Feed(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=15)
    description = models.CharField(max_length=5000)
    lang = models.CharField(max_length=10)

    url = models.CharField(unique=True, max_length=200)

    published = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ['name']
        permissions = (
            (
                'select_feed', pgettext_lazy(
                    'Permission description', 'Select feed.')),
            (
                'manage_feed', pgettext_lazy(
                    'Permission description', 'Manage feed.'))
        )

    def __str__(self):
        return "%s %s" % (self.site.name, self.name)

class Article(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    picture_url = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=5000)
    authors = models.CharField(max_length=100, blank=True)
    url = models.CharField(unique=True, max_length=200)

    pub_date = models.DateTimeField('date published', auto_now_add=True, blank=True)
    reg_date = models.DateTimeField('date registered', auto_now_add=True, blank=True)

    published = models.BooleanField(default=True)

    likes = models.ManyToManyField(
        User, 
        through='feedbacks.Like',
        through_fields=('article', 'user'),
        related_name='liked_articles'
    )

    class Meta:
        ordering = ['-reg_date', '-pub_date']
        permissions = (
            (
                'select_article', pgettext_lazy(
                    'Permission description', 'Select article.')),
            (
                'manage_article', pgettext_lazy(
                    'Permission description', 'Manage article.'))
        )

    def __str__(self):
        return "%s %s %s" % (
            self.feed.site.name, 
            self.feed.name, 
            self.title
        )