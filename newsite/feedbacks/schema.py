import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required, permission_required, exceptions

from django.core.exceptions import ValidationError
from core.types import RelayModelMutation

from news.schema import ArticleNode
from .models import Like


class LikeNode(DjangoObjectType):
    class Meta:
        model = Like
        filter_fields = {
            'article__id': ['exact', 'icontains'],
            'user__id': ['exact', 'icontains'],
            'created_at': ['exact', 'icontains', 'year__gt', 'month__gt', 'day__gt']
        }
        interfaces = (graphene.relay.Node,)


class LikeInput(object):
    article = graphene.ID()


class LikeCreate(RelayModelMutation):
    like = graphene.Field(LikeNode)

    class Input(LikeInput):
        pass

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **data):
        data['user'] = info.context.user

        article_id = data.get('article')
        article = cls.get_node_or_error(
            info, article_id, 'article_id', only_type=ArticleNode
        )
        data['article'] = article
        print(data)
        like = cls.create_instance_by_input(Like, data)
        return LikeCreate(like=like)


class LikeDelete(RelayModelMutation):
    like = graphene.Field(LikeNode)

    class Input():
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **data):
        user_id = info.context.user.id
        like = cls.get_node_or_error(
            info, data['id'], 'like_id', only_type=LikeNode
        )

        has_perm = info.context.user.has_perm('feedbacks.manage_like')
        if has_perm or (like.user.id == user_id):
            like.delete()
            return LikeDelete(like=like)
        else:
            raise exceptions.PermissionDenied()

class Query(object):
    like = graphene.relay.Node.Field(LikeNode)
    likes = DjangoFilterConnectionField(LikeNode)


    @login_required
    def resolve_like(self, info, **data):
        like_id = data.get('id')
        user_id = info.context.user.id
        like = graphene.Node.get_node_from_global_id(info, like_id, Like)

        has_perm = info.context.user.has_perm('feedbacks.manage_like')
        if has_perm or (like.user.id == user_id):
            return like
        return None

    @login_required
    def resolve_likes(self, info, **kwargs):
        user_id = info.context.user.id
        has_perm = info.context.user.has_perm('feedbacks.manage_like')
        if has_perm:
            return Like.objects.all()
        return Like.objects.filter(user_id=user_id)


class Mutation(object):
    like = LikeCreate.Field()
    unlike = LikeDelete.Field()