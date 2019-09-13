import graphene
import graphql_jwt

from users.schema import Query as UsersQuery
from news.schema import Query as NewsQuery
from news.schema import Mutation as NewsMutation
from feedbacks.schema import Query as FeedbacksQuery
from feedbacks.schema import Mutation as FeedbacksMutation

class Query(
    UsersQuery,
    NewsQuery,
    FeedbacksQuery,
    graphene.ObjectType):
    
    pass

class Mutation(
    NewsMutation,
    FeedbacksMutation,
    graphene.ObjectType):

    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()

    # Long running refresh tokens
    revoke_token = graphql_jwt.relay.Revoke.Field()

    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
