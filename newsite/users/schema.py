import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required, permission_required

from core.types import RelayModelMutation
from .models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains', ],
            'is_staff': ['exact'],
            'is_active': ['exact'],
            'date_joined': ['exact', 'icontains', 'year__gt', 'month__gt', 'day__gt']
        }
        interfaces = (graphene.relay.Node,)


class Query(object):
    me = graphene.relay.Node.Field(UserNode)
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    @login_required
    def resolve_me(self, info, **data):
        user_id = info.context.user.id
        user = graphene.Node.get_node_from_global_id(info, user_id, User)

        return user

    @login_required
    def resolve_user(self, info, **data):
        user_id = data.get('id')
        viewer_id = info.context.user.id
        user = graphene.Node.get_node_from_global_id(info, user_id, User)

        has_perm = info.context.user.has_perm('user.manage_user')
        if has_perm or (user.id == viewer_id):
            return user
        return None

    @login_required
    def resolve_users(self, info, **kwargs):
        user_id = info.context.user.id
        has_perm = info.context.user.has_perm('user.manage_user')
        if has_perm:
            return User.objects.all()
        return User.objects.filter(pk=user_id)