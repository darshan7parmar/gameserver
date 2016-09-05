from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Player(models.Model):
	nick=models.CharField(max_length=20)
	player_id=models.CharField(max_length=20)


class Game(models.Model):
	STATUS = (
    ('w', 'Waiting to start'),
    ('s', 'Started'),
    ('f', 'Finished'),)
	game_status=models.CharField(max_length=1,choices=STATUS)
	players = models.ManyToManyField(Player,related_name='players')
	admin_player=models.ForeignKey(Player,related_name='admin_player')
	current_player=models.ForeignKey(Player,related_name='current_player')
	#to decide
	turn_seq=models.CharField(max_length=20)
	words_done=ArrayField(models.CharField(max_length=20))
	scores=JSONField()
	board=ArrayField(ArrayField(models.CharField(max_length=1)))












