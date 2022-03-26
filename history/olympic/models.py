from django.db import models
from uuid import uuid4

# Create your models here.
class Person(models.Model):
    id_person   = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    age         = models.IntegerField()
    height      = models.IntegerField()
    weight      = models.IntegerField()
    team        = models.UUIDField()
    nationality = models.UUIDField()


class Team(models.Model):
    id_team = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name    = models.CharField(max_length=255)

class Nationality(models.Model):
    id_nationality = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name           = models.CharField(max_length=3)

class Game(models.Model):
    id_game = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name    = models.CharField(max_length=255)
    year    = models.UUIDField()
     
class Year(models.Model):
    id_year = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    year    = models.IntegerField()

class ParticipationGame(models.Model):
    id_game   = models.UUIDField()
    id_person = models.UUIDField()