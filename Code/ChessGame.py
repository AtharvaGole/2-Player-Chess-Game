#Imports
import pygame, random, sys, time
from pygame.locals import *

#Setting up the pygame window
width,height,topMenu=800,600,0
pygame.init()
gameDisplay=pygame.display.set_mode((width,height+topMenu))

#Fonts to be used for display
font = pygame.font.SysFont("comicsansms", 60)
font1 = pygame.font.SysFont("comicsansms", 25)

#Colors to be used
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

#Method for drawinf text on the pygame window
def drawtext(text, font, surface, x, y):        
    textobj = font.render(text, 1, blue)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

#Keeps the track of all the dead pieces on the board
def deadPiece(piece):
    data=piece.getName()
    if data[1] is "White":
        if data[0] is "Pawn":
            deadWhite[0].append(piece)
        else:
            deadWhite[1].append(piece)
    else:
        if data[0] is "Pawn":
            deadBlack[0].append(piece)
        else:
            deadBlack[1].append(piece)

#Draws the dead pieces of both the players on both the sides of the board
def drawDeadPiece():
    #For drawing dead white pieces
    for itr in deadWhite:
        k=0
        for piece in itr:
            data=piece.getName()
            if data[0] is "Pawn":
                piece.drawPieceByCoordinates(width-(width-height)/2,k*height/8+topMenu,data[1])
            else:
                piece.drawPieceByCoordinates(width-(width-height)/2+40,k*height/8+topMenu,data[1])
            k+=1
            
    #For drawing dead black pieces
    for itr in deadBlack:
        k=0
        for piece in itr:
            data=piece.getName()
            if data[0] is "Pawn":
                piece.drawPieceByCoordinates(0,k*height/8+topMenu,data[1])
            else:
                piece.drawPieceByCoordinates(40,k*height/8+topMenu,data[1])
            k+=1

#Loads the image of the required name            
def load_image(imagename):
    return pygame.image.load(imagename)

"""
Every object of this class is a piece on the chess board like Pawn, Rook, Knight, Bishop, Queen and King.
It stores all the information of a piece like its name, which player it belongs to, its coordinates, etc.
It contains methods for drawing the piece. 
"""

class Piece:
    #Initializes the piece with its co-ordinates, name and which player it belongs to
    def __init__(self,x,y,name,player):
        self.name=name
        self.player=player
        self.x=x
        self.y=y
        if self.name is "Pawn":
            self.adjustx,self.adjusty=15,10
        elif self.name is "Rook" or self.name is "Knight":
            self.adjustx,self.adjusty=11,10
        elif self.name is "Bishop":
            self.adjustx,self.adjusty=5,10
        elif self.name is "Queen" or self.name is "King":
            self.adjustx,self.adjusty=9,10
    
    #It returns name and the player name it belongs to
    def getName(self):
        return [self.name,self.player]

    #It returns the position of the piece
    def getPosition(self):
        return (self.x,self.y)
    
    #it sets the position of a piece. It used when a piecce is moved
    def setPosition(self,x,y):
        self.x=x
        self.y=y

    #It displays the piece on the board    
    def drawPiece(self):
        if self.player is "White":
            player="1"
        else:
            player="2"
        if (self.x+self.y)%2==0:
            color="1"
        else:
            color="2"
        self.image = load_image(self.name+player+color+".png")
        self.imagerect = self.image.get_rect()
        self.imagerect.left = (width-height)/2+self.x*height/8+self.adjustx
        self.imagerect.top = self.y*height/8+self.adjusty+topMenu
        gameDisplay.blit(self.image,self.imagerect)

    #It displays the piece on the board    
    def drawPieceByCoordinates(self,x,y,player):
        if player is "White":
            player="1"
        else:
            player="2"
        color="2"
        self.image = load_image(self.name+player+color+".png")
        self.imagerect = self.image.get_rect()
        self.imagerect.left = x
        self.imagerect.top = y+topMenu
        gameDisplay.blit(self.image,self.imagerect)

