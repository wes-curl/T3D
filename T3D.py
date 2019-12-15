from os import system, name 
import random

def clear(): 
    #windows 
    if name == 'nt': 
        system('cls') 
    # for mac and linux 
    else: 
        system('clear')
     

def main():
    #initialize board
    board = newBoard()
    victor = ''
    while True:
        #draw board
        drawBoard(board)
        #ask for player input
        #a list, [x, y ,z]
        playerMove = getPlayerInput(board)
        board[playerMove[0]][playerMove[1]][playerMove[2]] = "X"
        #check for win -> break
        if anywin(board):#win(board, playerMove[0], playerMove[1], playerMove[2]):
            victor = "human"
            break
        #run AI
        #a list, [x, y, z]
        #AIMove = getAIMove(board)
        AIMove = decide(board)
        board[AIMove[0]][AIMove[1]][AIMove[2]] = "O"
        #check for win -> break
        if anywin(board):#win(board, AIMove[0], AIMove[1], AIMove[2]):
            victor = "AI"
            break
    #congratulate/shame player based on who won
    drawBoard(board)
    if victor == "human":
        print("Congratulations, player!")
    else:
        print("The computer wins!")
    


####################################################AI SUITE############################################

########################################################"STOLEN" AI SYSTEM######################################
#Based on a Tic-Tac-Toe AI from https://mitxela.com/projects/bf_tic_tac_toe
#simply: it always takes a win, then it takes a move that blocks a player win, then it picks from every other location via other methods.
#at the moment, the backup plan is randomness

#checks if a position is at the end of two in a row, if false, returns "". If Xs, X. If Os, O.
#that is: XYZ is empty, but the other two match
def endof(grids, x, y, z):
    #is XYZ empty?
    if grids[x][y][z] == "":
        #are there exactly two filled spaces in the row?
        #X
        if(grids[upval(x)][y][z] != "" and grids[downval(x)][y][z] != ""):
            #print("dingX")
            return grids[upval(x)][y][z]
        #Y
        elif(grids[x][upval(y)][z] != "" and grids[x][downval(y)][z] != ""):
            #print("dingY")
            return grids[x][upval(y)][z]
        #Z
        elif(grids[x][y][upval(z)]  != "" and grids[x][y][downval(z)]  != ""):
            #print("dingZ")
            return grids[x][y][upval(z)]
        else:
            return ""
    else:
        return ""

def downval(x):
    return - abs(2 * x - 1) + 3

def upval(x):
    return abs(x - 1)


#returns the coordinate where it will make its move
def decide(board):
    # the move that will be made if there are no instant wins
    backup = []
    # other moves that can be made
    available = []
    for x in range(0,3):
        for y in range(0,3):
            for z in range(0,3):
                value = endof(board, x,y,z)
                if value == "O":
                    print("O:",[x,y,z])
                    return [x,y,z]
                elif value == "X":
                    print("X:", [x,y,z])
                    backup = [x,y,z]
                else:
                    available.append([x,y,z])
    #there was no quick win, but there was a way to counter a human win
    if len(backup) == 3:
        return backup
    #no easy answers! Oh no! Pick a random point
    choice = random.random()
    choice *= len(available)
    choice = round(choice)

    return available[choice]



#########################PLAYER INPUT SUITE#####################################

#takes in nothing, returns a list of player input coords
def getPlayerInput(board):
    move = input("Please type your move in the format \'Numeral number letter\': \n")
    while not validInput(board, move):
        move = input("Please PROPERLY type your move in the format \'Numeral number letter\': \n")
    return interpret(move)

def validInput(board, move):
    brokenDownMove = move.split(" ")
    if brokenDownMove[0] == "DEBOOG":
        print("winstatus:", anywin(board))
        print(board)
        return False
    if brokenDownMove[0] == "DEBUGAT":
        print(win(board, int(brokenDownMove[1]), int(brokenDownMove[2]), int(brokenDownMove[3])))
    if brokenDownMove[0] == "PYCHIC":
        print(AIMoves(board))
    if brokenDownMove[0] != 'I' and brokenDownMove[0] != 'II' and brokenDownMove[0] != 'III':
        print('numeral error', brokenDownMove[0])
        return False
    elif brokenDownMove[1] != '1' and brokenDownMove[1] != '2' and brokenDownMove[1] != '3':
        print('number error', brokenDownMove[1])
        return False
    elif brokenDownMove[2] != 'A' and brokenDownMove[2] != 'a' and brokenDownMove[2] != 'B' and brokenDownMove[2] != 'b' and brokenDownMove[2] != 'C' and brokenDownMove[2] != 'c':
        print('letter error', brokenDownMove[2])
        return False
    valueAt = interpret(move)
    valueAt = board[valueAt[0]][valueAt[1]][valueAt[2]]
    return valueAt == ""

