import graphene

from graphql.error import GraphQLError
from django.core.exceptions import ValidationError

class RelayModelMutation(graphene.relay.ClientIDMutation):
    class Meta:
        abstract = True

    @classmethod
    def clean_input(cls, input):
        return input

    @classmethod
    def clean_instance(cls, instance):
        return instance

    @classmethod
    def update_instance_by_input(cls, instance, input):
        input = cls.clean_input(input)

        model = type(instance)
        for field in model._meta.fields:
            if field.name in input.keys():
                setattr(instance, field.name, input.get(field.name))

        for field in model._meta.many_to_many:
            if field.name in input.keys():
                many = getattr(instance, field.name)
                many.set(input.get(field.name))

        instance = cls.clean_instance(instance)
        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    def create_instance_by_input(cls, model, input):
        input = cls.clean_input(input)

        arguments = {}
        for field in model._meta.fields:
            if field.name in input.keys():
                arguments[field.name] = input.get(field.name)

        instance = model(**arguments)
        instance = cls.clean_instance(instance)
        instance.full_clean()
        instance.save()

        for field in model._meta.many_to_many:
            if field.name in input.keys():
                many = getattr(instance, field.name)
                many.set(input.get(field.name))

        return instance

    @classmethod
    def get_node_or_error(cls, info, node_id, field="id", only_type=None):
        if not node_id:
            return None

        try:
            node = graphene.Node.get_node_from_global_id(info, node_id, only_type)
        except (AssertionError, GraphQLError) as e:
            raise ValidationError({field: str(e)})
        else:
            if node is None:
                raise ValidationError(
                    {field: "Couldn't resolve to a node: %s" % node_id}
                )
        return node