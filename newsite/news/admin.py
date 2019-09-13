from django.contrib import admin


from news.models import Site, Feed, Article

admin.site.register(Site)
admin.site.register(Feed)
admin.site.register(Article)