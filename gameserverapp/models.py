from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Player(models.Model):
	nick=models.CharField(max_length=20,blank=True)
	def __str__(self):              # __unicode__ on Python 2
		return str(self.nick)

class Board(models.Model):
	grid=ArrayField(ArrayField(models.CharField(max_length=1)),null=True)
	board_rows=models.IntegerField(default=15)
	board_cols=models.IntegerField(default=15)
	num_words=models.IntegerField(default=10)
	words_list=ArrayField(models.CharField(max_length=50))

class Game(models.Model):
	STATUS = (
    ('w', 'Waiting for start'),
    ('s', 'Started'),
    ('f', 'Finished'),)
	game_status=models.CharField(max_length=1,choices=STATUS)
	players = models.ManyToManyField(Player,related_name='player')
	admin_player=models.ForeignKey(Player,related_name='admin_player')
	turn_sequence=ArrayField(models.CharField(max_length=50))
	current_player=models.ForeignKey(Player,related_name='current_player',null=True)
	words_done=ArrayField(models.CharField(max_length=50))
	scores=JSONField()
	board=models.ForeignKey(Board,related_name="board",null=True)
	min_players=models.IntegerField()
	max_players=models.IntegerField()
	pass_count=models.IntegerField()
	def __str__(self):              # __unicode__ on Python 2
		return str(self.id)
	








