#To print the board
def print_board():
    # center used to give equal space to each print
    print("".center(12),end="")
    #printing column headers
    for i in columns:
        print(i.center(12),end="")
    print()
    print()
    #iterating each row of board
    for i, row in zip(rows, board):
        #printing row header
        print(str(i).center(12),end="")
        #iterating each value of row and printing
        for j in row:
            print(j.center(12),end="")
        print()
    print()

#function to get x and y indexes from alphanumeric representation
def alphaNumericPosToNumericPos(position):
    x=8-int(position[1])
    y=ord(position[0])-97
    return (x,y)

#function to get alphanumeric representation from x and y indexes
def numericPosToAlphanumericPos(x,y):
    return chr(y+97)+str(x)

#function to get a coin on specific position by alphanumeric representation
def getCoin(position):
    (x,y)=alphaNumericPosToNumericPos(position)
    return board[x][y]

#Function to check whether player selected a valid coin
def isValidSelection(playerinput,player):
    #checking whether alphanumeric player input has length of 2
    if len(playerinput)==2:
        #checking whether player entered valid row and column values
        if playerinput[0] in columns and int(playerinput[1]) in rows:
            coin=getCoin(playerinput)
            #checking whether player selected his respective coin
            if (player==1 and coin.startswith("W")) or (player==2 and coin.startswith("B")):
                return True
    return False

#function to handle input from player while selecting his coin
def parseInput(player):
    # to get input from player until he enters valid input
    while True:
        playerinput=input("Player-"+str(player)+" Enter Your Coin Position - ")
        if playerinput=="exit": #to handle exit command
            return "exit"
        elif playerinput=="print": #to handle print command
            print_board()
        elif isValidSelection(playerinput,player): # to check if player entered valid alphanumric position
            return playerinput
        else: # to tell player entered invalid input
            print("Invalid Selection")

#function to check if the player entered valid help command
def isValidHelpCommand(playerinput):
    #spliting player command to check whether it's in correct format
    command=playerinput.split(" ")
    #checking whether player entered two space seperated value one is alphanumeric representation and second is --help command
    if len(command)==2:
        #checking whether player entered valid alphanumeric representation
        if len(command[0])==2 and command[0][0] in columns and int(command[0][1]) in rows and command[1]=="--help":
            return True
    return False

#function to handle help command
def handleHelp(position,player):
    #list to store chances of getting captured if player make this move
    chancesOfCaptures=[]
    (x,y)=alphaNumericPosToNumericPos(position)
    #first checking whether opponents pawn can capture if player make the move
    if player==1: # logic for player 1
        if x-1>=0 and y-1>=0 and board[x-1][y-1]=='B_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x+1,y-1),"B_PAWN"))
        if x-1>=0 and y+1<8 and board[x-1][y+1]=='B_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x+1,y+1),"B_PAWN"))
    else: # logic for player 2
        if x+1<8 and y+1<8 and board[x+1][y+1]=='W_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x-1,y+1),"W_PAWN"))
        if x+1<8 and y-1>=0 and board[x+1][y-1]=='W_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x-1,y-1),"W_PAWN"))
    #storing coin at destination in temp to calculate chance of getting capture
    temp=board[x][y]
    #temporarily making destination as empty
    board[x][y]='X'
    # calculating each opponents move to check whether any of the opponent coin can capture if player makes the move
    for i in range(8):
        for j in range(8):
            #checking each coin whether its opponent's coin
            if (player ==1 and board[i][j].startswith("B") and board[i][j]!="B_PAWN") or (player==2 and board[i][j].startswith("W") and board[i][j]!="W_PAWN"):
                #flag to pass inverse player value so getmoves function can calculate opponents moves
                playerFlag=1
                if player==1:
                    playerFlag=2
                #calculating moves of the coin                
                (moves,captures)=getMoves(board[i][j].split("_")[1],i,j,playerFlag)
                #chekcing whether moves of opponent coin has the position where player tries to move
                if position in moves:
                    chancesOfCaptures.append((numericPosToAlphanumericPos(8-i,j),board[i][j]))
    # restoring emptied board value from temp
    board[x][y]=temp
    #checking whether any of the opponents coin can capture if player makes the move
    if len(chancesOfCaptures)>0:
        #printing chances of getting captured if player makes the move
        print("Chances of getting captured")
        for i in chancesOfCaptures:
            print(" * "+ i[1]+" from "+i[0])
    else:
        #printing Safe Placec if opponent cannot capture if player makes the move
        print("Safe Place")

#function to handle player input to move a coin
def parseInputNewPosition(moves):
    while True:
        playerinput=input("Enter position to move or enter 'change' to change the selection : ")
        if playerinput=="change": # handling change command if player wants to switch the selected coin
            return "change"
        if playerinput=="exit": # handling exit command
            return "exit"
        elif playerinput=="print": #handling print command
            print_board()
        elif isValidHelpCommand(playerinput): # handling help command
            position=playerinput.split(" ")[0]
            handleHelp(position,player)
        elif playerinput in moves: # checking whether player entered valid move
            return playerinput
        else:
            print("Invalid Selection")

