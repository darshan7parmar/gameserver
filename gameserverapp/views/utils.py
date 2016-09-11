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
	words_list.sort(key=lambda word: len(word), reverse=True)
	
	# Algorithm starts
	success=False
	placed_dict={}
	
	while not success:
		placed_count=0
		placed_dict={}
		for i in range(0,len(words_list)):
			
			word_placed=False
			word=words_list[i]
			word_len=len(word)
			
			while not word_placed:
				random_dir=random.choice(["HOR","VER"])
				if random_dir == "HOR":
					random_i=random.randint(0,len(grid)-1)
					random_j=random.randint(0,len(grid[0])-1-word_len)			
					if check_if_feasible_horizontal(word,grid,random_i,random_j):
						place_word_horizontal(word,grid,random_i,random_j)
						word_placed=True
						placed_count=placed_count+1
						placed_dict[word]={"location":[random_i,random_j],"direction":random_dir}
				else:
					random_i=random.randint(0,len(grid)-1-word_len)
					random_j=random.randint(0,len(grid[0])-1)
					if check_if_feasible_vertical(word,grid,random_i,random_j):
						place_word_vertical(word,grid,random_i,random_j)
						word_placed=True
						placed_count=placed_count+1
						placed_dict[word]={"location":[random_i,random_j],"direction":random_dir}

		if placed_count == len(words_list):
			success=True	
	place_random_char(grid)
	return placed_dict


def check_if_feasible_horizontal(word,grid,random_i,random_j):
	for k in range(0,len(word)):
		if not grid[random_i][random_j] == "-":
			if not grid[random_i][random_j] == word[k]:
				return False
		random_j=random_j+1
	return True

def check_if_feasible_vertical(word,grid,random_i,random_j):
	for k in range(0,len(word)):
		if not grid[random_i][random_j] == "-":
			if not grid[random_i][random_j] == word[k]:
				return False
		random_i=random_i+1
	return True




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


