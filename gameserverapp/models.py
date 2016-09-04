from django.db import models

# Create your models here.

class Player(models.Model):
	nick=models.CharField(max_length=20)
	player_id=models.CharField(max_length=20)


class Game(models.Model):
	game_status=models.CharField(max_length=20)
	players = models.ManyToManyField(Player,related_name='players')
	admin_player=models.ForeignKey(Player,related_name='admin_player')
	current_player=models.ForeignKey(Player,related_name='current_player')
	turn_seq=models.CharField(max_length=20)
	words_done=models.CharField(max_length=20)
	scores=models.CharField(max_length=20)







