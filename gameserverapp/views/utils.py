from gameserverapp.models import *
from gameserverapp.serializers import *
from gameserver import settings
import random
import re
import string

""" 
Grid related methods below 
"""

def initialize_grid(row,column):
	grid = []
	for i in range(row):
		empty_row = []
		for j in range(column):
			empty_row.append("-")
		grid.append(empty_row)
	return grid


def get_random_words(num_words):
	word_file = "words"
	WORDS = open(word_file).read().splitlines()
	words_list=[]
	for i in range(0,num_words):
		random_word=random.choice(WORDS)
		random_word = re.sub('[^0-9a-zA-Z]+', '', random_word)
		words_list.append(str(random_word))
	return words_list



def generate_grid(grid,words_list):
	placed_wordlist=[]
	words_list.sort(key=lambda word: len(word), reverse=True)
	# Algorithm starts
	success=False
	while not success:
		for i in range(0,len(words_list)):
			word_not_placed=False
			word=words_list[i]
			while not word_not_placed:
				random_i=random.choice(0,range(len(grid)))
				random_j=random.choice(0,range(len(grid)))
				random_dir=random.choice(["HOR","VER"])
				if random_dir == "HOR":
					check_if_feasible_horizonal(word,grid,random_i,random_j)
				else:
					check_if_feasible_vertical(word,grid,random_i,random_j)

	place_random_char(grid)




def check_if_feasible_horizontal(word,grid,random_i,random_j):
	pass


def place_word_horizontal(word,grid,i,j):
	for k in range(0,len(word)):
		grid[i][j+k]=word[k]

def place_word_vertical(word,grid,i,j):
	for k in range(0,len(word)):
		grid[i+k][j]=word[k]

def place_random_char(grid):

	for i in range(len(grid)):
		print (str(i))
		for j in range(len(grid[0])):
			if grid[i][j] == '-':
				grid[i][j]=random.choice(string.ascii_letters)



""" 
Create functions below  
"""

def create_player(game):
	player=Player.objects.create()
	player.nick="player"+str(player.id)
	player.save()
	return player



""" 
Validation functions below  
"""
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



def check_if_max_limit_reached(game):
	num_players=game.players.all().count()
	if num_players >= game.max_players :
		return True
	return False
