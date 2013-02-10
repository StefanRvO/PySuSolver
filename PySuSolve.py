#!/usr/bin/python2
import pygame
from pygame.locals import *
from sys import exit

SCREENSIZE=(500,500)
BACKGROUNDCOLOR=(255,255,255)
SELECTEDCOLOR=(200,200,200)
PlacedTextColor=(0,0,0)
SolvedTextColor=(255,0,0)
LineColor=(0,0,0)
def CheckMissplacements(Board,Solver=0):
    #checks if the numbers is correctly placed on the board so the solving can begin. e.g. There must not be the same number in the same block, row or collum twice.
#    return 0 if no errors, 1 if error in blocks, 2 if error in rows, and 3 if error in collums
    #Check the blocks
    for x in xrange(3):
        for y in xrange(3):
            Blocknumbers=[]
            #for i in range(3):
            #    for j in range (3):
            if Solver==0:
                #Blocknumbers.append(Board[3*x+i][3*y+j])
                Blocknumbers=[Board[3*x+0][3*y+0],Board[3*x+0][3*y+1],Board[3*x+0][3*y+2],Board[3*x+1][3*y+0],Board[3*x+1][3*y+1],Board[3*x+1][3*y+2],Board[3*x+2][3*y+0],Board[3*x+2][3*y+1],Board[3*x+2][3*y+2]] #This is ugly, but hopefully more effective than .append()

            else:
                #Blocknumbers.append(Board[(3*x+i)*9+(3*y+j)][0])
                Blocknumbers=[Board[(3*x+0)*9+(3*y+0)][0],Board[(3*x+0)*9+(3*y+1)][0],Board[(3*x+0)*9+(3*y+2)][0],Board[(3*x+1)*9+(3*y+0)][0],Board[(3*x+1)*9+(3*y+1)][0],Board[(3*x+1)*9+(3*y+2)][0],Board[(3*x+2)*9+(3*y+0)][0],Board[(3*x+2)*9+(3*y+1)][0],Board[(3*x+2)*9+(3*y+2)][0]]
            for l in xrange(1,10):
                if (Blocknumbers.count(l)>1):
                    if(Solver==0):
                        return (1,l,x,y,Blocknumbers.index(l))
                    else:
                        return -1
    # Check Rows
    for x in xrange(9):
        Rownumbers=[]
        #for y in range(9):
        if Solver==0:
            #Rownumbers.append(Board[x][y])
            Rownumbers=[Board[x][0],Board[x][1],Board[x][2],Board[x][3],Board[x][4],Board[x][5],Board[x][6],Board[x][7],Board[x][8]]
        else:
            #Rownumbers.append(Board[x*9+y][0])
            Rownumbers=[Board[x*9+0][0],Board[x*9+1][0],Board[x*9+2][0],Board[x*9+3][0],Board[x*9+4][0],Board[x*9+5][0],Board[x*9+6][0],Board[x*9+7][0],Board[x*9+8][0]]
        for l in xrange(1,10):
            if (Rownumbers.count(l)>1):
                if (Solver==0):
                    return (2,l,x,y,Rownumbers.index(l))
                else:
                    return -1
    #Check Collums
    for y in xrange(9):
        Collumnumbers=[]
        #for x in range(9):
        if Solver==0:
            #Collumnumbers.append(Board[x][y])
            Coullumnumbers=[Board[0][y],Board[1][y],Board[2][y],Board[3][y],Board[4][y],Board[5][y],Board[6][y],Board[7][y],Board[8][y]]
        else:
            #Collumnumbers.append(Board[x*9+y][0])
            Collumnumbers=[Board[0*9+y][0],Board[1*9+y][0],Board[2*9+y][0],Board[3*9+y][0],Board[4*9+y][0],Board[5*9+y][0],Board[6*9+y][0],Board[7*9+y][0],Board[8*9+y][0]]
        for l in xrange(1,10):
            if (Collumnumbers.count(l)>1):
                if Solver==0:
                    return (3,l,y,x,Collumnumbers.index(l))
                else:
                    return -1

    return 0