def interpret(move):
    brokenDownMove = move.split(" ")
    output = []
    if brokenDownMove[0] == "I":
        output.append(0)
    elif brokenDownMove[0] == "II":
        output.append(1) 
    else:
        output.append(2)

    if brokenDownMove[1] == "1":
        output.append(0) 
    elif brokenDownMove[1] == "2":
        output.append(1) 
    else:
        output.append(2)

    if brokenDownMove[2] == "a" or brokenDownMove[2] == "A":
        output.append(0) 
    elif brokenDownMove[2] == "b" or brokenDownMove[2] == "B":
        output.append(1) 
    else:
        output.append(2)

    return output

###########################################BOARD UTILITY SUITE#############################

def newBoard():
    board = []
    for G in range(0,3):
        Grid = []
        for R in range(0,3):
            Row = []
            for E in range(0,3):
                Row.append("")
            Grid.append(Row)
        board.append(Grid)
    return board

def liberate(board):
    output = []
    for G in board:
        grid = []
        for R in G:
            row = []
            for E in R:
                row.append(E)
            grid.append(row)
        output.append(grid)
    return output


def drawBoard(board):
    #the first row of Xs and Os
    firstRow = board[0][0] + board[1][0] + board[2][0]
    #the second row of Xs and Os
    secondRow = board[0][1] + board[1][1] + board[2][1]
    #the last row of Xs and Os
    thirdRow = board[0][2] + board[1][2] + board[2][2]
    print("                 I                        II                        III         ")
    print("          A      B      C          A       B      C           A      B      C   ")
    print()
    printRow(firstRow, "1")
    print("       ──────┼───────┼──────     ──────┼───────┼──────     ──────┼───────┼──────")
    printRow(secondRow, "2")
    print("       ──────┼───────┼──────     ──────┼───────┼──────     ──────┼───────┼──────")
    printRow(thirdRow, "3")
    print()

#prints an entire row, one row at a time
def printRow(row, number):
    for i in range(1, 4):
        print("    ", end="")
        printline(row, i, number)

                

#prints each letter, one level at a time, and divides them from each other
def printline(letters, level, number):
    if level == 2:
        print(number + "  ", end = "")
    else:
        print("   ", end="")
    for l in range(0, len(letters)):
        printLetter(letters[l], level)
        printVerticalDivider(l)
    print()

def printVerticalDivider(letterIndex):
    if letterIndex > 0 and (letterIndex + 1) % 3 == 0:
        print("     ", end = "")
    else:
        print(" │ ", end = "")

def full(board):
    for x in range (0,3):
        for y in range(0,3):
            for z in range(0,3):
                if board[x][y][z] == "":
                    return False
    return True


def win(grids, DX, DY, DZ):
    #For each coord: if all the variances of that coord are equal (while others stay constant), return true
    #X
    if(grids[0][DY][DZ] == grids[1][DY][DZ] == grids[2][DY][DZ] and grids[1][DY][DZ] != ""):
        return True
    #Y
    elif(grids[DX][0][DZ] == grids[DX][1][DZ] == grids[DX][2][DZ] and grids[DX][1][DZ] != ""):
        return True
    #Z
    elif(grids[DX][DY][0] == grids[DX][DY][1] == grids[DX][DY][2] and grids[DX][DY][1] != ""):
        return True
    else:
        return False
    #diagonals???


def anywin(grids):
    for x in range(0,3):
        for y in range(0,3):
            for z in range(0,3):
                if win(grids, x, y, z):
                    return True
    return False


def printLetter(letter, level):
    if letter == "":
        if level == 1:
            print("     ", end="")
        elif level == 2:
            print("     ", end="")
        else:
            print("     ", end="")
    elif letter == "O":
        if level == 1:
            print("╔═══╗", end="")
        elif level == 2:
            print("║   ║", end="")
        else:
            print("╚═══╝", end="")
    else:
        if level == 1:
            print("\   /", end="")
        elif level == 2:
            print("  X  ", end="")
        else:
            print("/   \\", end="")

######################################################################TEST CASES AND MAIN()#######################

main()

