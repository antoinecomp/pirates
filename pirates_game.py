# Flippy (an Othello or Reversi clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Based on the "reversi.py" code that originally appeared in "Invent
# Your Own Computer Games with Python", chapter 15:
#   http://inventwithpython.com/chapter15.html

import random, sys, pygame, copy
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 50 # width & height of each space on the board, in pixels
BOARDWIDTH = 11 # how many columns of spaces on the game board
BOARDHEIGHT = 3 # how many rows of spaces on the game board
EARTHWIDTH = 11
EARTHHEIGHT = 1
WHITE_TILE = 'WHITE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_TILE = 'HINT_TILE' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pirates !')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

# TO CHANGE image
    # Set up the background image.
    #boardImage = pygame.image.load('flippyboard.png')
    # Use smoothscale() to stretch the board image to fit the central line:
    #boardImage = pygame.transform.smoothscale(boardImage, (EARTHWIDTH * SPACESIZE, EARTHHEIGHT * SPACESIZE))
    #boardImageRect = boardImage.get_rect()
    #boardImageRect.topleft = (XMARGIN, YMARGIN + SPACESIZE)
# END TO CHANGE 
    BGIMAGE = pygame.image.load('sea.jpg')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    #BGIMAGE.blit(boardImage, boardImageRect)

    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Plays a single game each time this function is called.
    # Reset the board and game.

    mainBoard, moveBoard = getNewBoard()
    # print(mainBoard) 
    resetBoard(mainBoard) 
    # Reset the sailors and boat
    sailors = []
    white_sailors = []
    black_sailors = []

    sailors = resetSailors(sailors,mainBoard) # I HAVE TO SORT THE PIRATES ACCORDING TO THEIR NUMBERS ON A TILE
    turn = random.choice(['player1', 'player2'])

    # Draw the starting board
    drawBoard(mainBoard, sailors)
    # ask the player what color they want.
    playerTile, computerTile = enterPlayerTile() #MAYBE I HAVE TO SIMPLIFY
    print("Sale de enterPlayerTile")
    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    print("Surface and Rect objects for the New Game and Hints buttons done")


    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player1':
            print("player1's turn")
            # Player's turn:
            positionxy = None
            movexy = None
            while positionxy == None:
                # Keep looping until the player clicks on a valid space.
                # Determine which board data structure to use for display.
                boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        positionxy = getSpaceClicked(mousex, mousey)
                        print("Since adding groups sometimes it bugs at the very beginning")
                        white_sailors = [sailor for sailor in sailors if sailor.player == 'white']
                        black_sailors = [sailor for sailor in sailors if sailor.player == 'black']
                        # Here I have to check if it is one of the player's pirates:
                        if isPlayersPirate(positionxy[0],positionxy[1],white_sailors) == False:
                            return False

                while movexy == None:
                    # We have to show we have selected the sailor
                    # destination
                    for event in pygame.event.get(): # event handling loop
                        if event.type == MOUSEBUTTONUP:
                            # Handle mouse click events
                            xdestination, ydestiation = event.pos
                            # I don't know what does that stands for
                            if newGameRect.collidepoint( (xdestination, ydestiation) ):
                                # Start a new game
                                return True
                            # movexy is set to a two-item tuple XY coordinate, or None value
                            movexy = getSpaceClicked(xdestination, ydestiation)
                            print("Since adding groups sometimes it bugs at the very beginning")
                            white_sailors = [sailor for sailor in sailors if sailor.player == 'white']
                            black_sailors = [sailor for sailor in sailors if sailor.player == 'black']
                            # Here I have to check if the destination is empty:
                            # if isEmpty(movexy[0],movexy[1]) == False:
                            #    return False

                        # Check later if we can move the sailor according to the number of allowed move from moveboard 
                        #if movexy != None and not isValidMove(mainBoard, moveBoard, sailor, position[0], position[1], movexy[0], movexy[1]):
                        #    movexy = None

                # Make the move and end the turn.
                print(movexy[0], movexy[1])
                makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)

                # Draw the game board.
                drawBoard(boardToDraw,sailors)
                drawInfo(boardToDraw, playerTile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                DISPLAYSURF.blit(newGameSurf, newGameRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # get the new sailors 
            if getValidMoves(mainBoard, moveBoard, computerTile) != []:
                # Only set for the computer's turn if it can make a move.
                turn = 'player2'

    # Display the final score.
    drawBoard(mainBoard,sailors)
    scores = getScoreOfBoard(mainBoard)

    # Determine the text of the message to display. 
    
# TO MODIFY
    if scores[playerTile] > scores[computerTile]:
        text = 'You beat the computer by %s points! Congratulations!' % \
               (scores[playerTile] - scores[computerTile])
    elif scores[playerTile] < scores[computerTile]:
        text = 'You lost. The computer beat you by %s points.' % \
               (scores[computerTile] - scores[playerTile])
    else:
        text = 'The game was a tie!'
# TO MODIFY

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def isPlayersPirate(movex,movey,white_sailors):
    #check if there is a pirate at the given x and y position and if it is part of the player's pirates
    for sailor in white_sailors:
        if movex == sailor.x and movey == sailor.y and sailor.player == 'white':
            print("True")
            return True
    return False

def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


def drawBoard(board,sailors):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the sailors tiles
    for sailor in sailors:
        if sailor.player == 'white':
            board[sailor.x][sailor.y] = WHITE_TILE
        elif sailor.player == 'black':
            board[sailor.x][sailor.y] = BLACK_TILE
 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
               mousex < (x + 1) * SPACESIZE + XMARGIN and \
               mousey > y * SPACESIZE + YMARGIN and \
               mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None


def drawInfo(board, playerTile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    print(range(BOARDWIDTH),range(BOARDHEIGHT))
    print(len(board))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

def resetSailors(sailors,board):
    # sets up sailors and boats. # 2 sailors for each players
    #sailor_black_1 = Sailor('black',5,1,board)
    # sailor_black_2 = Sailor('black',5,1,board)
    sailor_white_1 = Sailor('white',5,1,board)
    # sailor_white_2 = Sailor('white',5,1,board)
    sailors = [sailor_white_1]
    # sailors += [sailor_black_1,sailor_black_2,sailor_white_1,sailor_white_2]

    boat_top_right = Boat(9,0)
    boat_top_left = Boat(2,0)
    boat_bottom_right = Boat(9,2)
    boat_bottom_left = Boat(2,2)

    return sailors

def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    boardMoves = []
    for i in range(BOARDWIDTH):
        MOVE = random.randint(1,5)
        board.append([EMPTY_SPACE] * BOARDHEIGHT)
        boardMoves.append([MOVE] * BOARDHEIGHT)# THE NUMBER OF MOVES ONE CAN DO ON A GIVEN tile

    return board,boardMoves


def isValidMove(board, boardMoves, sailor, xstart, ystart, xdestination, ydestiation):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnShip(xstart, ystart):
        return False

    sailor.x = xstart
    sailor.y = ystart

    # check if the destination is reachable from the boardMoves:
    if sailor.distance(xdestination,ydestiation) <= boardMoves(xstart, ystart):
        if isOnShip(sailor) and isShipAtPort(sailor) == False:
            if xdestination != xstart:
                return False
            else:
                return(xdestination,ydestiation)
        else:
            return(xdestination,ydestiation)
    else: 
        return False

def isOnShip(x, y):
    # Returns True if the coordinates are located on the Ship.
    return x == 0 or x == 2

def isShipAtPort(sailor):
    # check if the ship the sailor is it at a port
    pass


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_TILE
    return dupeBoard


def getValidMoves(board, boardMoves, sailor):
    # Returns a list of (x,y) tuples of all valid moves.
    # He can move as much as the tile where he is on the board allows him to
    # He can't go in the water unless he is driving a boat (two driving positions : front and back)
    # He can't move a boat if he was on hearth at the beginiing.
    moves = moveBoard[x][y]
    validMoves = []
    # two cases : on a boat or on the ground
    isOnEarth = True if(sailor.y == 1) else False # NOT VERY GOOD TO TEST ON MAGICAL VALUE 1
    # We take all tiles close enough to the sailor
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # Here we test the distance WE WILL TEST MOVEMENTS ON BOATS AFTERWARDS
            if isValidMove(board, boardMoves, sailor, x, y) != False:
                validMoves.append((x, y))    
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles.
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                xscore += 1
            if board[x][y] == BLACK_TILE:
                oscore += 1
    return {WHITE_TILE:xscore, BLACK_TILE:oscore}


def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [WHITE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, WHITE_TILE] if Black.

    # Create the text.
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [BLACK_TILE, WHITE_TILE]
                    
        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def makeMove(board, boardMoves, sailor, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    (x_end, y_end) = isValidMove(board, boardMoves, sailor, xstart, ystart)

    if x_end == False:
        return False

    board[xstart][ystart] = 'EMPTY_SPACE'

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    board[x_end][y_end] = sailor
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == BOARDWIDTH and y == 0) or \
           (x == 0 and y == BOARDHEIGHT) or \
           (x == BOARDWIDTH and y == BOARDHEIGHT)


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

class Sailor:
    def __init__(self, player,x,y,board):
        self.player = player
        self.x = x
        self.y = y
        self.board = board

    def distance(self,x,y):
        math.abs(self.x - x) + math.abs(self.y + y)

    def fire():
        pass

class Boat:
    def __init__(self,x,y):
        self.x = x
        self.y = y

if __name__ == '__main__':
    main()