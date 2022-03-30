from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField

from olympic import models

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Person
        fields = '__all__' 

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Team
        fields = '__all__' 

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Nationality
        fields = '__all__' 

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Game
        fields = '__all__' 

class ParticipationGameSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.ParticipationGame
        fields = '__all__'

class UploadFileSerializer(Serializer):
    csvFile = FileField(max_length=None, allow_empty_file=False)

    class Meta:
        fields = ['csvFile']
