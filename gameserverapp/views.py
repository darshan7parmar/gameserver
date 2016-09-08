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
from django.conf import settings
# Create your views here.


@api_view(['POST'])
@parser_classes((JSONParser,))
def create(request):
	#Only Post Requests are allowed
	data=request.data
	nick=data.get('nick')
	player_id=data.get('player_id')
	
	if player_id is not None:
		player=check_if_player_exists(player_id)
		
		if not player:
			content = {'detail': 'Player does not exist'}
			return Response(content,status=status.HTTP_404_NOT_FOUND)	
	
	else:
		player=create_player(nick)
	
	game=Game.objects.create(game_status='w',scores="{}",admin_player=player,words_done=[""],
		board=[['a'],['b']],turn_seq="xyz",min_players=2,max_players=5,pass_count=0)
	game.players.add(player)
	content = {'game_id':game.id,'player_id':player.id,'nick':player.nick}
	return Response(content,status=status.HTTP_201_CREATED)


def create_player(nick):
	if nick is None or nick.strip()== "":
		player=Player.objects.create()
		player.nick="player"+str(player.id)
		player.save()
	else:
		player=Player.objects.create(nick=str(nick))
	return player



@api_view(['POST'])
@parser_classes((JSONParser,))
def join(request):
	data = request.data
	game_id = data.get('game_id')
	nick = data.get('nick')
	player_id=data.get('player_id')

	game = check_if_game_exists(game_id)
	if not game:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)
	
	if player_id is not None:
		player=check_if_player_exists(player_id)
		
		if not player:
			content = {'detail': 'Player does not exist'}
			return Response(content,status=status.HTTP_404_NOT_FOUND)	
	else:
		player=create_player(nick)
	
	# if player has already joined game
	if  game.players.all().filter(id=player.id).exists():
		content = {'detail': 'You have already joined the game'}
		return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE)
	
	game.players.add(player)
	content={'player_id':player.id}
	return Response(content,status=status.HTTP_201_CREATED)


def check_if_game_exists(game_id):
	if game_id is not None:
		try:
			game=Game.objects.get(id=int(game_id))
		except Game.DoesNotExist:
			return None
		except ValueError:
			return None
	else:
		return None
	return game

def check_if_player_exists(player_id):
	if player_id is not None:
		try:
			player=Player.objects.get(id=int(player_id))
		except Player.DoesNotExist:
			return None
		except ValueError:
			return None	
	else:
		return None
	return player


@api_view(['POST'])
@parser_classes((JSONParser,))
def info(request):
	data=request.data
	game_id=data.get('game_id')
	player_id=data.get('player_id')

	game = check_if_game_exists(game_id)
	
	if not game:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	player= check_if_player_exists(player_id)
	if not player:
		content = {'detail': 'Player does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)		
	
	if not game.players.all().filter(id=player.id).exists():
		content = {'detail': 'Player not authorized'}
		return Response(content,status=status.HTTP_401_UNAUTHORIZED)

	gamedata=GameSerializer(game)
	return Response(gamedata.data,status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes((JSONParser,))
def start():
	data=request.data
	game_id=data.get('game_id')
	player_id=data.get('player_id')

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


def play(request):
	data=request.data
	player_id=data.get('player_id')
	game_id=data.get('game_id')
	word=data.get('word')
	start_loc=data.get('start-loc')
	direction=data.get('direction')

	try:
		game=Game.objects.get(id=game_id)
	except Game.DoesNotExist:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	try:
		player=Player.objects.get(id=player_id)
	except Game.DoesNotExist:
		content = {'detail': 'Player does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	#if word is empty
	if not word:
		game.pass_count+=1
	else:
		pass
#ending game by changing it's status
def endgame(game):
	game.game_status="f"
	game.save()			


# game_status=models.CharField(max_length=1,choices=STATUS)
# 	players = models.ManyToManyField(Player,related_name='players')
# 	admin_player=models.ForeignKey(Player,related_name='admin_player')
# 	current_player=models.ForeignKey(Player,related_name='current_player')
# 	#to decide
# 	turn_seq=models.CharField(max_length=20)
# 	words_done=ArrayField(models.CharField(max_length=20))
# 	scores=JSONField()
# 	board=ArrayField(ArrayField(models.CharField(max_length=1)))
