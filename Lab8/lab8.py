import random
from random import choice
from collections import Counter
import json


class Menace:

    def __init__(x):
        x.board = [" "]*9
        x.beads = [10]*9
        # x.matchboxes = {}
        x.movesplayed = []
        try:
            a_file = open("data.json", "r")
            # output = a_file.read()
            x.matchboxes = json.loads(a_file.read())
        except:
            x.matchboxes = {}
            # print("No Pre Game exist")

    def printBoard(x):
        print("\nPositions:")
        print("0 | 1 | 2   ", x.board[0],
              "|", x.board[1], "|", x.board[2])
        print("--+---+--    --+---+--")
        print("3 | 4 | 5   ", x.board[3],
              "|", x.board[4], "|", x.board[5])
        print("--+---+--    --+---+--")
        print("6 | 7 | 8   ", x.board[6],
              "|", x.board[7], "|", x.board[8])
        print("\n")

    def userChance(x):
        pos = int(input("Enter position: "))
        if x.board[pos] != " ":
            print("Wrong input enter again")
            x.userChance()
        else:
            x.board[pos] = "X"

    def compChance(x):
        current_board = x.board_string()
        # print("board", movesplayed)
        if current_board not in x.matchboxes:
            new_beads = [pos for pos, mark in enumerate(
                current_board) if mark == ' ']
            # Early boards start with more beads
            x.matchboxes[current_board] = new_beads * \
                ((len(new_beads) + 2) // 2)

        current_beads = x.matchboxes[current_board]
        if len(current_beads):
            bead = random.choice(current_beads)
            x.movesplayed.append((current_board, bead))
        else:
            bead = -1
        
        return bead

    def win(x):
        if (x.board[0] != ' ' and
            ((x.board[0] == x.board[1] == x.board[2]) or
             (x.board[0] == x.board[3] == x.board[6]) or
             (x.board[0] == x.board[4] == x.board[8]))) or (x.board[4] != ' ' and
                                                                     ((x.board[1] == x.board[4] == x.board[7]) or
                                                                      (x.board[3] == x.board[4] == x.board[5]) or
                                                                      (x.board[2] == x.board[4] == x.board[6]))) or (x.board[8] != ' ' and
                                                                                                                              ((x.board[2] == x.board[5] == x.board[8]) or
                                                                                                                               (x.board[6] == x.board[7] == x.board[8]))):
            return True
        else:
            return False

    def game_tie(x):
        c = Counter(x.board)
        for i in c:
            if (i == " "):
                return False
        return True

    def changing_bead(x, n):
        if n == 3:
            for (board, bead) in x.movesplayed:
                x.matchboxes[board].extend([bead, bead, bead])
            # x.num_win += 1
        if n == 2:
            for (board, bead) in x.movesplayed:
                x.matchboxes[board].append(bead)
        if n == 1:
            # Lose, remove a bead
            for (board, bead) in x.movesplayed:
                matchbox = x.matchboxes[board]
                del matchbox[matchbox.index(bead)]

    def resetGame(x):
        x.board = [" "]*9
        x.movesplayed = []

    def board_string(x):
        return ''.join(x.board)

    def playGame(x):
        chance = 0
        while (True):
            chance += 1
            move = x.compChance()
            x.board[move] = "O"
            # if chance>=2:
            if x.win():
                x.printBoard()
                x.changing_bead(3)
                print("Computer Won")
                break
            if x.game_tie():
                x.printBoard()
                x.changing_bead(2)
                print("Game game_tie")
                break
            x.printBoard()
            x.userChance()
            # if chance>=2:
            if x.win():
                x.printBoard()
                x.changing_bead(1)
                print("You Won")
                break

    def instructions(x):
        print("\n")
        print("###########################################################")
        print("Welcome to MENACE Tic Tac Toe")
        print("The computer will gradually learn from the matches")
        print("The difficulty will increase with more number of matches")
        print("You are X and the Computer is O")
        print("Start Playing!")
        print("###########################################################")
        print("\n")

    def exit(x):
        ans = input("\nDo you want to continue? Yes or No \n")
        if ans.lower() == "no":
            print("Thank you for playing!! \n")
            a_file = open("data.json", "w")
            json.dump(x.matchboxes, a_file)
            a_file.close()
            return True
        else:
            a_file = open("data.json", "w")
            json.dump(x.matchboxes, a_file)
            a_file.close()
            return False




if __name__ == '__main__':
    stop = False
    M = Menace()
    while(not stop):
        M.instructions()
        
        M.playGame()
        
        stop = M.exit()
        M.resetGame()