def FillPossible(Board):
    #Fill in naked singles and makes a list of possible values for each cell
    Possible=[""]*81
    Changed=0
    Check=1
    while Check==1:
        Check=0
        for i in range(81):
            if Board[i][1]==1:
                Possible[i]=[Board[i][0]]
            else:
                Possible[i]=[]
                for j in range(1,10):
                    Board[i][0]=j
                    if not CheckMissplacements(Board,1)==-1:
                        Possible[i].append(j)
                if len(Possible[i])==1:
                    Board[i][0]=Possible[i][0]
                    Board[i][1]=1
                    Check=1
                    Changed=1
                else:
                    Board[i][0]=""
    return (Possible,Changed)

def FindHiddenSingles(Possible,Board):
    #Check each row, collumn and block, and if a number only is candidate in one cell, it means that it must be that cell
    #Blocks:
    Changed=0
    for x in range(3):
        for y in range(3):
            for num in range(1,10): #check each number in this block
                cellList=[]
                for i in range(3):
                    for j in range(3):
                        if Possible[(3*x+i)*9+(3*y+j)].count(num)==1:
                            cellList.append((3*x+i)*9+(3*y+j))
                if len(cellList)==1:
                    if Board[cellList[0]][0]=="":
                        Board[cellList[0]][0]=num
                        Board[cellList[0]][1]=1
                        Changed=1
                        #print "blok, num :"+str(num)+" celle "+str(cellList[0])
    #rows
    for x in range(9):
        for num in range(1,10):
            cellList=[]
            for y in range(9):
                if Possible[x*9+y].count(num)==1:
                    cellList.append(x*9+y)
            if len(cellList)==1:
                if Board[cellList[0]][0]=="":
                    Board[cellList[0]][0]=num
                    Board[cellList[0]][1]=1
                    Changed=1
                    #print "raekke, num :"+str(num)+" celle"+str(cellList[0])
    #Collumns
    for y in range(9):
        for num in range(1,10):
            cellList=[]
            for x in range(9):
                if Possible[x*9+y].count(num)==1:
                    cellList.append(x*9+y)
            if len(cellList)==1:
                if Board[cellList[0]][0]=="":
                    Board[cellList[0]][0]=num
                    Board[cellList[0]][1]=1
                    Changed=1
                    #print "kollone, num :"+str(num)+" celle"+str(cellList[0])
    return Changed

def FindNakedSingles(PossibleList,Board):
    Changed=0
    for i in range(81):
        if not Board[i][1]==1:
            if len(PossibleList[i])==1: #We have found a naked single
                Changed=1
                Board[i][0]=PossibleList[i][0]
                Board[i][1]=1
    return Changed
                    
                            
