from gameserverapp.models import *
from gameserverapp.serializers import *
from gameserver import settings
from rest_framework import status
import random
import re
import string
from .utils import *

def join_validation(game_id,player_id):

	""" 
	Validiation for Game Join 
	"""

	isValid=False
	game=None
	player=None
	content=None
	httpstatus=None
	game = check_if_game_exists(game_id)
	player=check_if_player_exists(player_id)

	if not game:
		content = {'detail': 'Game does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND	
	
	elif player_id is not None and  not player:
		content = {'detail': 'Player does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND
			
	elif player_id is not None and game.players.all().filter(id=player.id).exists():
		content = {'detail': 'You have already joined the game'}
		httpstatus=status.HTTP_406_NOT_ACCEPTABLE

	elif check_if_max_limit_reached(game):
		content = {'detail': 'Maximum Player Already Joined'}
		httpstatus=status.HTTP_406_NOT_ACCEPTABLE	 

	else:
		isValid=True
		if player_id is None:	
			player=create_player(game)	

	return return_dictionary(isValid,game,player,content,httpstatus)



def info_validation(game_id,player_id):

	""" 
	Validiation for Game Info 
	"""


	isValid=False
	game=None
	player=None
	content=None
	httpstatus=None

	game = check_if_game_exists(game_id)
	player= check_if_player_exists(player_id)

	if not game:
		content = {'detail': 'Game does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND
	
	if not player:
		content = {'detail': 'Player does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND	
	
	elif not game.players.all().filter(id=player.id).exists():
		content = {'detail': 'Player not authorized'}
		httpstatus=status.HTTP_401_UNAUTHORIZED
	
	else:
		isValid=True	

	return return_dictionary(isValid,game,player,content,httpstatus)


def start_validation(game_id,player_id):

	""" 
	Validiation for Game Start 
	"""


	isValid=False
	game=None
	player=None
	content=None
	httpstatus=None


	# Check if Game exists
	game = check_if_game_exists(game_id)
	player=check_if_player_exists(player_id)
	
	if not game:
		content = {'detail': 'Game does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND

	elif not player:
		content = {'detail': 'Player does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND

	#Check if Player is admin
	elif not game.admin_player.id == int(player_id):
		content={'detail':'You are not authorized to start this game'}
		httpstatus=status.HTTP_401_UNAUTHORIZED

	#start the game by changing status and 
	elif game.players.all().count() < game.min_players :
		content={'detail': 'Please wait for more players to join'}
		httpstatus=status.HTTP_417_EXPECTATION_FAILED
	
	# if game is not in waiting state

	elif game.game_status != "w":
		content={'detail': 'Game Already Started or Finished'}
		httpstatus=status.HTTP_417_EXPECTATION_FAILED	

	else:
		isValid=True

	return return_dictionary(isValid,game,player,content,httpstatus)



def play_validation(game_id,player_id,word,start_loc,direction):
	""" 
	Validiation for Game Play 
	"""

	isValid=False
	game=None
	player=None
	content=None
	httpstatus=None

	game = check_if_game_exists(game_id)
	player=check_if_player_exists(player_id)

	if not game:
		content = {'detail': 'Game does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND

	#Check if Player Exists
	elif not player:
		content = {'detail': 'Player does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND

	elif not game.players.all().filter(id=player.id).exists():
		content = {'detail': 'Player not authorized'}
		httpstatus=status.HTTP_401_UNAUTHORIZED
	
	elif not game.game_status == 's':
		content = {'detail': 'Game not started or finished'}
		httpstatus=status.HTTP_401_UNAUTHORIZED

	elif not game.current_player.id == player.id:
		content = {'detail': 'It is not your turn to play'}
		httpstatus=status.HTTP_401_UNAUTHORIZED

	elif word is None or word.strip()== "":
		content = {'detail': 'Word can not be blank or None'}
		httpstatus=status.HTTP_404_NOT_FOUND

	elif direction is None or (direction != "RIGHT" and direction != "DOWN"):
		content = {'detail': 'Direction can be right or down'}
		httpstatus=status.HTTP_404_NOT_FOUND

	elif start_loc is None or len(start_loc) !=2:
		content = {'detail': 'start location must be provided or contain two values only.'}
		httpstatus=status.HTTP_404_NOT_FOUND
	
	else:
		isValid=True

	return return_dictionary(isValid,game,player,content,httpstatus) 




def pass_validation(game_id,player_id):
	""" 
	Validiation for Game Pass 
	"""

	isValid=False
	game=None
	player=None
	content=None
	httpstatus=None
	
	game = check_if_game_exists(game_id)
	player=check_if_player_exists(player_id)
	
	if not game:
		content = {'detail': 'Game does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND

	#Check if Player Exists
	elif not player:
		content = {'detail': 'Player does not exist'}
		httpstatus=status.HTTP_404_NOT_FOUND	

	elif not game.players.all().filter(id=player.id).exists():
		content = {'detail': 'Player not authorized'}
		httpstatus=status.HTTP_401_UNAUTHORIZED

	elif not game.game_status == 's':
		content = {'detail': 'Game not started or finished'}
		httpstatus=status.HTTP_401_UNAUTHORIZED

	elif not game.current_player.id == player.id:
		content = {'detail': 'It is not your turn to play'}
		httpstatus=status.HTTP_401_UNAUTHORIZED
	
	else:
		isValid=True

	return return_dictionary(isValid,game,player,content,httpstatus) 
	


def return_dictionary(isValid,game,player,content,httpstatus):
	return {'is_valid':isValid,'player':player,'game':game,'content':content,'status':httpstatus}
 