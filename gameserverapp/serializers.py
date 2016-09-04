from .models import Game, Player
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'
		# fields = ('players', 'admin_player', 'game_status', 'current_player',
		# 'turn_seq','words_done','scores')



class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'
		# fields = ('players', 'admin_player', 'game_status', 'current_player',
		# 'turn_seq','words_done','scores')
