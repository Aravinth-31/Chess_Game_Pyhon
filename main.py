
def print_board():
    row_format = "{:>15}" * (len(rows) + 1)
    print(row_format.format("", *columns))
    print()
    for team, row in zip(rows, board):
        print(row_format.format(team, *row))
    print()

board = [
    ["B_ROOK", "B_KNIGHT", "B_BISHOP", "B_QUEEN", "B_KING", "B_BISHOP", "B_KNIGHT", "B_ROOK"],
    ["B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN", "B_PAWN"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "X", "X", "X", "X", "X"],
    ["B_QUEEN", "X", "X", "X", "X", "X", "X", "X"],
    ["X", "X", "X", "W_KNIGHT", "X", "X", "X", "X"],
    ["W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN", "W_PAWN"],
    ["W_ROOK", "W_KNIGHT", "W_BISHOP", "W_QUEEN", "W_KING", "W_BISHOP", "W_KNIGHT", "W_ROOK"]
]
rows = [8, 7, 6, 5, 4, 3, 2, 1]
columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

print_board()

#path="C:/Users/ELCOT/Desktop/Chess_Game/GameHistory.txt"
path="GameHistory.txt"
file = open(path,"w")

player=1 # 1 for white(player1), 2 for black(player2)

def alphaNumericPosToNumericPos(position):
    x=8-int(position[1])
    y=ord(position[0])-97
    return (x,y)

def numericPosToAlphanumericPos(x,y):
    return chr(y+97)+str(x)

def getCoin(position):
    (x,y)=alphaNumericPosToNumericPos(position)
    return board[x][y]

def isValidSelection(playerinput,player):
    if len(playerinput)==2:
        if playerinput[0] in columns and int(playerinput[1]) in rows:
            coin=getCoin(playerinput)
            if (player==1 and coin.startswith("W")) or (player==2 and coin.startswith("B")):
                return True
    return False

def parseInput(player):
    while True:
        playerinput=input("Player-"+str(player)+" Enter Your Coin Position - ")
        if playerinput=="exit":
            return "exit"
        elif playerinput=="print":
            print_board()
        elif isValidSelection(playerinput,player):
            return playerinput
        else:
            print("Invalid Selection")

def isValidHelpCommand(playerinput):
    command=playerinput.split(" ")
    if len(command)==2:
        if len(command[0])==2 and command[0][0] in columns and int(command[0][1]) in rows and command[1]=="--help":
            return True
    return False

def handleHelp(position,player):
    chancesOfCaptures=[]
    (x,y)=alphaNumericPosToNumericPos(position)
    if player==1:
        if x-1>=0 and y-1>=0 and board[x-1][y-1]=='B_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x+1,y-1),"B_PAWN"))
        if x-1>=0 and y+1<8 and board[x-1][y+1]=='B_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x+1,y+1),"B_PAWN"))
    else:
        if x+1<8 and y+1<8 and board[x+1][y+1]=='W_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x-1,y+1),"W_PAWN"))
        if x+1<8 and y-1>=0 and board[x+1][y-1]=='W_PAWN':
            chancesOfCaptures.append((numericPosToAlphanumericPos(8-x-1,y-1),"W_PAWN"))
    temp=board[x][y]
    board[x][y]='X'
    for i in range(8):
        for j in range(8):
            if (player ==1 and board[i][j].startswith("B") and board[i][j]!="B_PAWN") or (player==2 and board[i][j].startswith("W") and board[i][j]!="W_PAWN"):
                playerFlag=1
                if player==1:
                    playerFlag=2
                (moves,captures)=getMoves(board[i][j].split("_")[1],i,j,playerFlag)
                if position in moves:
                    chancesOfCaptures.append((numericPosToAlphanumericPos(8-i,j),board[i][j]))
    board[x][y]=temp
    if len(chancesOfCaptures)>0:
        print("Chances of getting captured")
        for i in chancesOfCaptures:
            print(" * "+ i[1]+" from "+i[0])
    else:
        print("Safe Place")

def parseInputNewPosition(moves):
    while True:
        playerinput=input("Enter position to move or enter 'change' to change the selection : ")
        if playerinput=="change":
            return "change"
        if playerinput=="exit":
            return "exit"
        elif playerinput=="print":
            print_board()
        elif isValidHelpCommand(playerinput):
            position=playerinput.split(" ")[0]
            handleHelp(position,player)
        elif playerinput in moves:
            return playerinput
        else:
            print("Invalid Selection")

def calculateCaptures(player,moves,captures,x,y):
    if (player==1 and board[x][y].startswith("B")) or (player==2 and board[x][y].startswith("W")):
        capturing_position=numericPosToAlphanumericPos(8-x,y)
        capturing_coin=board[x][y].split("_")[1]
        moves.append(capturing_position)
        captures.append((capturing_position,capturing_coin))