def FindNakedPairsTripplesQuads(PossibleList):
    #If two cells in a group (row, collum, block) contains the same two candidates, these candidates can be removed from the rest of the cells in the group
    #loop through all cells, searching for a cell with two candidates
    Changed=0
    for checking in range(2,5):
        for i in range(81):
            if len(PossibleList[i])==checking:
                current=PossibleList[i]
                #if we find one, search through block, row and collum for the same pair.
                row=i%9
                collumn=i/9
                #search through row
                cellList=[i]
                for l in range(9):
                    if not row+l*9==i:
                        numbersfound=0
                        for candidate in current:
                            if PossibleList[row+l*9].count(candidate)>0:
                                numbersfound+=1
                        if numbersfound==len(PossibleList[row+l*9]):
                            cellList.append(row+l*9)
                       
                if len(cellList)==checking: #we have found a naked pair/tripple/quad.
                    for l in range(9):
                        if not cellList.count(row+l*9)>0: #check if we should delete in this cell
                            for candidate in current:
                                if PossibleList[row+l*9].count(candidate)==1:
                                    PossibleList[row+l*9].remove(candidate)
                                    Changed=1
                #search through collumn
                cellList=[i]
                for l in range(9):
                    if not collumn*9+l==i:
                        numbersfound=0
                        for candidate in current:
                            if PossibleList[collumn*9+l].count(candidate)>0:
                                numbersfound+=1
                        if numbersfound==len(PossibleList[collumn*9+l]):
                            cellList.append(collumn*9+l)
                        
                if len(cellList)==checking: #we have found a naked pair/tripple/quad.
                    for l in range(9):
                        if not cellList.count(collumn*9+l)>0: #check if we should delete in this cell
                            for candidate in current:
                                if PossibleList[collumn*9+l].count(candidate)==1:
                                    PossibleList[collumn*9+l].remove(candidate)
                                    Changed=1
                #search through blocks
                cellList=[i]
                    #find out whick block we belongs to
                blockX=collumn/3
                blockY=row/3
                for x in range(3):
                    for y in range(3):
                        if not (blockX*3+x)*9+(blockY*3+y)==i:
                            numbersfound=0
                            for candidate in current:
                                if PossibleList[(blockX*3+x)*9+(blockY*3+y)].count(candidate)>0:
                                    numbersfound+=1
                            if numbersfound==len(PossibleList[(blockX*3+x)*9+(blockY*3+y)]):
                                cellList.append((blockX*3+x)*9+(blockY*3+y))
                            
                if len(cellList)==checking: #we have found a naked pair/tripple/quad.
                    for x in range(3):
                        for y in range(3):
                            if not cellList.count((blockX*3+x)*9+(blockY*3+y))>0:
                                for candidate in current:
                                    if PossibleList[(blockX*3+x)*9+(blockY*3+y)].count(candidate)==1:
                                        PossibleList[(blockX*3+x)*9+(blockY*3+y)].remove(candidate)
                                        Changed=1
    return Changed                              
    
def FindHiddenPairs(PossibleList):
    #This find cells in unit, where to cells are the only ones to contain two specific candidates
    Changed=0
    #Find in collumns
    for x in range(9):
        numlist=[[],[]]
        for num in range(1,10):
            cellList=[]
            for y in range(9):
                if PossibleList[x*9+y].count(num)==1:
                    cellList.append(x*9+y)
            if len(cellList)==2:
                numlist[1].append(cellList)
                numlist[0].append(1)
            else:
                numlist[1].append("")
                numlist[0].append(0)
        for i in range(9):
            if numlist[0][i]:
                current=numlist[1][i]
                for l in range(9):
                    if numlist[1][l]==current and not l==i: #We found a hidden pair. These candidates are the only ones which share a pair
                        if not (PossibleList[numlist[1][i][0]]==[l+1,i+1] and PossibleList[numlist[1][i][1]]==[l+1,i+1]):
                            PossibleList[numlist[1][i][0]]=[l+1,i+1]
                            PossibleList[numlist[1][i][1]]=[l+1,i+1]
                            Changed=1
    #find in rows 
    for y in range(9):
        numlist=[[],[]]
        for num in range(1,10):
            cellList=[]
            for x in range(9):
                if PossibleList[x*9+y].count(num)==1:
                    cellList.append(x*9+y)
            if len(cellList)==2:
                numlist[1].append(cellList)
                numlist[0].append(1)
            else:
                numlist[1].append("")
                numlist[0].append(0)
        for i in range(9):
            if numlist[0][i]:
                current=numlist[1][i]
                for l in range(9):
                    if numlist[1][l]==current and not l==i: #We found a hidden pair. These candidates are the only ones which share a pair
                        if not (PossibleList[numlist[1][i][0]]==[l+1,i+1] and PossibleList[numlist[1][i][1]]==[l+1,i+1]):
                            PossibleList[numlist[1][i][0]]=[l+1,i+1]
                            PossibleList[numlist[1][i][1]]=[l+1,i+1]
                            Changed=1
    #Find in Blocks
    for x in range(3):
        for y in range(3):
            numlist=[[],[]]
            for num in range(1,10): #check each number in this block
                cellList=[]
                for i in range(3):
                    for j in range(3):
                        if PossibleList[(3*x+i)*9+(3*y+j)].count(num)==1:
                            cellList.append((3*x+i)*9+(3*y+j))
                if len(cellList)==2:
                    numlist[1].append(cellList)
                    numlist[0].append(1)
                else:
                    numlist[1].append("")
                    numlist[0].append(0)
            for i in range(9):
                if numlist[0][i]:
                    current=numlist[1][i]
                    for l in range(9):
                        if numlist[1][l]==current and not l==i: #We found a hidden pair. These candidates are the only ones which share a pair
                            if not (PossibleList[numlist[1][i][0]]==[l+1,i+1] and PossibleList[numlist[1][i][1]]==[l+1,i+1]):
                                PossibleList[numlist[1][i][0]]=[l+1,i+1]
                                PossibleList[numlist[1][i][1]]=[l+1,i+1]
                                Changed=1
    return Changed
                           
                            
