from .models import Game, Player
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
	
	#serializing the relations
	admin_player = serializers.StringRelatedField()
	current_player = serializers.StringRelatedField()
	players = serializers.StringRelatedField(many=True)
	
	class Meta:
		model = Game
		fields = '__all__'



class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'
