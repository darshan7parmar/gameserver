GameServer API

1. POST /gameserver/game/create
	Info : Creates a new game on server 
	Parameters :  player_id [optional]  if player is already registered.
				  nick [optional] nick name of player.
	Response :
		201 : game_id  game created
		404 : player does not exists if player id provided.


2. POST /gameserver/game/join
	Info : a user can join game on server 
	Parameters :  game_id   - game id
				  player_id[optional] - player_id of user
				  nick[optional] - nick of user   
	Response :
		404 : Game does not exists | Player does not exists
		406 : Maximum player already joined game
		201 : Player created returns player_id

3. POST /gameserver/game/start
	Info : starts game on server 
	Parameters :  game_id   - game id 
				  player_id - player id of admin 
	Response :
		404 : Game does not exists | Player does not exists
		401 : Player is unauthorized
		417 : Please wait for more players to Join | Game already started or finished
		200 : Sucess returns game details

4. POST /gameserver/game/info
   Info : Information about a game
   Parameters: game_id - game id
   			   player_id - player id of any user who is entitled to play game 
   Response: 
   		404 : Game does not exists | Player does not exists
   		401 : Player is unauthorized
   		200 : Sucess returns game details

