from pickle import NONE
from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Person(models.Model):
    id_person   = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    name        = models.CharField(max_length=255)
    height      = models.IntegerField()
    weight      = models.IntegerField()
    team        = models.ForeignKey(to="Team", on_delete=models.DO_NOTHING)
    nationality = models.ForeignKey(to="Nationality", on_delete=models.DO_NOTHING)

class Team(models.Model):
    id_team   = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    team      = models.CharField(max_length=255)

class Nationality(models.Model):
    id_nationality = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    nation         = models.CharField(max_length=255)

class Game(models.Model):
    id_game   = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    game      = models.CharField(max_length=255)
    year      = models.IntegerField()
    class Season(models.TextChoices):
        WINTER = 'WT', _('Winter')
        SUMMER = 'SM', _('Summer')

    season = models.CharField(
        max_length=2,
        choices=Season.choices,
        default=Season.SUMMER
    )
   
class ParticipationGame(models.Model):
    id_participation = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    person           = models.ForeignKey(to="Person", on_delete=models.DO_NOTHING)
    game             = models.ForeignKey(to="Game", on_delete=models.DO_NOTHING)
    events           = models.ForeignKey(to="Event", on_delete=models.DO_NOTHING)
    class Medal(models.TextChoices):
        NONE   = 'NA', _('N/A')
        BRONZE = 'BZ', _('Bronze')
        SILVER = 'SV', _('Silver')
        GOLD   = 'GD', _('Gold')

    medal = models.CharField(
        max_length=2,
        choices=Medal.choices,
        default=Medal.NONE,
    )

class Sport(models.Model):
    id_sport  = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    sport     = models.CharField(max_length=255)

class Event(models.Model):
    id_event  = models.AutoField(verbose_name='ID',primary_key = True, serialize=False, auto_created=True)
    event     = models.CharField(max_length=255)