def FindHiddenTrippels(PossibleList):
    pass
    #May Be implemented in the future


def FindHiddenQuads(PossibleList):
    pass
    #May Be Implemented in the future
def FindPointingPairs(PossibleList):
    #If a candidate value inside a box only exists in one row or collumn, it can be removed from the same row or collumn in other boxes.
    #Not currently working
    Changed=0
    for x in range(3):
        for y in range(3):
            for num in range(1,10):
                CellList=[]
                for i in range(3):
                    for j in range(3):
                        if PossibleList[(3*x+i)*9+(3*y+j)].count(num)==1:
                            CellList.append((3*x+i,3*y+j))
                if len(CellList)==3 or len(CellList)==2:
                    #Check if number exist only in the same row or collumn
                    SameRow=1
                    SameCollumn=1
                    row=CellList[0][0]
                    collumn=CellList[0][1]
                    
                    for cell in CellList[1:]:
                        if not cell[0]==row:
                            SameRow=0
                        if not cell[1]==collumn:
                            SameCollumn=0
                    if SameRow: #if the candidate only exist in the same row, delete candidate in the rest of the row
                        #Get coullmns we shouldn't delete in
                        skipThese=[]
                        for cell in CellList:
                            skipThese.append(cell[1])
                        #Delete in all others
                        for thiscollumn in range(9):
                            if not skipThese.count(thiscollumn)==1:
                                if PossibleList[row*9+thiscollumn].count(num)==1:
                                    PossibleList[row*9+thiscollumn].remove(num)
                                    Changed=1
                        #print "Pointing Pair at:"
                        #for cell in CellList:
                        #    print cell
                        #print "Nummer="+str(num)
                    elif SameCollumn: #if the candidate only exist in the same row, delete candidate in the rest of the row
                        skipThese=[]
                        for cell in CellList:
                            skipThese.append(cell[0])
                        #Delete in all others
                        for thisrow in range(9):
                            if not skipThese.count(thisrow)==1:
                                if PossibleList[thisrow*9+collumn].count(num)==1:
                                    PossibleList[thisrow*9+collumn].remove(num)
                                    Changed=1
                        #print "Pointing Pair at:"
                        #for cell in CellList:
                        #    print cell
                        #print "Nummer="+str(num)
    return Changed
                         
                        
            
