#!/usr/bin/python2
import pygame
from pygame.locals import *
from sys import exit

SCREENSIZE=(600,600)
BACKGROUNDCOLOR=(255,255,255)
SELECTEDCOLOR=(200,200,200)
PlacedTextColor=(0,0,0)
SolvedTextColor=(255,0,0)
LineColor=(0,0,0)

def CheckMissplacements():
    #checks if the numbers is correctly placed on the board so the solving can begin. e.g. There must not be the same number in the same block, row or collum twice.
#    return 0 if no errors, 1 if error in blocks, 2 if error in rows, and 3 if error in collums
    #Check the blocks
    for x in range(3):
        for y in range(3):
            Blocknumbers=[]
            for i in range(3):
                for j in range (3):
                    Blocknumbers.append(BoardNumbers[3*x+i][3*y+j])
            for l in range(10):
                if (Blocknumbers.count(l)>1):
                    
                    return (1,l,x,y,Blocknumbers.index(l))
    # Check Rows
    for x in range(9):
        Rownumbers=[]
        for y in range(9):
            Rownumbers.append(BoardNumbers[x][y])
        for l in range(10):
            if (Rownumbers.count(l)>1):
                return (2,l,x,y,Rownumbers.index(l))
    #Check Collums            
    for y in range(9):
        Collumnumbers=[]
        for x in range(9):
            Collumnumbers.append(BoardNumbers[x][y])
        for l in range(10):
            if (Collumnumbers.count(l)>1):
                return (3,l,y,x,Collumnumbers.index(l))
                
    return 0

def DrawBoard(Solver=-1):
    screen.fill(BACKGROUNDCOLOR)
    #Color the selected field
    pygame.draw.rect(screen,SELECTEDCOLOR,pygame.Rect((SelectedField[0]*SCREENSIZE[0]/9,SelectedField[1]*SCREENSIZE[1]/9),(SCREENSIZE[1]/9+1,SCREENSIZE[0]/9+1)))
        #Draw lines vertical and horizontal, every third should be wider to mark the big and small grid.
    for x in range(8):
        if ((x+1)%3==0):
            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]),3)
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[0])/9*(x+1)),3)
        else:
        
            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]))
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[0])/9*(x+1)))
    
    #Draw numbers on board
    for x in range(9):
        for y in range(9):
            text=font.render(str(BoardNumbers[x][y]),True,PlacedTextColor)
            screen.blit(text,(int(float(SCREENSIZE[0])/9*(x+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*(y+0.5)-text.get_height() / 2)))
            #print int(float(SCREENSIZE[0])/9*(x+0.5)-text.get_width() / 2)
            #print int(float(SCREENSIZE[0])/9*(y+0.5)-text.get_height() / 2)
    if Solver==-1:
        #do Nothing
        print ""
    elif Solver==0:
        font2=  pygame.font.SysFont("Times New Roman", SCREENSIZE[0]/8)     
        text= font2.render("Solving the Board..",True,(0,0,255))
        screen.blit(text,(SCREENSIZE[0]/2 -text.get_width() / 2, SCREENSIZE[1]/2 - text.get_height() /2))
    elif Solver[0]==1:
        #error in block, mark the error red
        text=font.render(str(Solver[1]),True,(255,0,0))
        
        screen.blit(text,(int(float(SCREENSIZE[0])/9*((3*Solver[2]+Solver[4]/3)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*((3*Solver[3]+Solver[4]%3)+0.5)-text.get_height() / 2)))
        
    elif Solver[0]==2:
        #Error in Row. Mark error red
        text=font.render(str(Solver[1]),True,(255,0,0))
        screen.blit(text,(int(float(SCREENSIZE[0])/9*((Solver[2])+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*((Solver[4])+0.5)-text.get_height() / 2)))
    elif Solver[0]==3:
        #Error in Collum. Mark error red
        text=font.render(str(Solver[1]),True,(255,0,0))
        screen.blit(text,(int(float(SCREENSIZE[0])/9*((Solver[4])+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*((Solver[2])+0.5)-text.get_height() / 2)))
        
        
    pygame.display.flip()
    
pygame.init()
screen=pygame.display.set_mode(SCREENSIZE,0,32)
font = pygame.font.SysFont("Times New Roman", SCREENSIZE[0]/12)
SelectedField=(0,0)
BoardNumbers=[[""]*9 for i in range(9)]
DrawBoard()
Enterpressed=0
while 1:


    #Eventquoue
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
            
        elif event.type==KEYDOWN:
            if event.key==K_1:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=1
            elif event.key==K_2:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=2
            elif event.key==K_3:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=3
            elif event.key==K_4:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=4
            elif event.key==K_5:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=5
            elif event.key==K_6:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=6
            elif event.key==K_7:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=7
            elif event.key==K_8:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=8
            elif event.key==K_9:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=9
            elif event.key==K_DELETE:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=""
            elif event.key==K_RETURN:
                Ready=CheckMissplacements() 
                print Ready #debug
                DrawBoard(Ready)     #Some remains to be written
                Enterpressed=1
                if Ready==0:
                    DrawSolvedBoard(SolveBoard()) #remains to be written
                    
            if Enterpressed==0:
                DrawBoard()
            Enterpressed=0
            
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                #There seems to be a small slip in field selection. Should be fixed at some point
                print event.pos #debug
                #print ("Field number="+str(int(float(event.pos[0])/SCREENSIZE[0]*9))+","+str(int(float(event.pos[1])/SCREENSIZE[1]*9))) #debug
                SelectedField=(int(float(event.pos[0])/SCREENSIZE[0]*9),int(float(event.pos[1])/SCREENSIZE[1]*9))
                DrawBoard()
            
    
    #DrawBoard()
            
    
