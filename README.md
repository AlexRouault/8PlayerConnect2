# 8PlayerConnect2
Gameplay for an 8-player version of Connect 2 (Like Connect 4), with the intent of developing AI that learns to play the game well.

`<init.py>` is a python file that initializes the database for storing the AI startegy. **Running this file after filling the database will delete all of the AI's knowledge learned up to date!**

`<8PlayerConnect2.py>` is a python file that is in charge of running an instance of a game and moderating the learning of the AI.

`<strategy.db>` is a sqlite3 database that contains data necessary for the AI to decide where to make a move.