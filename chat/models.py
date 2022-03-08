from django.db import models
from django import forms

#Modelos

class User(models.Model):
    nickname = models.CharField(max_length=100)

class Sala(models.Model):
    nombre_sala = models.CharField(max_length=100)

class Message(models.Model):
    content = models.TextField()
    fecha_hora = models.DateTimeField()
    sala = models.ForeignKey(Sala, models.DO_NOTHING, db_column='sala', blank=True, null=True)
    usuario_envia = models.ForeignKey(User, models.DO_NOTHING, db_column='user', blank=True, null=True)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields= ['content', 'fecha_hora', 'sala', 'usuario_envia']