def PrepareBoard(Board):
    possible=FillPossible(Board)
    PossibleList=possible[0]
    while True:
        while True:
            naked=FindNakedSingles(PossibleList,Board)
            hidden=FindHiddenSingles(PossibleList,Board)
            DrawSolvingBoard(PossibleList)
            #SolvingBoard=checker[0]
            print "naked : "+str(naked)
            print "CrossCheck: "+str(hidden)
            
            if not (hidden==1 or naked==1):
                break
            else:
                    possible=FillPossible(Board)
                    PossibleList=possible[0]
        while True:
            TempPossibleList=PossibleList[:]
            NakedGroups=FindNakedPairsTripplesQuads(PossibleList)
            HiddenPairs=FindHiddenPairs(PossibleList)
            HiddenPairs=0 #Workaround for buggy change detection, should be fixed
            PointingPairs=FindPointingPairs(PossibleList) #Should Be Working
            FindHiddenTrippels(PossibleList) #Not implemented, does nothing
            FindHiddenQuads(PossibleList) #Not implemented, does nothing
            print "NakedGroups :"+str(NakedGroups)
            print "HiddenPairs :"+str(HiddenPairs)
            print "PointingPairs :"+str(PointingPairs)
            if not (NakedGroups==1 or HiddenPairs==1 or PointingPairs==1):
                break
        naked=FindNakedSingles(PossibleList,Board)
        hidden=FindHiddenSingles(PossibleList,Board)
        DrawSolvingBoard(PossibleList)
        if not(hidden==1 or naked==1):
            break
        else:
                possible=FillPossible(Board)
                PossibleList=possible[0]
        
            
    for i in range(9):
        print PossibleList[(i*9):((i+1)*9)]
        
    print ""
    print Board
    return(Board,PossibleList)
    
def CheckFaultyBoard(PossibleList):
    for candidates in PossibleList:
        if len(candidates)==0:
            return -1
    
    return 0





def SolveBoard():
    Solved=0
    #Here we solve the board
    #We use bruteforce for now. May be optimised later when working
    #first we copy boardnumbers
    SolvingBoard=[""]*81
    for i in range(9):
        for j in range(9):
            if not BoardNumbers[i][j]=="":
                SolvingBoard[i*9+j]=[BoardNumbers[i][j],1,0]
            else:
                SolvingBoard[i*9+j]=["",0,0]


#We have now copied in the entered board. Solvingboard is now of a list of list.
#The list contains the following:
#[0] contains the value of the cell
#[1] Contains either the numbers 0 or 1
#0 means we should not edit this cell. These are the cells entered by the user, 0 means we are alowed to edit the cell
#We have also reformated it a bit. It is now one-dimensional. This makes things a bit easier later on.
#[2] contains the candidate which is currently active
    #We prepare for bruteforce.
    #We find some easy cells and make a list of candidates for each cell
    Temp=PrepareBoard(SolvingBoard)
    PossibleList=Temp[1]
    SolvingBoard=Temp[0] 
    if (CheckFaultyBoard(PossibleList)==-1): #check if a cell have no candidate
        return -1
    
    #brute force part
    #Here we use brute force to solve for the remaining cells.
    
    



    #Now we make a loop.
    CurrentCell=-1
    BackStepped=0
    LastNotValid=0
    Jumps=0
    while True:
        #print SolvingBoard
        Jumps+=1
        if Jumps%200==0:
            DrawSolvingBoard(SolvingBoard,1) #For fancy graphics and the lulz
        while True: #add 1 to currentcell, and keep doing to we come to a uncertain cell
            CurrentCell+=1
            if CurrentCell>80:
                #return, the board is now solved
                #print SolvingBoard
                SolvingBoard.append(Jumps)
                return SolvingBoard
                
            if SolvingBoard[CurrentCell][1]==0: #break incrementing loop if we reach an unsolved cell
                break
        SolvingBoard[CurrentCell][2]=0
        SolvingBoard[CurrentCell][0]=PossibleList[CurrentCell][SolvingBoard[CurrentCell][2]]
        while True:
            if BackStepped: #we have just stepped a cell back. try the next candidate for the cell
                BackStepped=0
                if not SolvingBoard[CurrentCell][0]==PossibleList[CurrentCell][-1]: #check if we are at last candidate
                    SolvingBoard[CurrentCell][2]+=1
                    SolvingBoard[CurrentCell][0]=PossibleList[CurrentCell][SolvingBoard[CurrentCell][2]]
                else:
                    LastNotValid=1
            if CheckMissplacements(SolvingBoard,1)==-1 or LastNotValid: #if cell don't fit, or we tried this before, we try the next possible value for the cell
                LastNotValid=0
                SolvingBoard[CurrentCell][2]+=1
                if not SolvingBoard[CurrentCell][2]+1 > len(PossibleList[CurrentCell]):
                    SolvingBoard[CurrentCell][0]=PossibleList[CurrentCell][SolvingBoard[CurrentCell][2]]
                else: #if we have tried all possibilities, go back to next unsolved cell
                    SolvingBoard[CurrentCell][0]=""
                    while True:
                        CurrentCell-=1
                        BackStepped=1
                        if CurrentCell<0:
                            return -1 #Board could not be solved
                        if not SolvingBoard[CurrentCell][1]==1:
                            break
            else: #break if cell fits
                break
      







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
        pass
    elif Solver==0:
        font2=  pygame.font.SysFont("Times New Roman", SCREENSIZE[0]/10)
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
    elif Solver[0]==4: #To few numbers entered
        font2=  pygame.font.SysFont("Times New Roman", SCREENSIZE[0]/12)
        text= font2.render("You only entered "+str(Solver[1])+" numbers",True,(255,0,0))
        text2= font2.render("You need to enter at least 16!",True,(255,0,0))
        screen.blit(text,(SCREENSIZE[0]/2 -text.get_width() / 2, SCREENSIZE[1]/2 - text.get_height()))
        screen.blit(text2,(SCREENSIZE[0]/2 -text2.get_width() / 2, SCREENSIZE[1]/2 + text2.get_height()/2))


    pygame.display.flip()