"""
It is used for storing the chess Grid. As there is only one chess grid. List grid is made static.
The grid list contains all the objects of pieces present on the board. If any element is None then it means that there is no piece at that position.
It's methods are used for displaying the grid, drawing the pieces,etc.
"""
class Grid:
    #Static lsit grid
    grid=[]
    
    #Iniatializes the grid at the start of the game.
    def __init__(self):
        self.grid=[[None for j in range(8)] for i in range(8)]
        self.grid[0][6],self.grid[1][6],self.grid[2][6],self.grid[3][6],self.grid[4][6],self.grid[5][6],self.grid[6][6],self.grid[7][6],self.grid[0][7],self.grid[1][7],self.grid[2][7],self.grid[3][7],self.grid[4][7],self.grid[5][7],self.grid[6][7],self.grid[7][7]=Piece(0,6,"Pawn","White"),Piece(1,6,"Pawn","White"),Piece(2,6,"Pawn","White"),Piece(3,6,"Pawn","White"),Piece(4,6,"Pawn","White"),Piece(5,6,"Pawn","White"),Piece(6,6,"Pawn","White"),Piece(7,6,"Pawn","White"),Piece(0,7,"Rook","White"),Piece(1,7,"Knight","White"),Piece(2,7,"Bishop","White"),Piece(3,7,"Queen","White"),Piece(4,7,"King","White"),Piece(5,7,"Bishop","White"),Piece(6,7,"Knight","White"),Piece(7,7,"Rook","White")
        self.grid[0][1],self.grid[1][1],self.grid[2][1],self.grid[3][1],self.grid[4][1],self.grid[5][1],self.grid[6][1],self.grid[7][1],self.grid[0][0],self.grid[1][0],self.grid[2][0],self.grid[3][0],self.grid[4][0],self.grid[5][0],self.grid[6][0],self.grid[7][0]=Piece(0,1,"Pawn","Black"),Piece(1,1,"Pawn","Black"),Piece(2,1,"Pawn","Black"),Piece(3,1,"Pawn","Black"),Piece(4,1,"Pawn","Black"),Piece(5,1,"Pawn","Black"),Piece(6,1,"Pawn","Black"),Piece(7,1,"Pawn","Black"),Piece(0,0,"Rook","Black"),Piece(1,0,"Knight","Black"),Piece(2,0,"Bishop","Black"),Piece(3,0,"Queen","Black"),Piece(4,0,"King","Black"),Piece(5,0,"Bishop","Black"),Piece(6,0,"Knight","Black"),Piece(7,0,"Rook","Black")

    #Returns grid    
    def getGrid(self):
        return self.grid

    #Displays the grid
    def displayGrid(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    pygame.draw.rect(gameDisplay,(50,50,50),(i*(height)/8+(width-height)/2,j*(height)/8+topMenu,(height)/8,(height)/8))
                else:
                    pygame.draw.rect(gameDisplay,(200,200,200),(i*(height)/8+(width-height)/2,j*(height)/8+topMenu,(height)/8,(height)/8))
                pygame.draw.rect(gameDisplay,black,(i*(height)/8+(width-height)/2,j*(height)/8+topMenu,(height)/8,(height)/8),1)
        self.drawPiece()

    #Displays the pieces
    def drawPiece(self):
        for i in range(8):
            for j in range(8):
                if self.grid[i][j]!=None:
                    self.grid[i][j].drawPiece()
                    
"""
It is responsible for handling turns of a player, checking whether a move is valid or not, checking for checks,checkmates, stalemates, 
castelling, showing valid positions of a piece, etc.
"""
class Chess:
    grid=None
    #Initialzes the game
    def __init__(self):
        self.grid=Grid()
        self.turn="White"
        self.check_w=False
        self.check_b=False
        self.king_w=False
        self.king_b=False
        self.rook_w_l=False
        self.rook_w_r=False
        self.rook_b_l=False
        self.rook_b_r=False
    
    #Keeps track of the turn
    def toggle_turn(self):
        if self.turn is "White":
            self.turn="Black"
        else:
            self.turn="White"
            
    #Returns which player's turn it is
    def getTurn(self):
        return self.turn
    
    #Checks if the player making the move has it's turn or not
    def correct_player(self,x,y):
        if self.grid.grid[x][y]!=None and self.grid.grid[x][y].player==self.turn:
            return True
        return False

    #It moves th piece
    def movePiece(self,oldPosition,newPosition):
        #print(self.grid.grid[oldPosition[0]][oldPosition[1]].name is "King")
        if self.grid.grid[oldPosition[0]][oldPosition[1]].name is "King" and abs(newPosition[0]-oldPosition[0])==2:
            #print(newPosition,"abc")
            if newPosition==[2,7]:
                self.grid.grid[0][7].setPosition(3,7)
                self.grid.grid[3][7]=self.grid.grid[0][7]
                self.grid.grid[0][7]=None
            elif newPosition==[6,7]:
                self.grid.grid[7][7].setPosition(5,7)
                self.grid.grid[5][7]=self.grid.grid[7][7]
                self.grid.grid[7][7]=None
            elif newPosition==[2,0]:
                self.grid.grid[0][0].setPosition(3,0)
                self.grid.grid[3][0]=self.grid.grid[0][0]
                self.grid.grid[0][0]=None
            else:
                self.grid.grid[7][0].setPosition(5,0)
                self.grid.grid[5][0]=self.grid.grid[7][0]
                self.grid.grid[7][0]=None
            
        #print(oldPosition,newPosition)
        self.grid.grid[oldPosition[0]][oldPosition[1]].setPosition(newPosition[0],newPosition[1])
        self.grid.grid[newPosition[0]][newPosition[1]]=self.grid.grid[oldPosition[0]][oldPosition[1]]
        self.grid.grid[oldPosition[0]][oldPosition[1]]=None

    def removePiece(self,x,y):
        #print(self.grid.grid[x][y],x,y,"x y")
        if self.grid.grid[x][y]!=None:
            deadPiece(self.grid.grid[x][y])
        
    def showHint(self,x,y):
        #print("call ShowHint")
        clickedPiece=self.grid.getGrid()[x][y]
        places=[]
        if clickedPiece==None:
            return
        if clickedPiece.getName()[0] is "Pawn":
            if clickedPiece.getName()[1] is "White":
                if y==6 and self.grid.getGrid()[x][y-1]==None and self.grid.getGrid()[x][y-2]==None and self.valid_move([x,y],[x,y-2]):
                    self.highlight(x,y-2)
                    places.append([x,y-2])
                if y-1>=0 and self.grid.getGrid()[x][y-1]==None and self.valid_move([x,y],[x,y-1]):
                    self.highlight(x,y-1)
                    places.append([x,y-1])
                if x-1>=0 and y-1>=0 and self.grid.getGrid()[x-1][y-1]!=None and (self.grid.getGrid()[x-1][y-1].getName()[1] is "Black") and self.valid_move([x,y],[x-1,y-1]):
                    self.highlight(x-1,y-1)
                    places.append([x-1,y-1])
                if x+1<8 and y-1>=0 and self.grid.getGrid()[x+1][y-1]!=None and(self.grid.getGrid()[x+1][y-1].getName()[1] is "Black") and self.valid_move([x,y],[x+1,y-1]):
                    self.highlight(x+1,y-1)
                    places.append([x+1,y-1])
            else:
                if y==1 and self.grid.getGrid()[x][y+1]==None and self.grid.getGrid()[x][y+2]==None and self.valid_move([x,y],[x,y+2]):
                    self.highlight(x,y+2)
                    places.append([x,y+2])
                if y+1<8 and self.grid.getGrid()[x][y+1]==None and self.valid_move([x,y],[x,y+1]):
                    self.highlight(x,y+1)
                    places.append([x,y+1])
                if x-1>=0 and y+1<8 and self.grid.getGrid()[x-1][y+1]!=None and (self.grid.getGrid()[x-1][y+1].getName()[1] is "White") and self.valid_move([x,y],[x-1,y+1]):
                    self.highlight(x-1,y+1)
                    places.append([x-1,y+1])
                if x+1<8 and y+1<8 and self.grid.getGrid()[x+1][y+1]!=None and (self.grid.getGrid()[x+1][y+1].getName()[1] is "White") and self.valid_move([x,y],[x+1,y+1]):
                    self.highlight(x+1,y+1)
                    places.append([x+1,y+1])

        elif clickedPiece.getName()[0] is "Rook":
            places=self.check(x,y,"straight")
       
        elif clickedPiece.getName()[0] is "Knight":
            if y-2>=0:
                if x-1>=0 and (self.grid.getGrid()[x-1][y-2]==None or (self.grid.getGrid()[x-1][y-2]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x-1][y-2].getName()[1]))) and self.valid_move([x,y],[x-1,y-2]):
                    self.highlight(x-1,y-2)
                    places.append([x-1,y-2])
                if x+1<8 and (self.grid.getGrid()[x+1][y-2]==None or (self.grid.getGrid()[x+1][y-2]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x+1][y-2].getName()[1]))) and self.valid_move([x,y],[x+1,y-2]):
                    self.highlight(x+1,y-2)
                    places.append([x+1,y-2])
            if y+2<8:
                if x-1>=0 and (self.grid.getGrid()[x-1][y+2]==None or (self.grid.getGrid()[x-1][y+2]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x-1][y+2].getName()[1]))) and self.valid_move([x,y],[x-1,y+2]):
                    self.highlight(x-1,y+2)
                    places.append([x-1,y+2])
                if x+1<8 and (self.grid.getGrid()[x+1][y+2]==None or (self.grid.getGrid()[x+1][y+2]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x+1][y+2].getName()[1]))) and self.valid_move([x,y],[x-1,y+2]):
                    self.highlight(x+1,y+2)
                    places.append([x+1,y+2])
            if x-2>=0:
                if y-1>=0 and (self.grid.getGrid()[x-2][y-1]==None or (self.grid.getGrid()[x-2][y-1]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x-2][y-1].getName()[1]))) and self.valid_move([x,y],[x-2,y-1]):
                    self.highlight(x-2,y-1)
                    places.append([x-2,y-1])
                if y+1<8 and (self.grid.getGrid()[x-2][y+1]==None or (self.grid.getGrid()[x-2][y+1]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x-2][y+1].getName()[1])))and self.valid_move([x,y],[x-2,y+1]):
                    self.highlight(x-2,y+1)
                    places.append([x-2,y+1])
            if x+2<8:
                if y-1>=0 and (self.grid.getGrid()[x+2][y-1]==None or (self.grid.getGrid()[x+2][y-1]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x+2][y-1].getName()[1]))) and self.valid_move([x,y],[x+2,y-1]):
                    self.highlight(x+2,y-1)
                    places.append([x+2,y-1])
                if y+1<8 and (self.grid.getGrid()[x+2][y+1]==None or (self.grid.getGrid()[x+2][y+1]!=None and (self.grid.getGrid()[x][y].getName()[1] is not self.grid.getGrid()[x+2][y+1].getName()[1])))and self.valid_move([x,y],[x+2,y+1]):
                    self.highlight(x+2,y+1)
                    places.append([x+2,y+1])

    
        elif clickedPiece.getName()[0] is "Bishop":
            places=self.check(x,y,"diagonal")
            
        elif clickedPiece.getName()[0] is "Queen":
            places=self.check(x,y,"straight")
            places+=self.check(x,y,"diagonal")
       
        elif clickedPiece.getName()[0] is "King":
            arr=[[-1,0,1,-1,1,-1,0,1],[-1,-1,-1,0,0,1,1,1]]
            k=0
            while k<len(arr[0]):
                i,j=x+arr[0][k],y+arr[1][k]
                if i>=0 and i<8 and j>=0 and j<8 and ((self.grid.getGrid()[i][j]==None) or (self.grid.getGrid()[i][j]!=None and (self.grid.getGrid()[i][j].getName()[1] is not self.grid.getGrid()[x][y].getName()[1]))) and self.valid_move([x,y],[i,j]): 
                    self.highlight(i,j)
                    places.append([i,j])
                k+=1

            if not (self.check_w or self.king_w or self.rook_w_l) and self.grid.grid[1][7]==None and self.grid.grid[2][7]==None and self.grid.grid[3][7]==None and self.valid_move([4,7],[2,7]):
                self.highlight(2,7)
                places.append([2,7])
            if not (self.check_w or self.king_w or self.rook_w_r) and self.grid.grid[5][7]==None and self.grid.grid[6][7]==None and self.valid_move([4,7],[6,7]):
                self.highlight(6,7)
                places.append([6,7])
            if not (self.check_b or self.king_b or self.rook_b_l) and self.grid.grid[1][0]==None and self.grid.grid[2][0]==None and self.grid.grid[3][0]==None and self.valid_move([4,0],[2,0]):
                self.highlight(2,0)
                places.append([2,0])
            if not (self.check_b or self.king_b or self.rook_b_r) and self.grid.grid[5][0]==None and self.grid.grid[6][0]==None and self.valid_move([4,0],[6,0]):
                self.highlight(6,0)
                places.append([6,0])
        #print(places,clickedPiece.getName(),"showHint")
        return places

    def check(self,x,y,checkType):
        #print("call check")
        places=[]
        arr=None
        if checkType is "straight":
            arr=[[1,-1,0,0],[0,0,1,-1]]
        else:
            arr=[[1,1,-1,-1],[1,-1,1,-1]]
        k=0
        while k<4:
            i,j=x+arr[0][k],y+arr[1][k]
            while i>=0 and i<8 and j>=0 and j<8 and self.grid.getGrid()[i][j]==None:
                #print(i,j,"check")
                if self.valid_move([x,y],[i,j]):
                    self.highlight(i,j)
                    places.append([i,j])
                i+=arr[0][k]
                j+=arr[1][k]
            if i>=0 and i<8 and j>=0 and j<8 and self.grid.getGrid()[i][j]!=None and (self.grid.getGrid()[i][j].getName()[1] is not self.grid.getGrid()[x][y].getName()[1] and self.valid_move([x,y],[i,j])):
                self.highlight(i,j)
                places.append([i,j])
            k+=1
        return places

    
    def check_for_check(self,player):
        flag=0
        for i in range(8):
            for j in range(8):
                if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player and self.grid.grid[i][j].name is "King":
                    x=i
                    y=j
                    flag=1
                    break
            if flag==1:
                break
        flag=0
        for i in range(x+1,8):
            if self.grid.grid[i][y]!=None and self.grid.grid[i][y].player is player:
                break
            elif self.grid.grid[i][y]!=None and self.grid.grid[i][y].player is not player and (self.grid.grid[i][y].name is "Rook" or self.grid.grid[i][y].name is "Queen"):
                return True
            elif self.grid.grid[i][y]!=None and self.grid.grid[i][y].player is not player and not (self.grid.grid[i][y].name is "Rook" or self.grid.grid[i][y].name is "Queen"):
                break
        for i in range(x-1,-1,-1):
            if self.grid.grid[i][y]!=None and self.grid.grid[i][y].player is player:
                break
            elif self.grid.grid[i][y]!=None and self.grid.grid[i][y].player is not player and (self.grid.grid[i][y].name is "Rook" or self.grid.grid[i][y].name is "Queen"):
                return True
            elif self.grid.grid[i][y]!=None and self.grid.grid[i][y].player is not player and not (self.grid.grid[i][y].name is "Rook" or self.grid.grid[i][y].name is "Queen"):
                break
        for j in range(y+1,8):
            if self.grid.grid[x][j]!=None and self.grid.grid[x][j].player is player:
                break
            elif self.grid.grid[x][j]!=None and self.grid.grid[x][j].player is not player and (self.grid.grid[x][j].name is "Rook" or self.grid.grid[x][j].name is "Queen"):
                return True
            elif self.grid.grid[x][j]!=None and self.grid.grid[x][j].player is not player and not (self.grid.grid[x][j].name is "Rook" or self.grid.grid[x][j].name is "Queen"):
                break
        for j in range(y-1,-1,-1):
            if self.grid.grid[x][j]!=None and self.grid.grid[x][j].player is player:
                break
            elif self.grid.grid[x][j]!=None and self.grid.grid[x][j].player is not player and (self.grid.grid[x][j].name is "Rook" or self.grid.grid[x][j].name is "Queen"):
                return True
            elif self.grid.grid[x][j]!=None and self.grid.grid[x][j].player is not player and not (self.grid.grid[x][j].name is "Rook" or self.grid.grid[x][j].name is "Queen"):
                break
        
        i=x+1
        j=y+1
        while i<8 and j<8:
            if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player:
                break
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                return True
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and not (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                break
            i+=1
            j+=1

        i=x-1
        j=y+1
        while i>=0 and j<8:
            if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player:
                break
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                return True
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and not (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                break
            i-=1
            j+=1
           
        i=x+1
        j=y-1
        while i<8 and j>=0:
            if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player:
                break
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                return True
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and not (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                break
            i+=1
            j-=1

        i=x-1
        j=y-1
        while i>=0 and j>=0:
            if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player:
                break
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                return True
            elif self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is not player and not (self.grid.grid[i][j].name is "Bishop" or self.grid.grid[i][j].name is "Queen"):
                break
            i-=1
            j-=1
        
        if self.isValid(x-1,y-2) and self.grid.grid[x-1][y-2]!=None and self.grid.grid[x-1][y-2].player is not player and self.grid.grid[x-1][y-2].name is "Knight":
            return True
        if self.isValid(x-2,y-1) and self.grid.grid[x-2][y-1]!=None and self.grid.grid[x-2][y-1].player is not player and self.grid.grid[x-2][y-1].name is "Knight":
            return True
        if self.isValid(x+1,y-2) and self.grid.grid[x+1][y-2]!=None and self.grid.grid[x+1][y-2].player is not player and self.grid.grid[x+1][y-2].name is "Knight":
            return True
        if self.isValid(x+2,y-1) and self.grid.grid[x+2][y-1]!=None and self.grid.grid[x+2][y-1].player is not player and self.grid.grid[x+2][y-1].name is "Knight":
            return True
        if self.isValid(x-1,y+2) and self.grid.grid[x-1][y+2]!=None and self.grid.grid[x-1][y+2].player is not player and self.grid.grid[x-1][y+2].name is "Knight":
            return True
        if self.isValid(x-2,y+1) and self.grid.grid[x-2][y+1]!=None and self.grid.grid[x-2][y+1].player is not player and self.grid.grid[x-2][y+1].name is "Knight":
            return True
        if self.isValid(x+1,y+2) and self.grid.grid[x+1][y+2]!=None and self.grid.grid[x+1][y+2].player is not player and self.grid.grid[x+1][y+2].name is "Knight":
            return True
        if self.isValid(x+2,y+1) and self.grid.grid[x+2][y+1]!=None and self.grid.grid[x+2][y+1].player is not player and self.grid.grid[x+2][y+1].name is "Knight":
            return True
        
        if self.grid.grid[x][y]!=None and self.grid.grid[x][y].player is "White" and ((self.isValid(x-1,y-1) and self.grid.grid[x-1][y-1]!=None and self.grid.grid[x][y].player!=self.grid.grid[x-1][y-1].player and self.grid.grid[x-1][y-1].name is "Pawn") or (self.isValid(x+1,y-1) and self.grid.grid[x+1][y-1]!=None and self.grid.grid[x][y].player!=self.grid.grid[x+1][y-1].player and self.grid.grid[x+1][y-1].name is "Pawn")):
            return True
        if self.grid.grid[x][y]!=None and self.grid.grid[x][y].player is "Black" and ((self.isValid(x+1,y+1) and self.grid.grid[x+1][y+1]!=None and self.grid.grid[x][y].player!=self.grid.grid[x+1][y+1].player and self.grid.grid[x+1][y+1].name is "Pawn") or (self.isValid(x-1,y+1) and self.grid.grid[x-1][y+1]!=None and self.grid.grid[x][y].player!=self.grid.grid[x-1][y+1].player and self.grid.grid[x-1][y+1].name is "Pawn")):
            return True

        if self.isValid(x-1,y-1) and self.grid.grid[x-1][y-1]!=None and self.grid.grid[x-1][y-1].player is not player and self.grid.grid[x-1][y-1].name is "King":
            return True
        if self.isValid(x-1,y) and self.grid.grid[x-1][y]!=None and self.grid.grid[x-1][y].player is not player and self.grid.grid[x-1][y].name is "King":
            return True
        if self.isValid(x-1,y+1) and self.grid.grid[x-1][y+1]!=None and self.grid.grid[x-1][y+1].player is not player and self.grid.grid[x-1][y+1].name is "King":
            return True
        if self.isValid(x,y-1) and self.grid.grid[x][y-1]!=None and self.grid.grid[x][y-1].player is not player and self.grid.grid[x][y-1].name is "King":
            return True
        if self.isValid(x,y+1) and self.grid.grid[x][y+1]!=None and self.grid.grid[x][y+1].player is not player and self.grid.grid[x][y+1].name is "King":
            return True
        if self.isValid(x+1,y-1) and self.grid.grid[x+1][y-1]!=None and self.grid.grid[x+1][y-1].player is not player and self.grid.grid[x+1][y-1].name is "King":
            return True
        if self.isValid(x+1,y) and self.grid.grid[x+1][y]!=None and self.grid.grid[x+1][y].player is not player and self.grid.grid[x+1][y].name is "King":
            return True
        if self.isValid(x+1,y+1) and self.grid.grid[x+1][y+1]!=None and self.grid.grid[x+1][y+1].player is not player and self.grid.grid[x+1][y+1].name is "King":
            return True
        
        return False

    def valid_move(self,oldPosition,newPosition):
        if self.grid.grid[oldPosition[0]][oldPosition[1]].name=="King" and abs(newPosition[0]-oldPosition[0])==2:
            p1=self.grid.grid[oldPosition[0]][oldPosition[1]]
            p2=self.grid.grid[newPosition[0]][newPosition[1]]
            if newPosition==[2,7]:
                p3=self.grid.grid[0][7]
                p4=self.grid.grid[3][7]
                self.grid.grid[0][7]=None
                self.grid.grid[3][7]=self.grid.grid[0][7]
                t=self.check_for_check(self.getTurn())
                self.grid.grid[0][7]=p3
                self.grid.grid[3][7]=p4
            elif newPosition==[6,7]:
                p3=self.grid.grid[7][7]
                p4=self.grid.grid[5][7]
                self.grid.grid[7][7]=None
                self.grid.grid[5][7]=self.grid.grid[7][7]
                t=self.check_for_check(self.getTurn())
                self.grid.grid[7][7]=p3
                self.grid.grid[5][7]=p4
            elif newPosition==[2,0]:
                p3=self.grid.grid[0][0]
                p4=self.grid.grid[3][0]
                self.grid.grid[0][0]=None
                self.grid.grid[3][0]=self.grid.grid[0][0]
                t=self.check_for_check(self.getTurn())
                self.grid.grid[0][0]=p3
                self.grid.grid[3][0]=p4
            else:
                p3=self.grid.grid[7][0]
                p4=self.grid.grid[5][0]
                self.grid.grid[7][0]=None
                self.grid.grid[5][0]=self.grid.grid[7][0]
                t=self.check_for_check(self.getTurn())
                self.grid.grid[7][0]=p3
                self.grid.grid[5][0]=p4
        else:    
            p1=self.grid.grid[oldPosition[0]][oldPosition[1]]
            p2=self.grid.grid[newPosition[0]][newPosition[1]]
            self.grid.grid[oldPosition[0]][oldPosition[1]]=None
            self.grid.grid[newPosition[0]][newPosition[1]]=p1
            t=self.check_for_check(self.getTurn())
            self.grid.grid[oldPosition[0]][oldPosition[1]]=p1
            self.grid.grid[newPosition[0]][newPosition[1]]=p2
        return not t

    def newPiece(self,turn,x,y,chess,gameDisplay):
        if ((turn is "White" and y==0) or (turn is "Black" and y==7)) and self.grid.grid[x][y].name is "Pawn":
            if turn is "White":
                t="1"
            else:
                t="2"
            gameDisplay.fill((200,200,200))
            drawDeadPiece()
            chess.displayGrid()
            pygame.display.update()
            time.sleep(0.5)
            start=300
            pygame.draw.rect(gameDisplay,(200,200,200),(start,250,230,70))
            image = load_image("Rook"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+5
            imagerect.top = 255
            gameDisplay.blit(image,imagerect)
            image = load_image("Knight"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+55
            imagerect.top = 255
            gameDisplay.blit(image,imagerect)
            image = load_image("Bishop"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+105
            imagerect.top = 255
            gameDisplay.blit(image,imagerect)
            image = load_image("Queen"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+165
            imagerect.top = 255
            gameDisplay.blit(image,imagerect)
            pygame.draw.rect(gameDisplay,black,(start,250,230,70),1)
            pygame.draw.rect(gameDisplay,black,(start,250,57,70),1)
            pygame.draw.rect(gameDisplay,black,(start+57,250,52,70),1)
            pygame.draw.rect(gameDisplay,black,(start+109,250,57,70),1)
            pygame.draw.rect(gameDisplay,black,(start+166,250,64,70),1)
            flag=0
            while True:
                for event in pygame.event.get():
                    position=pygame.mouse.get_pos()
                    #print(position)
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if position[1]>=250 and position[1]<=320:
                            if position[0]>=start and position[0]<=start+57:
                                p="Rook"
                                flag=1
                                break
                            elif position[0]>=start+57 and position[0]<=start+109:
                                p="Knight"
                                flag=1
                                break
                            elif position[0]>=start+109 and position[0]<=start+166:
                                p="Bishop"
                                flag=1
                                break
                            elif position[0]>=start+166 and position[0]<=start+230:
                                p="Queen"
                                flag=1
                                break
                    if position[1]>=250 and position[1]<=320:
                        if not(position[0]>=start and position[0]<=start+57):
                            pygame.draw.rect(gameDisplay,black,(start,250,57,70),1)
                        if not(position[0]>=start+57 and position[0]<=start+109):
                            pygame.draw.rect(gameDisplay,black,(start+57,250,52,70),1)
                        if not(position[0]>=start+109 and position[0]<=start+166):
                            pygame.draw.rect(gameDisplay,black,(start+109,250,57,70),1)
                        if not(position[0]>=start+166 and position[0]<=start+230):
                            pygame.draw.rect(gameDisplay,black,(start+166,250,64,70),1)

                    if position[1]>=250 and position[1]<=320:
                        if position[0]>=start and position[0]<=start+57:
                            pygame.draw.rect(gameDisplay,red,(start,250,57,70),1)
                        if position[0]>=start+57 and position[0]<=start+109:
                            pygame.draw.rect(gameDisplay,red,(start+57,250,52,70),1)
                        if position[0]>=start+109 and position[0]<=start+166:
                            pygame.draw.rect(gameDisplay,red,(start+109,250,57,70),1)
                        if position[0]>=start+166 and position[0]<=start+230:
                            pygame.draw.rect(gameDisplay,red,(start+166,250,64,70),1)
                                    
                pygame.display.update()
                if flag==1:
                    break

            piece=Piece(x,y,p,turn)
            self.grid.grid[x][y]=piece

    def no_moves(self,player):
        for i in range(8):
            for j in range(8):
                #if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player:
                    #print("\n"*4)
                    #print(self.grid.grid[i][j].name,i,j,self.showHint(i,j))
                if self.grid.grid[i][j]!=None and self.grid.grid[i][j].player is player and self.showHint(i,j)!=[]:
                    return False
        return True

    def stalemate(self):
        count=0
        for i in range(8):
            for j in range(8):
                if self.grid.grid[i][j]!=None:
                    count+=1
        if count==2:
            return True
        return False
        
    def isValid(self,x,y):
        if x<0 or x>=8 or y<0 or y>=8:
            return False
        return True

    def monitor_castelling_conditions(self,x,y):
        if x==0:
            if y==0:
                self.rook_b_l=True
            if y==7:
                self.rook_w_l=True
        if x==7:
            if y==0:
                self.rook_b_r=True
            if y==7:
                self.rook_w_r=True

    def monitor_castelling_conditions1(self,turn):
        if turn is "White":
            self.check_w=True
        else:
            self.check_b=True

    def monitor_castelling_conditions2(self,turn):
        if turn is "White":
            self.king_w=True
        else:
            self.king_b=True
                           
    def highlight(self,x,y):
         pygame.draw.rect(gameDisplay,red,(x*(height)/8+(width-height)/2,y*(height)/8+topMenu,(height)/8,(height)/8),3)

    def dehighlight(self,places):
        if places!=None:
            for place in places:
                pygame.draw.rect(gameDisplay,white,(place[0]*(height)/8+(width-height)/2,place[1]*(height)/8+topMenu,(height)/8,(height)/8),3)

    def displayGrid(self):
        self.grid.displayGrid()


try:
    while True:
        deadWhite=[[],[]]
        deadBlack=[[],[]]
        chess=Chess()
        moveState="None"
        gameDisplay.fill((200,200,200))
        chess.displayGrid()
        places=[]
        d={"White":"Black","Black":"White"}
        while True:
            gameOver=False
            for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        gameExit=True
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        position=pygame.mouse.get_pos()
                        x=int((position[0]-(width-height)/2)//(height/8))
                        y=int(position[1]//(height/8)+topMenu)
                        if chess.isValid(x,y):
                            if moveState is "None" and chess.correct_player(x,y):
                                oldPosition=[x,y]
                                places=chess.showHint(x,y)
                                #print(places,"places")
                                moveState="Hint"
                            elif moveState is "Hint":
                                if [x,y] in places:
                                    chess.monitor_castelling_conditions(oldPosition[0],oldPosition[1])
                                    if chess.grid.grid[oldPosition[0]][oldPosition[1]].name is "King":
                                        chess.monitor_castelling_conditions2(chess.getTurn())
                                    chess.removePiece(x,y)
                                    chess.movePiece(oldPosition,[x,y])                
                                    chess.newPiece(chess.getTurn(),x,y,chess,gameDisplay)
                                    chess.toggle_turn()
                                    #print(chess.check_for_check(chess.getTurn()),chess.no_moves(chess.getTurn()))
                                    if chess.check_for_check(chess.getTurn()):
                                        chess.monitor_castelling_conditions1(chess.getTurn())
                                        if not chess.no_moves(chess.getTurn()):
                                            drawtext('Check!!!', font, gameDisplay, 240, 200)
                                            pygame.display.update()
                                            time.sleep(0.5)
                                            gameDisplay.fill((200,200,200))
                                            drawDeadPiece()
                                            chess.displayGrid()
                                            pygame.display.update()
                                    if chess.no_moves(chess.getTurn()):
                                        gameDisplay.fill((200,200,200))
                                        drawDeadPiece()
                                        chess.displayGrid()
                                        if chess.check_for_check(chess.getTurn()):
                                            drawtext('CheckMate!!!', font, gameDisplay, 240, 200)
                                            drawtext('%s Wins'%(d[chess.getTurn()]), font, gameDisplay, 240, 260)
                                        else:
                                            drawtext('Stalemate!!!', font, gameDisplay, 240, 200)
                                            drawtext('Match Draw', font, gameDisplay, 240, 260)
                                        pygame.display.update()
                                        gameOver=True
                                        break
                                    if chess.stalemate():
                                        gameDisplay.fill((200,200,200))
                                        drawDeadPiece()
                                        chess.displayGrid()
                                        drawtext('Stalemate!!!', font, gameDisplay, 240, 200)
                                        drawtext('Match Draw', font, gameDisplay, 240, 260)
                                        pygame.display.update()
                                        gameOver=True
                                        break
                                        
                                gameDisplay.fill((200,200,200))
                                drawDeadPiece()
                                chess.displayGrid()
                                moveState="None"
                                if [x,y] not in places and chess.isValid(x,y) and chess.correct_player(x,y):
                                    oldPosition=[x,y]
                                    places=chess.showHint(x,y)
                                    moveState="Hint"

            #drawtext('%s White %s Black' %(chess.check_for_check("White"),chess.check_for_check("Black")), font, gameDisplay, 350, 300)                
            
            pygame.display.update()
            #print(gameOver)
            if gameOver:
                break
            
        time.sleep(2)
        flag=0
        start=300
        pygame.draw.rect(gameDisplay,(200,200,200),(start,250,230,70))
        pygame.draw.rect(gameDisplay,black,(start,250,230,70),1)
        drawtext('Play Again?', font1, gameDisplay, start+50, 250)
        pygame.draw.rect(gameDisplay,black,(start+10,280,65,30),1)
        drawtext('Yes', font1, gameDisplay, start+20, 275)
        pygame.draw.rect(gameDisplay,black,(start+175,280,45,30),1)
        drawtext('No', font1, gameDisplay, start+185, 275)
        pygame.display.update()
        while True:
            b=0
            for event in pygame.event.get():
                position=pygame.mouse.get_pos()
                #print(position)
                if position[1]>=280 and position[1]<=310:
                    if not(position[0]>=start+10 and position[0]<=start+65):
                        pygame.draw.rect(gameDisplay,black,(start+10,280,65,30),1)
                    if not(position[0]>=start+175 and position[0]<=start+220):
                        pygame.draw.rect(gameDisplay,black,(start+175,280,45,30),1)
                if position[1]>=280 and position[1]<=310:
                    if position[0]>=start+10 and position[0]<=start+65:
                        pygame.draw.rect(gameDisplay,red,(start+10,280,65,30),1)
                    if position[0]>=start+175 and position[0]<=start+220:
                        pygame.draw.rect(gameDisplay,red,(start+175,280,45,30),1)
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if position[1]>=280 and position[1]<=310:
                        if position[0]>=start+10 and position[0]<=start+65:
                            flag=1
                            b=1
                            break
                        if position[0]>=start+175 and position[0]<=start+220:
                            flag=0
                            b=1
                            break
                pygame.display.update()
            if b==1:
                break
        if flag==0:
            break
except:
    print("Error!!!")
pygame.quit()
quit()
