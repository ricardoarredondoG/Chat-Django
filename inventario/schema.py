import graphene
from graphene_django import DjangoObjectType
from .models import *
import graphene
import channels_graphql_ws

class MedicamentoType(DjangoObjectType):
    class Meta:
        model = Medicamento

class PresentacionType(DjangoObjectType):
    class Meta:
        model = Presentacion

class PrincipioActivoType(DjangoObjectType):
    class Meta:
        model = PrincipioActivo

class StockType(DjangoObjectType):
    class Meta:
        model = Stock

class ViaAdministracion(DjangoObjectType):
    class Meta:
        model = ViaAdministracion

class DeletePrincipioActivo(graphene.Mutation):
    ok = graphene.Boolean()
    class Arguments:
        id = graphene.ID()
    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = PrincipioActivo.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class AddPrincipioActivo(graphene.Mutation):
    principioActivo = graphene.Field(PrincipioActivoType)
    class Arguments:
        nombre = graphene.String()
        alertaStockBajo = graphene.Int()
        grupo = graphene.String()

    @classmethod   
    def mutate(cls, root, info, **kwargs):  
        obj = PrincipioActivo.objects.create(nombre=kwargs["nombre"], alertaStockBajo=kwargs["alertaStockBajo"])
        MySubscription.broadcast(payload=obj, group=kwargs["grupo"])
        return cls(obj)



#Mutaciones
class Mutation(graphene.ObjectType):
    delete_PrincipioActivo = DeletePrincipioActivo.Field()
    add_PrincipioActivo = AddPrincipioActivo.Field()



#Query
class Query(graphene.ObjectType):
    medicamento = graphene.List(MedicamentoType)
    principioActivo = graphene.List(PrincipioActivoType)

    def resolve_medicamento(self, info, **kwargs):
        return Medicamento.objects.all()
    def resolve_principioActivo(self, info, **kwargs):
        return PrincipioActivo.objects.all()



#Sucriptions
class MySubscription(channels_graphql_ws.Subscription):
    # Subscription payload.
    event = graphene.Field(PrincipioActivoType)
    
    class Arguments:
        chatroom = graphene.String()

    def subscribe(cls, info, chatroom=None):
        return [chatroom] if chatroom is not None else None

    def publish(self, info, chatroom=None):
        return MySubscription(event=self)

    
        
class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    my_subscription = MySubscription.Field()


schema = graphene.Schema(query=Query,  mutation=Mutation,  subscription=Subscription,)


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""
    schema = schema

    # Uncomment to send keepalive message every 42 seconds.
    # send_keepalive_every = 42

    # Uncomment to process requests sequentially (useful for tests).
    # strict_ordering = True

    async def on_connect(self, payload):
        """New client connection handler."""
        # You can `raise` from here to reject the connection.
        print("New client connected!")
    