#function to check whether the obstruction is an opponent or same troop
def calculateCaptures(player,moves,captures,x,y):
    #checking whether the obstruction is an opponent or same troop
    if (player==1 and board[x][y].startswith("B")) or (player==2 and board[x][y].startswith("W")):
        #if it's opponent then finding its alphanumeric representation and coin then storing in captures list
        capturing_position=numericPosToAlphanumericPos(8-x,y)
        capturing_coin=board[x][y].split("_")[1]
        moves.append(capturing_position)
        captures.append((capturing_position,capturing_coin))

#function to calculate moves and captures
def getMoves(coin,x,y,player):
    # assigning empty list to moves and captures in the starting
    moves=[]
    captures=[]
    # to calculate moves if selected coin is pawn
    if coin=="PAWN":
        # checking whether it's player 1 or 2
        if player==1:
            # pawn can move 1 step forward so checking is it's empty
            if x-1>=0 and board[x-1][y]=="X":
                moves.append(numericPosToAlphanumericPos(8-x+1,y))
            # if it's the first move then pawn can move 2 step forward so checking if the path is clear
            if x==6 and board[x-1][y]=='X' and board[x-2][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-x+2,y))
            # pawn can capture diagonally so checking is there a chance
            if x-1>=0 and y-1>=0 and board[x-1][y-1].startswith("B"):
                position=numericPosToAlphanumericPos(8-x+1,y-1)
                capturing_coin=board[x-1][y-1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))            
            # pawn can capture diagonally so checking is there a chance
            if x-1>=0 and y+1>=0 and board[x-1][y+1].startswith("B"):
                position=numericPosToAlphanumericPos(8-x+1,y+1)
                capturing_coin=board[x-1][y+1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))                        
        else:
            # pawn can move 1 step forward so checking is it's empty
            if x+1<8 and board[x+1][y]=="X":
                moves.append(numericPosToAlphanumericPos(8-x-1,y))
            # if it's the first move then pawn can move 2 step forward so checking if the path is clear
            if x==1 and board[x+1][y]=='X' and board[x+2][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-x-2,y))
            # pawn can capture diagonally so checking is there a chance
            if x+1<8 and y-1>=0 and board[x+1][y-1].startswith("W"):
                position=numericPosToAlphanumericPos(8-x-1,y-1)
                capturing_coin=board[x+1][y-1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))            
            # pawn can capture diagonally so checking is there a chance
            if x+1<8 and y+1>=0 and board[x+1][y+1].startswith("W"):
                position=numericPosToAlphanumericPos(8-x-1,y+1)
                capturing_coin=board[x+1][y+1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))                        
    if coin=="KNIGHT": # checking if the selected coin is knight
        # knight have unique moves which is stored in a list
        knight_possibilities=[(1,2),(2,1),(-1,2),(2,-1),(1,-2),(-2,1),(-1,-2),(-2,-1)]
        # iterating over each possibility
        for possibility in knight_possibilities:
            (flagX,flagY)=possibility
            newX=flagX+x
            newY=flagY+y
            # checking whether the move is possible
            if newX>=0 and newX<8 and newY>=0 and newY<8:
                # checking whether the move is empty or obstruction
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else:
                    #checking the obstruction is an opponent or same troop
                    calculateCaptures(player,moves,captures,newX,newY)
    if coin=="ROOK" or coin=="QUEEN": # checking whether the selected coin is rook or queen since queen has the abilities of rook
        # iterating vertically towards down
        for i in range(x+1,8):
            # checking whether the move is empty or obstruction
            if board[i][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-i,y))
            else: 
                #checking the obstruction is an opponent or same troop and stopping there
                calculateCaptures(player,moves,captures,i,y)
                break
        # iterating vertically towards top
        for i in range(x-1,-1,-1):
            # checking whether the move is empty or obstruction
            if board[i][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-i,y))
            else: 
                #checking the obstruction is an opponent or same troop and stopping there
                calculateCaptures(player,moves,captures,i,y)
                break
        # iterating horizontally towards right
        for i in range(y+1,8):
            # checking whether the move is empty or obstruction
            if board[x][i]=='X':
                moves.append(numericPosToAlphanumericPos(8-x,i))
            else: 
                #checking the obstruction is an opponent or same troop and stopping there
                calculateCaptures(player,moves,captures,x,i)
                break
        # iterating horizontally towards left
        for i in range(y-1,-1,-1):
            # checking whether the move is empty or obstruction
            if board[x][i]=='X':
                moves.append(numericPosToAlphanumericPos(8-x,i))
            else: 
                #checking the obstruction is an opponent or same troop and stopping there
                calculateCaptures(player,moves,captures,x,i)
                break
    if coin=="BISHOP" or coin=="QUEEN":  # checking whether the selected coin is bishop or queen since queen has the abilities of bishop
        # iterating diagonaly towards bottom-right
        for i in range(1,8):
            newX=x+i
            newY=y+i
            # checking if it's valid position
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                # checking whether the move is empty or obstruction
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    #checking the obstruction is an opponent or same troop and stopping there
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
        # iterating diagonaly towards bottom-right
        for i in range(1,8):
            newX=x-i
            newY=y-i
            # checking if it's valid position
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                # checking whether the move is empty or obstruction
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    #checking the obstruction is an opponent or same troop and stopping there
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
        # iterating diagonaly towards bottom-right
        for i in range(1,8):
            newX=x-i
            newY=y+i
            # checking if it's valid position
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                # checking whether the move is empty or obstruction
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    #checking the obstruction is an opponent or same troop and stopping there
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
        # iterating diagonaly towards bottom-right
        for i in range(1,8):
            newX=x+i
            newY=y-i
            # checking if it's valid position
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                # checking whether the move is empty or obstruction
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    #checking the obstruction is an opponent or same troop and stopping there
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
    if coin=="KING": # checking whether the selected coin is a king
        # king has ability to move on eight direction one step, that is stored in list
        king_possibilities=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        # iterating over each possibility
        for possibility in king_possibilities:
            (flagX,flagY)=possibility
            newX=flagX+x
            newY=flagY+y
            # checking whether it's a valid move
            if newX>=0 and newX<8 and newY>=0 and newY<8:
                # checking whether the move is empty or obstruction
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else:
                    #checking the obstruction is an opponent or same troop
                    calculateCaptures(player,moves,captures,newX,newY)
    return (moves,captures)

