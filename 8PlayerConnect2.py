import sqlite3
import random
import copy

class Connect2:

    def __init__(self, board=None):
        self.current_player = 1
        if board == None:
            self.board = [[" " for row in range(6)] for col in range(7)]
            # 05 15 25 35 45 55 65
            # 04 14 24 34 44 54 64
            # ... ... ... ... ...

    def __str__(self):
        rep = "+-+-+-+-+-+-+-+"
        for row in range(5,-1,-1):
            rep += "\n|" + "|".join([self.board[col][row] for col in range(7)]) + "|"
        rep += "\n+-+-+-+-+-+-+-+"
        return rep

    def get_board(self):
        return copy.deepcopy(self.board)

    def play(self, row):
        char = str(self.current_player)
        for i in range(6):
            if self.board[row][i] == " ":
                self.board[row][i] = char
                self.current_player = (self.current_player % 8) + 1
                return self.is_won()
        raise ValueError("Row Full!")

    def is_won(self):
        for col in range(7):
            for row in range(6):
                me = self.board[col][row]
                if me != " ":
                    for adj in self.adj(row, col):
                        if adj == me:
                            return True
                else:
                    break
        return False


    def adj(self, row, col):
        li = []
        if row != 0:
            li.append(self.board[col][row-1])
        if row != 5:
            li.append(self.board[col][row+1])
        if col != 0:
            li.append(self.board[col-1][row])
        if col != 6:
            li.append(self.board[col+1][row])
        if row != 0 and col != 0:
            li.append(self.board[col-1][row-1])
        if row != 5 and col != 0:
            li.append(self.board[col-1][row+1])
        if row != 0 and col != 6:
            li.append(self.board[col+1][row-1])
        if row != 5 and col != 6:
            li.append(self.board[col+1][row+1])
        return li

class AI:

    def __init__(self):
        self.mymoves = []
        
    def play(self, db, gameboard):
        c = db.cursor()
        c.execute("PRAGMA foreign_keys = ON;")

        #find the current gamestate of the board for the db
        moves_code = ""
        current = 1
        empty = False
        while not empty:
            empty = True
            for col in range(7):
                try:
                    if gameboard[col][0] == str(current):
                        moves_code += gameboard[col].pop()
                        current = (current % 8) + 1
                        empty = False
                        break
                except IndexError:
                    pass
        #....
            
        c.execute("SELECT column0, column1, column2, column3, column4, column5, column6 FROM beads WHERE gameboard = ?;", (moves_code,))
        data = c.fetchone()
        
        #If the moves_code does not exist in the DB (AI has not ever seen this gamestate), create
        # a new row in the DB with a moves_code corresponding to the current gamestate, and insert
        # the default number of beads into each column of this new row. Then, select a random
        # column to play in.
        if not data:
            c.execute("INSERT INTO beads (gameboard) VALUES (?)", (moves_code,))
            play = random.randint(0,6)
            self.mymoves.append((moves_code, play))
            return play
        #....

        #If the moves_code exists in the DB, select a random bead from the row, and play in its
        # column
        else:
            selection = random.randrange(sum(data))
            for column in range(7):
                selection -= data[column]
                if selection < 0:
                    return column
            raise Exception("We fucked up here!")
        #....
        
            

def gameplay():
    conn = sqlite3.connect("strategy.db")
    players = (AI(),AI(),AI(),AI(),AI(),AI(),AI(),AI())
    game = Connect2()
    player = 1
    while not game.is_won():
        game.play(players[(player - 1) % 8].play(conn, game.get_board()))
        player = (player % 8) + 1
        print(game.get_board())
    conn.commit()
    conn.close()
    

gameplay()