def getMoves(coin,x,y,player):
    moves=[]
    captures=[]
    if coin=="PAWN":
        if player==1:
            if x-1>=0 and board[x-1][y]=="X":
                moves.append(numericPosToAlphanumericPos(8-x+1,y))
            if x==6 and board[x-1][y]=='X' and board[x-2][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-x+2,y))
            if x-1>=0 and y-1>=0 and board[x-1][y-1].startswith("B"):
                position=numericPosToAlphanumericPos(8-x+1,y-1)
                capturing_coin=board[x-1][y-1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))            
            if x-1>=0 and y+1>=0 and board[x-1][y+1].startswith("B"):
                position=numericPosToAlphanumericPos(8-x+1,y+1)
                capturing_coin=board[x-1][y+1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))                        
        else:
            if x+1<8 and board[x+1][y]=="X":
                moves.append(numericPosToAlphanumericPos(8-x-1,y))
            if x==1 and board[x+1][y]=='X' and board[x+2][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-x-2,y))
            if x+1<8 and y-1>=0 and board[x+1][y-1].startswith("W"):
                position=numericPosToAlphanumericPos(8-x-1,y-1)
                capturing_coin=board[x+1][y-1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))            
            if x+1<8 and y+1>=0 and board[x+1][y+1].startswith("W"):
                position=numericPosToAlphanumericPos(8-x-1,y+1)
                capturing_coin=board[x+1][y+1].split("_")[1]
                moves.append(position)
                captures.append((position,capturing_coin))                        
    if coin=="KNIGHT":
        knight_possibilities=[(1,2),(2,1),(-1,2),(2,-1),(1,-2),(-2,1),(-1,-2),(-2,-1)]
        for possibility in knight_possibilities:
            (flagX,flagY)=possibility
            newX=flagX+x
            newY=flagY+y
            if newX>=0 and newX<8 and newY>=0 and newY<8:
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else:
                    calculateCaptures(player,moves,captures,newX,newY)
    if coin=="ROOK" or coin=="QUEEN":
        for i in range(x+1,8):
            if board[i][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-i,y))
            else: 
                calculateCaptures(player,moves,captures,i,y)
                break
        for i in range(x-1,-1,-1):
            if board[i][y]=='X':
                moves.append(numericPosToAlphanumericPos(8-i,y))
            else: 
                calculateCaptures(player,moves,captures,i,y)
                break
        for i in range(y+1,8):
            if board[x][i]=='X':
                moves.append(numericPosToAlphanumericPos(8-x,i))
            else: 
                calculateCaptures(player,moves,captures,x,i)
                break
        for i in range(y-1,-1,-1):
            if board[x][i]=='X':
                moves.append(numericPosToAlphanumericPos(8-x,i))
            else: 
                calculateCaptures(player,moves,captures,x,i)
                break
    if coin=="BISHOP" or coin=="QUEEN":
        for i in range(1,8):
            newX=x+i
            newY=y+i
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
        for i in range(1,8):
            newX=x-i
            newY=y-i
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
        for i in range(1,8):
            newX=x-i
            newY=y+i
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
        for i in range(1,8):
            newX=x+i
            newY=y-i
            if newX<8 and newX>=0 and newY<8 and newY>=0:
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else: 
                    calculateCaptures(player,moves,captures,newX,newY)
                    break
    if coin=="KING":
        king_possibilities=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for possibility in king_possibilities:
            (flagX,flagY)=possibility
            newX=flagX+x
            newY=flagY+y
            if newX>=0 and newX<8 and newY>=0 and newY<8:
                if board[newX][newY]=='X':
                    moves.append(numericPosToAlphanumericPos(8-newX,newY))
                else:
                    calculateCaptures(player,moves,captures,newX,newY)
    return (moves,captures)

def moveCoin(currentPosition,newPosition):
    (curX,curY)=alphaNumericPosToNumericPos(currentPosition)
    (newX,newY)=alphaNumericPosToNumericPos(newPosition)
    coinAtSource=board[curX][curY]
    coinAtDestination=board[newX][newY]
    string="White " if coinAtSource.startswith("W") else "Black "
    if coinAtDestination=='X':
        string+=coinAtSource.split("_")[1] + " at "+currentPosition+" has been moved to "+newPosition+"\n"
    else:
        string+= coinAtSource.split("_")[1] + " at "+currentPosition+" has captured "+coinAtDestination.split("_")[1]+" at "+newPosition+"\n"
    file.write(string)
    print(string)
    board[newX][newY]=board[curX][curY]
    board[curX][curY]="X"
while True:
    currentPosition=parseInput(player)
    if(currentPosition=="exit"):
        print("Game Ended")
        break

    coin=getCoin(currentPosition)
    print("The Coin You have selected is - "+ coin.split("_")[1])
    (x,y)=alphaNumericPosToNumericPos(currentPosition)
    (moves,captures)=getMoves(coin.split("_")[1],x,y,player)
    if len(moves)>0:
        print("Moves You can Make - "+",".join(moves))
    else:
        print("You cannot move this coin right now")
    if len(captures)>0:
        print("Coins You can capture - ",captures)
    else:
        print("You cannot capture anything right now")

    newPosition=parseInputNewPosition(moves)
    if newPosition=="change":
        continue
    elif(newPosition=="exit"):
        print("Game Ended")
        break

    moveCoin(currentPosition,newPosition)

    if player==1:
        player=2
    else:
        player=1
file.write("Game Ended\n")
file.close()
