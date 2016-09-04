from django.db import models

# Create your models here.

class Player(models.Model):
	nick=models.CharField(max_length=20)
	player_id=models.CharField(max_length=20)


class Game(models.Model):
	game_status=models.CharField()
	players = models.ManyToManyField(Player)
	admin_player=models.ForeignKey(Player)
	current_player=models.ForeignKey(Player)
	turn_seq=models.CharField()
	words_done=models.CharField()
	scores=models.CharField()







