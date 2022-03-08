from typing_extensions import Required
import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from .models import *
import channels_graphql_ws

#Type
class MessageType(DjangoObjectType):
    class Meta:
        model = Message

class UserType(DjangoObjectType):
    class Meta:
        model = User

#<--------------------------------- Query --------------------------------->

class Query(graphene.ObjectType):
    all_messages = graphene.List(MessageType)
    all_messages_by_sala = graphene.List(MessageType,  salaId=graphene.Int(required= True))
    all_user = graphene.List(UserType)

    def resolve_all_messages(self, info, **kwargs):
        return Message.objects.all()

    def resolve_all_messages_by_sala(self, info, salaId):
        sala = Sala.objects.get(id = salaId )
        return Message.objects.filter(sala = sala)
    
    def resolve_all_user(self, info):
        return User.objects.all()

#<--------------------------------- Mutation --------------------------------->

#Enviar Mensaje
class MessageInput(graphene.InputObjectType):
    content = graphene.String()
    fecha_hora = graphene.DateTime()
    sala = graphene.Int()
    usuario_envia = graphene.Int()

class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        message_data = MessageInput(required=True)

    @classmethod   
    def mutate(cls, root, info, message_data):
        sala = Sala.objects.get(id = message_data.sala )
        usuario_envia = User.objects.get(id = message_data.usuario_envia)
        obj = Message.objects.create(content=message_data.content, fecha_hora=message_data.fecha_hora, sala=sala, usuario_envia=usuario_envia)
        RecibeMessage.broadcast(payload=obj, group=str(message_data.sala))
        return cls(obj)


class Mutation(graphene.ObjectType):
    #Mutacion Enviar Mensaje
    send_message = SendMessage.Field()

#<--------------------------------- Suscription --------------------------------->


class RecibeMessage(channels_graphql_ws.Subscription):
    
    messagereceived = graphene.Field(MessageType)
    
    class Arguments:
        chatroom = graphene.String()

    def subscribe(cls, info, chatroom=None):
        return [chatroom] if chatroom is not None else None

    def publish(self, info, chatroom=None):
        return RecibeMessage(messagereceived=self)


class Subscription(graphene.ObjectType):
    recibe_message = RecibeMessage.Field()


#Schema
schema = graphene.Schema(query=Query,  mutation=Mutation,  subscription=Subscription,)

class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema
