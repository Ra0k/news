import datetime

from django.db import models
from django.utils.translation import pgettext_lazy

from news.models import Article
from users.models import User


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateField('date liked', auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('article', 'user',)

    def __str__(self):
        return "%s %s" % (self.user.email, self.article.title)