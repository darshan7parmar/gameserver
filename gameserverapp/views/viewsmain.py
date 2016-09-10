from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from gameserverapp.models import *
from gameserverapp.serializers import *
from gameserver import settings
import random
import re
from .utils import *


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
	
	#Create Board
	grid = initialize_grid(settings.board_rows,settings.board_cols)
	words_list=get_random_words(settings.num_words)
	generate_grid(grid,words_list)
	board = Board.objects.create(grid=grid,board_rows=settings.board_rows,
	board_cols=settings.board_cols,words_list=words_list)
	
	#Create Game
	turn_seq=[]
	turn_seq.append(player.nick)
	scores=dict()
	scores[player.nick]=0
	words_done=[]
	game = Game.objects.create(board=board,game_status='w',scores=scores,admin_player=player,
		current_player=player,words_done=words_done,
		turn_sequence=turn_seq,min_players=settings.min_players,
		max_players=settings.max_players,pass_count=0)
	
	
	game.players.add(player)
	content = {'game_id':game.id,'player_id':player.id,'nick':player.nick}
	return Response(content,status=status.HTTP_201_CREATED)




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
		maxlimitbool=check_if_max_limit_reached(game)
		if maxlimitbool:
			content = {'detail': 'Maximum Player Already Joined'}
			return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE)	 
		
		player=create_player(nick)	
	# if player has already joined game
	if  game.players.all().filter(id=player.id).exists():
		content = {'detail': 'You have already joined the game'}
		return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE)
	
	game.players.add(player)
	game.turn_sequence.append(player.nick)
	scores=game.scores
	scores[player.nick]=0
	game.scores=scores
	game.save()
	content={'player_id':player.id}
	return Response(content,status=status.HTTP_201_CREATED)




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
	boardata=BoardSerializer(game.board)
	return Response({"game":gamedata.data,"board":boardata.data},status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes((JSONParser,))
def start(request):
	data=request.data
	game_id=data.get('game_id')
	player_id=data.get('player_id')

	# Check if Game exists
	game = check_if_game_exists(game_id)
	
	if not game:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	#Check if Player Exists
	player=check_if_player_exists(player_id)
	
	if not player:
		content = {'detail': 'Player does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	#Check if Player is admin
	if not game.admin_player.id == int(player_id):
		content={'detail':'You are not authorized to start this game'}
		return Response(content,status=status.HTTP_401_UNAUTHORIZED)

	#start the game by changing status and 
	num_players=game.players.all().count()
	if num_players < game.min_players :
		content={'detail': 'Please wait for more players to join'}
		return Response(content,status=status.HTTP_417_EXPECTATION_FAILED)
	
	# if game is not in waiting state

	if game.game_status != "w":
		content={'detail': 'Game Already Started or Finished'}
		return Response(content,status=status.HTTP_417_EXPECTATION_FAILED)	

	game.game_status="s"
	game.save()	
	content=GameSerializer(game)

	return Response(content.data,status=status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes((JSONParser,))
def play(request):
	data=request.data
	player_id=data.get('player_id')
	game_id=data.get('game_id')
	word=data.get('word')
	word=str(word)
	start_loc=data.get('start_loc')
	direction=data.get('direction')
	
	game = check_if_game_exists(game_id)
	
	if not game:
		content = {'detail': 'Game does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	#Check if Player Exists
	player=check_if_player_exists(player_id)

	if not player:
		content = {'detail': 'Player does not exist'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)	

	if not game.players.all().filter(id=player.id).exists():
		content = {'detail': 'Player not authorized'}
		return Response(content,status=status.HTTP_401_UNAUTHORIZED)
	
	if not game.game_status == 's':
		content = {'detail': 'Game not started or finished'}
		return Response(content,status=status.HTTP_401_UNAUTHORIZED)

	if not game.current_player.id == player.id:
		content = {'detail': 'It is not your turn to play'}
		return Response(content,status=status.HTTP_401_UNAUTHORIZED)

	if word is None or word.strip()== "":
		content = {'detail': 'Word can not be blank or None'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	if direction is None or (direction != "RIGHT" and direction != "DOWN"):
		content = {'detail': 'Direction can be right or down'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)

	if start_loc is None or len(start_loc) !=2:
		content = {'detail': 'start location must be provided or contain two values only.'}
		return Response(content,status=status.HTTP_404_NOT_FOUND)


	#Change turn 
	game.pass_count=0
	change_turn_sequence(game)
	# Check if word already identified
	if  word in game.words_done :
		content = {'detail': 'Word already identified'}
		return Response(content,status=status.HTTP_100_CONTINUE)

	if not word in game.board.words_list:
		content = {'detail': 'No such word in dictionary'}
		return Response(content,status=status.HTTP_100_CONTINUE)

	# Find word match
	match=find_word(game,word,start_loc,direction)
	if not match:
		return Response({"detail":"word does not match"},status=status.HTTP_100_CONTINUE)
		
	scores=game.scores
	scores[player.nick]=scores[player.nick]+1
	game.scores=scores
	game.words_done.append(word)

	#end game 
	if len(game.words_done) == game.board.num_words:
		game.game_status="f"
	
	game.save()	
	return Response({"detail":"success"},status=status.HTTP_201_CREATED)



def find_word(game,word,start_loc,direction):
	if direction == "DOWN":
		return find_word_vertical_down(game,word,start_loc)
	elif direction == "RIGHT":
		return find_word_vertical_right(game,word,start_loc)


def find_word_vertical_down(game,word,start_loc):
	grid=game.board.grid
	i=int(start_loc[0])
	j=int(start_loc[1])
	match=False
	for k in range(0,len(word)):
		if (k+i) >= len(grid):
			break
		
		if k == len(word)-1:
			if grid[k+i][j] == word[k]:
				match=True
				break
		else:
			if not grid[k+i][j] == word[k]:
				break
	return match

def find_word_vertical_right(game,word,start_loc):
	grid=game.board.grid
	i=int(start_loc[0])
	j=int(start_loc[1])
	match=False
	for k in range(0,len(word)):
		if (k+j) >= len(grid):
			break
		
		if k == len(word)-1:
			if grid[i][k+j] == word[k]:
				match=True
				break
		else:
			if not grid[i][k+j] == word[k]:
				break
	return match


def change_turn_sequence(game):
	turn_seq=game.turn_sequence
	turn_seq = turn_seq[1:]
	turn_seq.append(game.current_player.nick)
	game.turn_sequence=turn_seq
	game.current_player=game.players.all().filter(nick=turn_seq[0])[0]
	game.save()


@api_view(['POST'])
@parser_classes((JSONParser,))
def passturn(request):
	data=request.data
	player_id=data.get('player_id')
	game_id=data.get('game_id')

