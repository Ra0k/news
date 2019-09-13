import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required, permission_required

from news.models import Site, Feed, Article
from core.types import RelayModelMutation


class SiteNode(DjangoObjectType):
    class Meta:
        model = Site
        filter_fields = {
            'name': ['exact', 'icontains'],
            'short_name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'lang': ['exact'],
            'url': ['exact', 'icontains']
        }
        interfaces = (graphene.relay.Node,)


class FeedNode(DjangoObjectType):
    class Meta:
        model = Feed
        filter_fields = {
            'site': ['exact'],
            'site__name': ['exact', 'icontains'],
            'site__short_name': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'short_name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'lang': ['exact']
        }
        interfaces = (graphene.relay.Node,)


class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article
        filter_fields = {
            'feed__site': ['exact'],
            'feed__site__name': ['exact', 'icontains'],
            'feed__site__short_name': ['exact', 'icontains'],
            'feed': ['exact'],
            'feed__name': ['exact', 'icontains'],
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'authors': ['exact', 'icontains'],
            'url': ['exact', 'icontains'],
            'pub_date': ['exact', 'year__gt', 'month__gt', 'day__gt'],
            'reg_date': ['exact', 'year__gt', 'month__gt', 'day__gt']
        }
        interfaces = (graphene.relay.Node,)


class SiteInput(object):
    name = graphene.String()
    short_name = graphene.String()
    description = graphene.String()
    lang = graphene.String()
    url = graphene.String()
    published = graphene.Boolean()
    active = graphene.Boolean()


class SiteCreate(RelayModelMutation):
    site = graphene.Field(SiteNode)

    class Input(SiteInput):
        pass

    @classmethod
    @permission_required('news.manage_site')
    def mutate_and_get_payload(cls, root, info, **data):
        site = cls.create_instance_by_input(Site, data)
        return SiteCreate(site=site)


class SiteUpdate(RelayModelMutation):
    site = graphene.Field(SiteNode)

    class Input(SiteInput):
        id = graphene.ID()

    @classmethod
    @permission_required('news.manage_site')
    def mutate_and_get_payload(cls, root, info, **data):
        site_id = data.pop('id')
        site = Site.objects.get(pk=from_global_id(site_id)[1])
        site = cls.update_instance_by_input(site, data)
        return SiteUpdate(site=site)


class FeedInput(object):
    site = graphene.ID()
    name = graphene.String()
    short_name = graphene.String()
    description = graphene.String()
    lang = graphene.String()
    url = graphene.String()
    published = graphene.Boolean()
    actice = graphene.Boolean()


class FeedCreate(RelayModelMutation):
    feed = graphene.Field(FeedNode)

    class Input(FeedInput):
        id = graphene.ID()

    @classmethod
    @permission_required('news.manage_feed')
    def mutate_and_get_payload(cls, root, info, **data):
        site_id = data.get('site')
        site = cls.get_node_or_error(
            info, site_id, field="site_id", only_type=SiteNode
        )
        data['site'] = site

        feed = cls.create_instance_by_input(Feed, data)
        return FeedCreate(feed=feed)


class FeedUpdate(RelayModelMutation):
    feed = graphene.Field(FeedNode)

    class Input(FeedInput):
        id = graphene.ID()

    @classmethod
    @permission_required('news.manage_feed')
    def mutate_and_get_payload(cls, root, info, **data):
        feed_id = data.pop('id')
        feed = Feed.objects.get(pk=from_global_id(feed_id)[1])
        feed = cls.update_instance_by_input(feed, data)
        return FeedUpdate(feed=feed)


class ArticleInput(object):
    feed = graphene.ID()
    title = graphene.String()
    picture_url = graphene.String()
    description = graphene.String()
    authors = graphene.String()
    url = graphene.String()
    pub_date = graphene.Boolean()
    reg_date = graphene.Boolean()
    published = graphene.Boolean()


class ArticleCreate(RelayModelMutation):
    article = graphene.Field(ArticleNode)

    class Input(ArticleInput):
        id = graphene.ID()

    @classmethod
    #@permission_required('news.manage_article')
    def mutate_and_get_payload(cls, root, info, **data):
        feed_id = data.get('feed')
        feed = cls.get_node_or_error(
            info, feed_id, field="feed_id", only_type=FeedNode
        )
        data['feed'] = feed
        print(feed)
        article = cls.create_instance_by_input(Article, data)
        return ArticleCreate(article=article)


class ArticleUpdate(RelayModelMutation):
    article = graphene.Field(ArticleNode)

    class Input(ArticleInput):
        id = graphene.ID()

    @classmethod
    @permission_required('news.manage_article')
    def mutate_and_get_payload(cls, root, info, **data):
        article_id = data.pop('id')
        article = Article.objects.get(pk=from_global_id(article_id)[1])
        article = cls.update_instance_by_input(article, data)
        return ArticleUpdate(article=article)


class Query(object):
    site = graphene.relay.Node.Field(SiteNode)
    all_sites = DjangoFilterConnectionField(SiteNode)

    feed = graphene.relay.Node.Field(FeedNode)
    all_feeds = DjangoFilterConnectionField(FeedNode)

    article = graphene.relay.Node.Field(ArticleNode)
    all_articles = DjangoFilterConnectionField(ArticleNode)

    def resolve_site(self, info, **data):
        site_id = data.get('id')
        site = graphene.Node.get_node_from_global_id(info, site_id, Site)

        has_perm = info.context.user.has_perm('news.manage_site')
        if site.published or has_perm:
            return site
        return None

    def resolve_all_sites(self, info, **kwargs):
        has_perm = info.context.user.has_perm('news.manage_site')
        if has_perm:
            return Site.objects.all()
        return Site.objects.filter(published=True)

    def resolve_feed(self, info, **data):
        feed_id = data.get('id')
        feed = graphene.Node.get_node_from_global_id(info, feed_id, Feed)

        site = feed.site
        published = feed.published and site.published
        has_perm = info.context.user.has_perm('news.manage_feed')
        if published or has_perm:
            return feed
        return None

    def resolve_all_feeds(self, info, **kwargs):
        has_perm = info.context.user.has_perm('news.manage_feed')
        if has_perm:
            return Feed.objects.all()
        
        return Feed.objects.filter(
            published=True, 
            site__published=True
        )

    def resolve_article(self, info, **data):
        article_id = data.get('id')
        article = graphene.Node.get_node_from_global_id(info, article_id, Article)

        feed = article.feed
        site = feed.site
        published = article.published and feed.published and site.published
        has_perm = info.context.user.has_perm('news.manage_article')
        if published or has_perm:
            return article
        return None

    def resolve_all_articles(self, info, **kwargs):
        has_perm = info.context.user.has_perm('news.manage_article')
        if has_perm:
            return Article.objects.all()
        
        return Article.objects.filter(
            published=True, 
            feed__published=True, 
            feed__site__published=True
        )


class Mutation(object):
    create_site = SiteCreate.Field()
    update_site = SiteUpdate.Field()

    create_article = ArticleCreate.Field()
    update_article = ArticleUpdate.Field()