#function to handle move
def moveCoin(currentPosition,newPosition):
    # calculating x and y indexes of current position
    (curX,curY)=alphaNumericPosToNumericPos(currentPosition)
    # calculating x and y indexes of new position
    (newX,newY)=alphaNumericPosToNumericPos(newPosition)
    # fetching coins at position
    coinAtSource=board[curX][curY]
    coinAtDestination=board[newX][newY]

    # defining string for writing history
    string="White " if coinAtSource.startswith("W") else "Black "
    # checking whether move is a empty or capture
    if coinAtDestination=='X':
        #if empty then writing as coin moved
        string+=coinAtSource.split("_")[1] + " at "+currentPosition+" has been moved to "+newPosition+"\n"
    else:
        #if capture then writing as coin captured
        string+= coinAtSource.split("_")[1] + " at "+currentPosition+" has captured "+coinAtDestination.split("_")[1]+" at "+newPosition+"\n"
    #to write the calculated string in file
    file.write(string)
    print(string)
    #moving coin to the new position
    board[newX][newY]=board[curX][curY]
    #making current position as empty
    board[curX][curY]="X"

# Defined default board structure in a 2d array
board = [
    ["B_ROOK", "B_KNIGHT", "B_BISHOP", "B_QUEEN", "B_KING", "B_BISHOP", "B_KNIGHT", "B_ROOK"],
    ["B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
    ["W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN"],
    ["W_ROOK", "W_KNIGHT", "W_BISHOP", "W_QUEEN", "W_KING", "W_BISHOP", "W_KNIGHT", "W_ROOK"]
]
# row headers
rows = [8, 7, 6, 5, 4, 3, 2, 1]
# column headers
columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
# printing board when starting the game
print_board()

path="GameHistory.txt" # provide full path if you need to store history in specific file like this - "C:/Users/ELCOT/Desktop/Chess_Game/GameHistory.txt"
#opening file for writing history
file = open(path,"w")

player=1 # 1 for white(player1), 2 for black(player2)

#to handle recursive player inputs
while True:
    #getting 1st input from player which is coin he wants to select
    currentPosition=parseInput(player)
    if(currentPosition=="exit"): # to handle exit command
        print("Game Ended")
        break

    # if player entered valid alphanumeric position then fetching coin at that position
    coin=getCoin(currentPosition)
    # letting player know which coin he has selected
    print("The Coin You have selected is - "+ coin.split("_")[1])
    (x,y)=alphaNumericPosToNumericPos(currentPosition)
    # calculating moves and captures which can make
    (moves,captures)=getMoves(coin.split("_")[1],x,y,player)
    # letting the player know the moves they can make
    if len(moves)>0:
        print("Moves You can Make - "+",".join(moves))
    else:
        print("You cannot move this coin right now")
    # letting the player know the captures they can make
    if len(captures)>0:
        print("Coins You can capture - ",captures)
    else:
        print("You cannot capture anything right now")

    # to handle new position input
    newPosition=parseInputNewPosition(moves)
    if newPosition=="change": # handle change command if it's a change he has to select a coin from the begining
        continue
    elif(newPosition=="exit"): # handling exit command
        print("Game Ended")
        break

    # if he entered valid new position then making that move
    moveCoin(currentPosition,newPosition)

    # switching player if current player is 1 then changing it to 2 and vice-versa
    if player==1:
        player=2
    else:
        player=1

#writing as Game ended in end of file and closing it safely
file.write("Game Ended\n")
file.close()
