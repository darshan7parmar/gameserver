from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
# Create your views here.


@api_view(['POST'])
@parser_classes((JSONParser,))
def create(request):
	#Only Post Requests are allowed
	data=request.data
	nick=data['nick']
	player=Player.objects.create(nick=nick,player_id='xyz')
	game=Game.objects.create(game_status='w',scores="{}",admin_player=player,words_done=[""],board=[['a'],['b']],turn_seq="xyz")
	game.players.add(player)
	content = {'game_id':game.id,'player_id':player.id,'nick':player.nick}
	return Response(content,status=status.HTTP_201_CREATED)



@api_view(['POST'])
@parser_classes((JSONParser,))
def join(request):
	data=request.data
	game_id=data['game_id']
	nick=data['nick']

	# Check if Game exists
	try:
		game=Game.objects.get(id=game_id)
	except Game.DoesNotExist:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	player=Player.objects.create(nick=nick,player_id="xyz")	
	game.players.add(player)
	content={'player_id':player.id}
	return Response(content,status=status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes((JSONParser,))
def info(request):
	data=request.data
	game_id=data['game_id']
	#player_id=data['player_id']

	# Check if Game exists
	try:
		game=Game.objects.get(id=game_id)
	except Game.DoesNotExist:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	gamedata=GameSerializer(game)
	return Response(gamedata.data,status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes((JSONParser,))
def start():
	data=request.data
	game_id=data['game_id']
	player_id=data['player_id']

	# Check if Game exists
	try:
		game=Game.objects.get(id=game_id)
	except Game.DoesNotExist:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	#Check if Player is admin
	if not str(game.admin_player.id) == game_id:
		content={'detail':'You are not authorized to start this game'}
		return Response(content,status=status.HTTP_401_UNAUTHORIZED)

	#start the game by changing status and 
	num_players=count(game.players)
	if num_players < game.min_players :
		content={'detail': 'Please wait for more players to join'}
		return Response(content,status=status.HTTP_417_EXPECTATION_FAILED)
	
	game.game_status="s"
	game.save()	
	content=GameSerializer(game)
	return Response(content,status=status.HTTP_201_CREATED)




# game_status=models.CharField(max_length=1,choices=STATUS)
# 	players = models.ManyToManyField(Player,related_name='players')
# 	admin_player=models.ForeignKey(Player,related_name='admin_player')
# 	current_player=models.ForeignKey(Player,related_name='current_player')
# 	#to decide
# 	turn_seq=models.CharField(max_length=20)
# 	words_done=ArrayField(models.CharField(max_length=20))
# 	scores=JSONField()
# 	board=ArrayField(ArrayField(models.CharField(max_length=1)))