def DrawSolvedBoard(Board):
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

    if Board==-1: #We could not solve the board

        font2=  pygame.font.SysFont("Times New Roman", SCREENSIZE[0]/8)
        text= font2.render("Could not Solve",True,(255,0,0))
        screen.blit(text,(SCREENSIZE[0]/2 -text.get_width() / 2, SCREENSIZE[1]/2 - text.get_height() /2))
    else:
        #Draw the solved board.
        #user-entered values should be black, solved values should be blue
        for i in range(81):
            #make the text
            text=font.render(str(Board[i][0]),True,(0,0,255)) #make blue
            #Draw
            screen.blit(text,(int(float(SCREENSIZE[0])/9*((i/9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_height() / 2)))
            #Draw userentered numbers black
        for x in range(9):
            for y in range(9):
                text=font.render(str(BoardNumbers[x][y]),True,PlacedTextColor)
                screen.blit(text,(int(float(SCREENSIZE[0])/9*(x+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*(y+0.5)-text.get_height() / 2)))
    pygame.display.flip()

def DrawSolvingBoard(PossibleList, Mode=0):
    screen.fill(BACKGROUNDCOLOR)
        #Draw Lines
    for x in range(8):
        if ((x+1)%3==0):
            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]),3)
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[0])/9*(x+1)),3)
        else:

            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]))
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[0])/9*(x+1)))
    #Draw Numbers
    if Mode==0:
        for i in range(81):
            if len(PossibleList[i])==1:
                #make the text
                text=font.render(str(PossibleList[i][0]),True,(0,0,0)) #make black
                #Draw
                screen.blit(text,(int(float(SCREENSIZE[0])/9*((i/9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_height() / 2)))
    elif Mode==1:
        for i in range(81):
            #make the text
            if PossibleList[i][1]==1:
                text=font.render(str(PossibleList[i][0]),True,(0,0,0)) #make black if constant
            else:
                text=font.render(str(PossibleList[i][0]),True,(0,0,255)) #make blue if variable
            #Draw
            screen.blit(text,(int(float(SCREENSIZE[0])/9*((i/9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_height() / 2)))
    pygame.display.flip()
    

pygame.init()
screen=pygame.display.set_mode(SCREENSIZE,0,32)
font = pygame.font.SysFont("Times New Roman", SCREENSIZE[0]/12)
SelectedField=[0,0]
BoardNumbers=[[""]*9 for i in range(9)]
DrawBoard()
Enterpressed=0
clock=pygame.time.Clock()
while 1:


    #Eventquoue
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()

        elif event.type==KEYDOWN:
            if event.key in (K_1, K_KP1) :
                BoardNumbers[SelectedField[0]][SelectedField[1]]=1
            elif event.key in (K_2, K_KP2):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=2
            elif event.key in (K_3, K_KP3):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=3
            elif event.key in (K_4, K_KP4):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=4
            elif event.key in (K_5, K_KP5):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=5
            elif event.key in (K_6, K_KP6):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=6
            elif event.key in (K_7, K_KP7):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=7
            elif event.key in (K_8, K_KP8):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=8
            elif event.key in (K_9, K_KP9):
                BoardNumbers[SelectedField[0]][SelectedField[1]]=9
            elif event.key==K_DELETE:
                BoardNumbers[SelectedField[0]][SelectedField[1]]=""
            elif event.key==K_UP:
                if not SelectedField[1]==0:
                    SelectedField[1]-=1
                else:
                    SelectedField[1]=8
            elif event.key==K_DOWN:
                if not SelectedField[1]==8:
                    SelectedField[1]+=1
                else:
                    SelectedField[1]=0
            elif event.key==K_LEFT:
                if not SelectedField[0]==0:
                    SelectedField[0]-=1
                else:
                    SelectedField[0]=8
            elif event.key==K_RIGHT:
                if not SelectedField[0]==8:
                    SelectedField[0]+=1
                else:
                    SelectedField[0]=0
            elif event.key==K_c: #This clears the board
                BoardNumbers=[[""]*9 for i in range(9)]
            elif event.key in (K_RETURN, K_KP_ENTER):
                Ready=CheckMissplacements(BoardNumbers,0)
                #count number of entered numbers, we have to have at least 16 (comment out if you want to solve anyway!)
                numbers=[]
                for i in range(9):
                    for j in range(9):
                        numbers.append(BoardNumbers[i][j])
                enteredNumbers=81-numbers.count("")
                #if enteredNumbers<=-1:
                #    Ready=(4,enteredNumbers)
                #print Ready #debug
                DrawBoard(Ready)
                Enterpressed=1
                if Ready==0:
                    #print SolveBoard()
                   SolvedBoard=SolveBoard()
                   DrawSolvedBoard(SolvedBoard)
                   #print SolvedBoard
                   if not SolvedBoard==-1:                  
                       print  SolvedBoard[-1]
            elif event.key==K_l: #Load from a seed file
                try:
                    file=open('seedfile','r')
                except IOError:
                    break #File does not exist
                BoardNumbers=[[""]*9 for i in range(9)]
                current=0
                while True:
                    thischar=file.read(1)
                    if thischar=="" or current>80:
                        break   #Break if we reach end of file
                    if thischar in ('0','1','2','3','4','5','6','7','8','9','.'):
                        row=current%9
                        collumn=current/9
                        if not thischar in ('.','0'):
                            BoardNumbers[row][collumn]=int(thischar)
                        else:
                            BoardNumbers[row][collumn]=""
                        current+=1
                       
                            
                        
                        
                    

            if Enterpressed==0:
                DrawBoard()
            Enterpressed=0


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:

                #print event.pos #debug
                #print ("Field number="+str(int(float(event.pos[0])/SCREENSIZE[0]*9))+","+str(int(float(event.pos[1])/SCREENSIZE[1]*9))) #debug
                SelectedField=[int(float(event.pos[0])/SCREENSIZE[0]*9),int(float(event.pos[1])/SCREENSIZE[1]*9)]
                DrawBoard()

    clock.tick(60)


