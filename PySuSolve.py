#!/usr/bin/python2
import sys
import random


SCREENSIZE = (600, 600)
FONTUSED = "Times New Roman"
ScaleFont = 1 #Used to scale the font a bit if the different fonts are slightly different in size. 1 fits to times new roman
BACKGROUNDCOLOR = (255, 255, 255)
SELECTEDCOLOR = (200, 200, 200)
PlacedTextColor = (0, 0, 0)
LogicSolveColor = (255, 165, 0)
BruteSolveColor=(0, 0, 255)
LineColor=(0, 0, 0)
ErrorColor=(255, 0, 0)
#Font size should be choosen from the smallest dimension of the screen
if SCREENSIZE[0] > SCREENSIZE[1]:
    FONTBASIS = SCREENSIZE[1]
else:
    FONTBASIS = SCREENSIZE[0]

def ChooseSolvingAlgorithm(CurrentState):
    #Show an dialog box where the user can choose which solving algorithm(s) to use
    #Currentstate is a list with the current choosen values.
    #Returns a list with the new values
    master=Tkinter.Tk()
    master.title("Algorithms")
    for i in range(8):
        CurrentState[i]=Tkinter.IntVar(master=master,value=CurrentState[i])
        
    Tkinter.Label(master,text="Which solving algorithm(s)\nshould be used").grid(row=0,sticky=Tkinter.W) #Title, left alligned (sticky is allignment, W is west
    Tkinter.Checkbutton(master,text="Find Candidates\n (With out this, only bruteforce will work)",variable=CurrentState[0]).grid(row=1,sticky=Tkinter.W) #With this as zero, only burteforcing will work. all cells will have all candidates (unless they are user-entered)
    Tkinter.Checkbutton(master,text="Find Naked Singles",variable=CurrentState[1]).grid(row=2,sticky=Tkinter.W) #find naked singles?
    Tkinter.Checkbutton(master,text="Find Hidden Singles",variable=CurrentState[2]).grid(row=3,sticky=Tkinter.W) #find hidden singles?
    Tkinter.Checkbutton(master,text="Find Naked Pairs, Tripples or Quads",variable=CurrentState[3]).grid(row=4,sticky=Tkinter.W)
    Tkinter.Checkbutton(master,text="Find Hidden Pairs",variable=CurrentState[4]).grid(row=5,sticky=Tkinter.W)
    Tkinter.Checkbutton(master,text="Find Pointing Pairs",variable=CurrentState[5]).grid(row=6,sticky=Tkinter.W)
    Tkinter.Checkbutton(master,text="Use guessing Bruteforce",variable=CurrentState[6]).grid(row=7,sticky=Tkinter.W)
    Tkinter.Checkbutton(master,text="Use regular (dumb) Bruteforce",variable=CurrentState[7]).grid(row=8,sticky=Tkinter.W)
    Tkinter.Button(master,text="Ok",command=master.quit).grid(row=9)
    master.mainloop()
    for i in range(8):
        CurrentState[i]=CurrentState[i].get()
    master.withdraw()
    return CurrentState    
def GetKeyEventsWSolving():
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()

        elif event.type==KEYDOWN:
            if event.key ==K_ESCAPE:
                print "Canceled"
                return -1
    return 0
    
    

def CheckMissplacements(Board, Solver = 0):
    #checks if the numbers is correctly placed on the board so the solving can begin. e.g. There must not be the same number in the same block, row or collum twice.
#    return 0 if no errors, 1 if error in blocks, 2 if error in rows, and 3 if error in collums.
    #If the second argument given is 1,we return -1 on error
    #Check the blocks
    for x in xrange(3):
        for y in xrange(3):
            Blocknumbers=[]
            for i in range(3):
                for j in range (3):
                    if Solver == 0:
                        Blocknumbers.append(Board[(3*x+i)*9+(3*y+j)])

                    else:
                        Blocknumbers.append(Board[(3*x+i)*9+(3*y+j)][0])
            for l in xrange(1,10):
                if (Blocknumbers.count(l) > 1):
                    if(Solver == 0):
                        return (1, l, x, y, Blocknumbers.index(l))
                    else:
                        return -1
    # Check Rows
    for x in xrange(9):
        Rownumbers = []
        for y in range(9):
            if Solver == 0:
                Rownumbers.append(Board[x*9+y])

            else:
                Rownumbers.append(Board[x*9+y][0])

        for l in xrange(1,10):
            if (Rownumbers.count(l) > 1):
                if (Solver == 0):
                    return (2, l, x, y, Rownumbers.index(l))
                else:
                    return -1
    #Check Collums
    for y in xrange(9):
        Collumnumbers = []
        for x in range(9):
            if Solver == 0:
                Collumnumbers.append(Board[x*9+y])

            else:
                Collumnumbers.append(Board[x*9+y][0])
        for l in xrange(1,10):
            if (Collumnumbers.count(l) > 1):
                if Solver == 0:
                    return (3, l, y, x, Collumnumbers.index(l))
                else:
                    return -1

    return 0

def FillCandidates(Board):
    #Fill in naked singles and makes a list of possible values for each cell
    PossibleList=[""] * 81

    for i in range(81):
        if not Board[i][0] =="":
            PossibleList[i] = [Board[i][0]]
        else:
            PossibleList[i] = []
            for j in range(1,10):
                Board[i][0] = j
                if not CheckMissplacements(Board,1) == -1:
                    PossibleList[i].append(j)
            if len(PossibleList[i]) == 1:
                Board[i][0] = PossibleList[i][0]
                Board[i][1] = 1
            else:
                Board[i][0] = ""
    return (PossibleList)

def FindHiddenSingles(PossibleList,Board,Draw=1):
    #Check each row, collumn and block, and if a number only is candidate in one cell, it means that it must be that cell
    #Blocks:
    Changed = 0
    for x in range(3):
        for y in range(3):
            for num in range(1, 10): #check each number in this block
                cellList = []
                for i in range(3):
                    for j in range(3):
                        if PossibleList[(3*x+i)*9+(3*y+j)].count(num) == 1:
                            cellList.append((3*x+i)*9+(3*y+j))
                if len(cellList) == 1:
                    if Board[cellList[0]][0] == "":
                        Board[cellList[0]][0] = num
                        Board[cellList[0]][1] = 1
                        PossibleList[cellList[0]] = [num]
                        Changed = 1
                        if Graphics and Draw:
                            DrawSolvingBoard(PossibleList)
                        #print "blok, num :"+str(num)+" celle "+str(cellList[0])
    #rows
    for x in range(9):
        for num in range(1,10):
            cellList = []
            for y in range(9):
                if PossibleList[x*9+y].count(num) == 1:
                    cellList.append(x*9+y)
            if len(cellList) == 1:
                if Board[cellList[0]][0] == "":
                    Board[cellList[0]][0] = num
                    Board[cellList[0]][1] = 1
                    PossibleList[cellList[0]] = [num]
                    Changed = 1
                    if Graphics and Draw:
                        DrawSolvingBoard(PossibleList)
                    #print "raekke, num :"+str(num)+" celle"+str(cellList[0])
    #Collumns
    for y in range(9):
        for num in range(1,10):
            cellList = []
            for x in range(9):
                if PossibleList[x*9+y].count(num) == 1:
                    cellList.append(x*9+y)
            if len(cellList) == 1:
                if Board[cellList[0]][0] == "":
                    Board[cellList[0]][0] = num
                    Board[cellList[0]][1] = 1
                    PossibleList[cellList[0]] = [num]
                    Changed = 1
                    if Graphics and Draw:
                        DrawSolvingBoard(PossibleList)

                    #print "kollone, num :"+str(num)+" celle"+str(cellList[0])
    return Changed

def FindNakedSingles(PossibleList,Board,Draw=1):
    check = 1
    Changed = 0
    while check == 1:
        check = 0
        for i in range(81):
            if not Board[i][1] == 1:
                if len(PossibleList[i]) == 1: #We have found a naked single
                    Changed = 1
                    Board[i][0] = PossibleList[i][0]
                    Board[i][1] = 1
                    Changed = 1
                    check = 1
                    if Graphics and Draw:
                        DrawSolvingBoard(PossibleList)
    return Changed


def FindNakedPairsTripplesQuads(PossibleList):
    #If two cells in a group (row, collum, block) contains the same two candidates, these candidates can be removed from the rest of the cells in the group
    #loop through all cells, searching for a cell with two candidates
    Changed=0
    for checking in range(2,5):
        for i in range(81):
            if len(PossibleList[i]) == checking:
                current = PossibleList[i]
                #if we find one, search through block, row and collum for the same pair.
                row = i%9
                collumn = i/9
                #search through row
                cellList = [i]
                for l in range(9):
                    if not row+l*9 == i:
                        numbersfound = 0
                        for candidate in current:
                            if PossibleList[row+l*9].count(candidate) > 0:
                                numbersfound += 1
                        if numbersfound == len(PossibleList[row+l*9]):
                            cellList.append(row+l*9)

                if len(cellList) == checking: #we have found a naked pair/tripple/quad.
                    for l in range(9):
                        if not cellList.count(row+l*9) > 0: #check if we should delete in this cell
                            for candidate in current:
                                if PossibleList[row+l*9].count(candidate) == 1:
                                    PossibleList[row+l*9].remove(candidate)
                                    Changed = 1
                #search through collumn
                cellList = [i]
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



def PrepareBoard(Board1,Draw = 1):
    #Make a copy of Board1 and put in board (this is neccesary for our bruteforcing
    Board=[]
    for i in range(81):
        Board.append([])
        for l in range (3):
            Board[i].append(Board1[i][l])
    if CurrentState[0]:
        PossibleList=FillCandidates(Board)
    else:
        #We fill all non-user entered cells with all candidates
        PossibleList=[""]*81
        for i in range(81):
            if Board[i][1] == 1:
                PossibleList[i] = [Board[i][0]]
            else:
                PossibleList[i] = [1,2,3,4,5,6,7,8,9]
    while True:
        while True:
            if Graphics and GetKeyEventsWSolving()==-1:
                return -2
            if CurrentState[1]:
                naked=FindNakedSingles(PossibleList,Board,Draw)
            else:
                naked=0
            if CurrentState[2]:
                hidden=FindHiddenSingles(PossibleList,Board,Draw)
            else:
                hidden=0
            #SolvingBoard=checker[0]
            if Verbose:
                if CurrentState[1]:
                    print "naked : "+str(naked)
                if CurrentState[2]:
                    print "CrossCheck: "+str(hidden)

            if not (hidden==1 or naked==1):
                break
            else:
                if CurrentState[0]:
                    PossibleList=FillCandidates(Board)
        while True:
            #copy PossibleList to tempboard
            TempList=[]
            for cell in range(len(PossibleList)):
                TempList.append([])
                for l in range(len(PossibleList[cell])):
                    TempList[cell].append(PossibleList[cell][l])
            if CurrentState[3]:        
                NakedGroups=FindNakedPairsTripplesQuads(PossibleList)
            else:
                NakedGroups=0
            if CurrentState[4]:    
                HiddenPairs=FindHiddenPairs(PossibleList)
            else:
                HiddenPairs=0
            if CurrentState[5]:
                PointingPairs=FindPointingPairs(PossibleList) #Should Be Working
            else:
                PointingPairs=0
            #FindHiddenTrippels(PossibleList) #Not implemented, does nothing
            #FindHiddenQuads(PossibleList) #Not implemented, does nothing
            if  (TempList==PossibleList):
                break
            else:
                if Verbose:
                    print "Found Naked or Hidden groups or pointing pairs"
                if Graphics and Draw:
                    DrawSolvingBoard(PossibleList)
        if CurrentState[1]:
            naked=FindNakedSingles(PossibleList,Board,Draw)
        else:
            naked=0
        if CurrentState[2]:
            hidden=FindHiddenSingles(PossibleList,Board,Draw)
        else:
            hidden=0
        if Verbose:
            if CurrentState[1]:
                print "naked : "+str(naked)
            if CurrentState[2]:
                print "CrossCheck: "+str(hidden)
        if not(hidden==1 or naked==1):
            break
        else:
            if CurrentState[0]:        
                PossibleList=FillCandidates(Board)



    #for i in range(9):
    #    print PossibleList[(i*9):((i+1)*9)]

    #print ""
    #print Board
    return(Board,PossibleList)

def CheckFaultyBoard(PossibleList):
    for candidates in PossibleList:
        if len(candidates)==0:
            return -1

    return 0

def BruteForceRandom(PossibleList,SolvingBoard):
    #This is a specialised bruteforce. We select a random nonsolved field.
    #At this field we fill in the first candidate.
    #We try to solve using logic. If it fails we move on to the next candidate and tries again.
    #If we can't solve with any of the candidates, we select another field and does the same, but now with both fields.
    #We do this only down to 5 levels. It is probabaly ore effective to use the standard bruteforce if we haven't solved at this point
    #(5 levels really means ~5^5= tries
    #A list containing the cells we are trying on
    

    testing=0
    CellList=[]
    for i in range(5):
        while True:
            RandomCell=random.randint(0,80)
            if not SolvingBoard[RandomCell][1]==1 or RandomCell in CellList:
                CellList.append(RandomCell)
                break
    
    #We have now selected the cells to try on
    
                
    for candidate0 in [""]+PossibleList[CellList[0]]:
        SolvingBoard[CellList[0]][0]=candidate0
        if not candidate0=="":
            SolvingBoard[CellList[0]][1]=1
        for candidate1 in [""]+PossibleList[CellList[1]]:
            SolvingBoard[CellList[1]][0]=candidate1
            if not candidate1=="":
               SolvingBoard[CellList[1]][1]=1
            for candidate2 in [""]+PossibleList[CellList[2]]:
                SolvingBoard[CellList[2]][0]=candidate2
                if not candidate2=="":
                    SolvingBoard[CellList[2]][1]=1
                for candidate3 in [""]+PossibleList[CellList[3]]:
                    SolvingBoard[CellList[3]][0]=candidate3
                    if not candidate3=="":
                        SolvingBoard[CellList[3]][1]=1
                    for candidate4 in PossibleList[CellList[4]]:
                        SolvingBoard[CellList[4]][0]=candidate4
                        SolvingBoard[CellList[4]][1]=1
                        TempList=PrepareBoard(SolvingBoard,0)
                        print SolvingBoard==TempList
                        testing+=1
                        DrawSolvingBoard(PossibleList,SolvingBoard,TempList[0],0,CellList)
                        print "Try number " +str(testing)
                        if testing>30: #may change this number.. Trying is taking too long. return and try with some other values
                            for i in range(5):
                                SolvingBoard[CellList[i]][0]=""
                                SolvingBoard[CellList[i]][1]=0
                            return -3
                        if TempList==-2:
                            for i in range(5):
                                SolvingBoard[CellList[i]][0]=""
                                SolvingBoard[CellList[i]][1]=0
                            return -2
                        Solved=1
                        for tempcell in TempList[0]:
                            if tempcell[0]=="":
                                Solved=0
                                print "error"
                                break
                        if Solved and not CheckMissplacements(TempList[0],1)==-1:
                            print "solved"
                            TempList[0].append(testing)
                            return TempList[0]
    for i in range(5):
        SolvingBoard[CellList[i]][0]=""
        SolvingBoard[CellList[i]][1]=0
                       
    return -1               
def BruteForce(PossibleList,SolvingBoard):
#    print PossibleList
#    print SolvingBoard
    CurrentCell=-1
    BackStepped=0
    LastNotValid=0
    Jumps=0
    while True:
        Jumps+=1
        if Jumps%200==0:
            if Graphics:
                DrawSolvingBoard(PossibleList,SolvingBoard) #For fancy graphics and the lulz
                if(GetKeyEventsWSolving()==-1): #Cancel event occured
                    return -2
            if Verbose:
                print "Jumps = "+str(Jumps)
        while True: #add 1 to currentcell, and keep doing to we come to a uncertain cell
            CurrentCell+=1
            if CurrentCell>80:
                #return, the board is now solved
                #Return jumps too
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
            #print CheckMissplacements(SolvingBoard,1)
            #print SolvingBoard
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


def SolveBoard(Board):
    Solved=0
    #Here we solve the board
    #We use bruteforce for now. May be optimised later when working
    #first we copy boardnumbers
    SolvingBoard=[""]*81
    for i in range(81):
            if not BoardNumbers[i]=="":
                SolvingBoard[i]=[BoardNumbers[i],1,0]
            else:
                SolvingBoard[i]=["",0,0]
    #print SolvingBoard


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
    if Temp==-2:
        return -2
    PossibleList=Temp[1]
    SolvingBoard=Temp[0]
    if (CheckFaultyBoard(PossibleList)==-1): #check if a cell have no candidate
        return -1
    #Check if we are done solving
    Solved=1
    for cell in SolvingBoard:
        if cell[0]=="":
            Solved=0
            break
            
    if Solved:
        SolvingBoard.append(0)
        return SolvingBoard
    #brute force part
    #Here we use brute force to solve for the remaining cells.
    if CurrentState[6]:
        tries=-30
        SolvedBoard=-3
        while SolvedBoard==-3: #it took too long, try to call again, and keep doing so. (We should maybe stop if we have called it a certain numbe of times, or let it run to end after some tries)
            tries+=30
            SolvedBoard=BruteForceRandom(PossibleList,SolvingBoard)
        if not SolvedBoard in (-1,-2):
            SolvedBoard[-1]+=tries
            return SolvedBoard

            
            
    if CurrentState[7]:
        SolvedBoard=BruteForce(PossibleList,SolvingBoard)
    if not 1 in CurrentState[6:]:
        if Solved:
            return SolvingBoard
        else:
            return -1
        
    return SolvedBoard



def GenerateBoard(difficulty):
    random.seed()
    #This function generates a sudoku board #It is not garanteed to have an unique solution
    #First we fill up the candidate list with all candidates
    CandidateList=[]
    for i in range(81):
        CandidateList.append([1,2,3,4,5,6,7,8,9])
    #Then we randomize the list for each cell
    for i in range(81):
        random.shuffle(CandidateList[i])
    SolvingBoard=[]
    for i in range(81):
        SolvingBoard.append(["",0,0])

    GeneratedBoard=BruteForce(CandidateList,SolvingBoard)
    if not GeneratedBoard==-1:
    #    print GeneratedBoard[-1]
        Temp=[""]*81
        for i in range(81):
            Temp[i]=GeneratedBoard[i][0]
        GeneratedBoard=Temp
    #Now we remove cells until the board only contains the number of cells specified in difficulty
    while True:
        GeneratedBoard[random.randint(0,80)]=""


        filled=0
        for i in range(81):
            if GeneratedBoard[i] in (1,2,3,4,5,6,7,8,9):
                filled+=1
        if filled<=difficulty:
            break
    return GeneratedBoard









def DrawBoard(Board,Solver=-1):
    screen.fill(BACKGROUNDCOLOR)
    #Color the selected field
    pygame.draw.rect(screen,SELECTEDCOLOR,pygame.Rect((SelectedField[0]*SCREENSIZE[0]/9,SelectedField[1]*SCREENSIZE[1]/9),(SCREENSIZE[0]/9+1,SCREENSIZE[1]/9+1)))
        #Draw lines vertical and horizontal, every third should be wider to mark the big and small grid.
    for x in range(8):
        if ((x+1)%3==0):
            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]),3)
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[1])/9*(x+1)),3)
        else:

            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]))
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[1])/9*(x+1)))

    #Draw numbers on board
    for i in range(81):
            text=font.render(str(Board[i]),True,PlacedTextColor)
            screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
            #print int(float(SCREENSIZE[0])/9*(x+0.5)-text.get_width() / 2)
            #print int(float(SCREENSIZE[0])/9*(y+0.5)-text.get_height() / 2)
    if Solver==-1:
        #do Nothing
        pass
    elif Solver==0:
        font2=  pygame.font.SysFont(FONTUSED, int(ScaleFont*float(FONTBASIS)/10))
        text= font2.render("Solving the Board..",True,BruteSolveColor)
        screen.blit(text,(SCREENSIZE[0]/2 -text.get_width() / 2, SCREENSIZE[1]/2 - text.get_height() /2))
    elif Solver[0]==1:
        #error in block, mark the error red
        text=font.render(str(Solver[1]),True,ErrorColor)

        screen.blit(text,(int(float(SCREENSIZE[0])/9*((3*Solver[3]+Solver[4]%3)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((3*Solver[2]+Solver[4]/3)+0.5)-text.get_height() / 2)))

    elif Solver[0]==2:
        #Error in Row. Mark error red
        text=font.render(str(Solver[1]),True,ErrorColor)
        screen.blit(text,(int(float(SCREENSIZE[0])/9*((Solver[4])+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((Solver[2])+0.5)-text.get_height() / 2)))
    elif Solver[0]==3:
        #Error in Collum. Mark error red
        text=font.render(str(Solver[1]),True,ErrorColor)
        screen.blit(text,(int(float(SCREENSIZE[0])/9*((Solver[2])+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((Solver[4])+0.5)-text.get_height() / 2)))
    elif Solver[0]==4: #To few numbers entered
        font2=  pygame.font.SysFont(FONTUSED, int(ScaleFont*float(FONTBASIS)/12))
        text= font2.render("You only entered "+str(Solver[1])+" numbers",True,ErrorColor)
        text2= font2.render("You need to enter at least 16!",True,ErrorColor)
        screen.blit(text,(SCREENSIZE[0]/2 -text.get_width() / 2, SCREENSIZE[1]/2 - text.get_height()))
        screen.blit(text2,(SCREENSIZE[0]/2 -text2.get_width() / 2, SCREENSIZE[1]/2 + text2.get_height()/2))


    pygame.display.flip()

def DrawSolvedBoard(solvedBoard,enteredBoard):
    screen.fill(BACKGROUNDCOLOR)
    #Color the selected field
    pygame.draw.rect(screen,SELECTEDCOLOR,pygame.Rect((SelectedField[0]*SCREENSIZE[0]/9,SelectedField[1]*SCREENSIZE[1]/9),(SCREENSIZE[0]/9+1,SCREENSIZE[1]/9+1)))
        #Draw lines vertical and horizontal, every third should be wider to mark the big and small grid.
    for x in range(8):
        if ((x+1)%3==0):
            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]),3)
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[1])/9*(x+1)),3)
        else:

            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]))
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[1])/9*(x+1)))

    if solvedBoard==-1: #We could not solve the board

        font2=  pygame.font.SysFont(FONTUSED, int(ScaleFont*float(FONTBASIS)/8))
        text= font2.render("Could not Solve",True,(255,0,0))
        screen.blit(text,(SCREENSIZE[0]/2 -text.get_width() / 2, SCREENSIZE[1]/2 - text.get_height() /2))
    elif solvedBoard==-2: #Solving was canceled
        DrawBoard(enteredBoard)
        return 0
    else:
        #Draw the solved board.
        #user-entered values should be black, logicsolved values should be orange, bruteforce values should be blue
        for i in range(81):
            #make the text
            if solvedBoard[i][1]==1:
                text=font.render(str(solvedBoard[i][0]),True,LogicSolveColor) #make orange
            else:
                text=font.render(str(solvedBoard[i][0]),True,BruteSolveColor) #make blue
            #Draw
            screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
            #Draw userentered numbers black
        for i in range(81):
                text=font.render(str(enteredBoard[i]),True,PlacedTextColor)
                screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
    pygame.display.flip()

def DrawSolvingBoard(PossibleList,Board=0,TempBoard=0,DrawPossible=1,BruteList=0):
    if TempBoard==0:
        TempBoard=Board
    screen.fill(BACKGROUNDCOLOR)
    candidatefont = pygame.font.SysFont(FONTUSED, int(ScaleFont*float(FONTBASIS)/28))
        #Draw Lines
    for x in range(8):
        if ((x+1)%3==0):
            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]),3)
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[1])/9*(x+1)),3)
        else:

            pygame.draw.line(screen, LineColor,(float(SCREENSIZE[0])/9*(x+1),0),(float(SCREENSIZE[0])/9*(x+1),SCREENSIZE[1]))
            pygame.draw.line(screen, LineColor,(0,float(SCREENSIZE[1])/9*(x+1)),(SCREENSIZE[0],float(SCREENSIZE[1])/9*(x+1)))
    #Draw Numbers
    if Board==0 and Board==TempBoard:
        for i in range(81):
            if len(PossibleList[i])==1:
                #make the text
                text=font.render(str(PossibleList[i][0]),True,LogicSolveColor) #make orange
                #Draw
                screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
            elif not len(PossibleList[i])==0:
                #draw the possible candidates
                if DrawPossible:
                    for candidate in PossibleList[i]:
                        text=candidatefont.render(str(candidate),True,LogicSolveColor)

                        screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9))+float(SCREENSIZE[0])/27*((candidate-1)%3+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9))+float(SCREENSIZE[1])/27*((candidate-1)/3+0.5)-text.get_height() / 2)))
    elif not Board==TempBoard:
        for i in range(81):
            #make the text
            if Board[i][1]==TempBoard[i][1] and not i in BruteList:
                text=font.render(str(Board[i][0]),True,LogicSolveColor) #make orange if constant
            elif not TempBoard[i][0]=="":
                text=font.render(str(TempBoard[i][0]),True,BruteSolveColor) #make blue if variable
            #else:
            #    #draw the possible candidates
            #    for candidate in PossibleList[i]:
            #        text=candidatefont.render(str(candidate),True,LogicSolveColor)
            #
            #        screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9))+float(SCREENSIZE[0])/27*((candidate-1)%3+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9))+float(SCREENSIZE[1])/27*((candidate-1)/3+0.5)-text.get_height() / 2)))

            #Draw
            if Board[i][1]==TempBoard[i][1] or not TempBoard[i][0]=="":
                screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
        #Draw user entered numbers black
        
    else: #We are bruteforcing (normal)
        for i in range(81):
            #make the text
            if Board[i][1]==1:
                text=font.render(str(Board[i][0]),True,LogicSolveColor) #make orange if constant
            elif not Board[i][0]=="":
                text=font.render(str(Board[i][0]),True,BruteSolveColor) #make blue if variable
            else:
                #draw the possible candidates
                if  DrawPossible:
                    for candidate in PossibleList[i]:
                        text=candidatefont.render(str(candidate),True,LogicSolveColor)
    
                        screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9))+float(SCREENSIZE[0])/27*((candidate-1)%3+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9))+float(SCREENSIZE[1])/27*((candidate-1)/3+0.5)-text.get_height() / 2)))

            #Draw
            if Board[i][1]==1 or not Board[i][0]=="":
                screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
        #Draw user entered numbers black
    for i in range(81):
        text=font.render(str(BoardNumbers[i]),True,PlacedTextColor)
        screen.blit(text,(int(float(SCREENSIZE[0])/9*((i%9)+0.5)-text.get_width() / 2),int(float(SCREENSIZE[1])/9*((i/9)+0.5)-text.get_height() / 2)))
    pygame.display.flip()
    #pygame.time.wait(500)
    #print "Drew"
def PrintBoard(Board): #Prints board to stdout
    for i in range(9):
        for j in Board[(i*9):((i+1)*9)]:
            if j in (1,2,3,4,5,6,7,8,9):
                print str(j)+" ",
            else:
                print ". ",
        print

def FetchInternetGeneratedBoard(boardtype):
    #This method fetches an board generated by the website http://kjell.haxx.se/sudoku/
    #It's rather "hacky", haven't worked much with html manipulation and just wanted it to work
    #boardtype consists of a list with the content [numbers on board,difficultylevel]
    #it's only with 17 numbers, that different difficulties can be choesen. Here there are 5 diffirent levels
    seed=random.randint(0,2146999999)
    numbers=boardtype[0]
    level=boardtype[1]
    url="http://kjell.haxx.se/sudoku/?action=Create%20a%20field&seed="+str(seed)+"-v3-"+str(numbers)+"-L"+str(level)
    import urllib
    try:
        f=urllib.urlopen(url)
        site=f.read()
        f.close()
    except IOError:
        print "Internet not available or kjell.haxx.se down"
        return -1
    fetchedBoard=[]
    fetchednumbers=0
    for i in range(len(site)-10): #itterate through all characters in the fetched html
    #we need to find the string 'value="' and then save the value after the " character.
    #When we have fund 81 values, we are done.
        if site[i]=='v' and site[i+1]=='a' and site[i+2]=='l' and site[i+3]=='u' and site[i+4]=='e' and site[i+5]=='=' and site[i+6]=='"':
            fetchedBoard.append(site[i+7])
            fetchednumbers+=1
        if fetchednumbers>=81:
            break
    #print fetchedBoard

    #Now we have fetched the board. The numbers is however arranged differently than we want.
    #They are arranged in 9 groups which is the blocks, block 0 is 0-8, block 1 is 9-17 and so on
    #We want the numbers to be arranged in Collumns: Collumn 0 is 0-8, collumn 1 is 9-17

    #split fetchedBoard up in blocks
    fetchedBlocks=[]
    for i in range(9):
        fetchedBlocks.append([])
        for j in range(9):
            fetchedBlocks[i].append(fetchedBoard[i*9+j])
            
            
    #Split each block in three parts, put in fetchedblocks
    for i in range(9):
        temp=fetchedBlocks[i]
        fetchedBlocks[i]=[[],[],[]]
        for j in range(3):
            fetchedBlocks[i][j]=temp[j*3:(j+1)*3]
    
    #put the split up blocks in collumns
    fetchedCollumns=[[]]*9
    for i in range(9):
        for j in range(3):
            for cell in fetchedBlocks[j+(i/3)*3][i%3][0:3]:
                fetchedCollumns[i].append(cell)
    
    #Put the collumns into final board
    FinalBoard=[]
    for i in range(9):
        for cell in fetchedCollumns[i]:
            FinalBoard.append(cell)
    
    
    #Lastly, we want to replace '"' with "", and make the char to int's
    for i in range(81):
        if FinalBoard[i]=='"':
            FinalBoard[i]=""
        else:
            FinalBoard[i]=int(FinalBoard[i])
    print "Fetched board with seed "+str(seed)+"-v3-"+str(numbers)+"-L"+str(level)
    return FinalBoard


BoardNumbers=[""] * 81
Graphics=1
Verbose=0
CurrentState=[1]*8
if len(sys.argv)>1: #If given argument, run in commandline only
    Graphics=0
    #The argument should be a board of the same format as the savefiles
    #e.g. ......1.....6..7.8..4........67.1......4...9...5....4..8..9.2..72..8........5..3.
    if sys.argv[1]=="--solve":
        #try to set verbose
        try:
            if sys.argv[4]=="--verbose" or sys.argv[4]=="-v":
                Verbose=1
        except IndexError:
            pass
        try:
            GivenBoard=sys.argv[2]
            #Put Board into BoardNumbers
            current=0
            for char in GivenBoard:
                if char in ('0','1','2','3','4','5','6','7','8','9','.'):
                    if current >80:
                        break   #Break if we reach board limit
                    
                    if char in ("1","2","3","4","5","6","7", "8", "9"):
                        BoardNumbers[current]=int(char)
                    else:
                        BoardNumbers[current]=""
                current+=1
            #Solve
            Ready=CheckMissplacements(BoardNumbers,0)
            #count number of entered numbers, we have to have at least 16 (comment out if you want to solve anyway!)
            numbers=[]
            for i in range(81):
                    numbers.append(BoardNumbers[i])
            enteredNumbers=81-numbers.count("")
            #if enteredNumbers<=-1:
            #    Ready=(4,enteredNumbers)
            #print Ready #debug
            if Ready==0:
                 #print SolveBoard()
                SolvedBoard=SolveBoard(BoardNumbers)
                if not SolvedBoard==-1:
                    if Verbose:
                        print  SolvedBoard[-1]
                    Temp=[""]*81
                    #Print the solved Board
                    for i in range(81):
                        Temp[i]=SolvedBoard[i][0]

                    AsString=0
                    try:
                        if sys.argv[3]=="--string":
                            AsString=1
                            #output as string instead of board

                            #Make string
                            boardstr=""
                            for cell in Temp:
                                if cell in (1,2,3,4,5,6,7,8,9):
                                    boardstr+=str(cell)
                                elif cell=="":
                                    boardstr+="."
                            #Output string:
                            print boardstr
                    except IndexError:
                        pass
                    if not AsString:
                        PrintBoard(Temp)
                else:
                    print "The given board was not valid. It could not be solved"

            else:
                print "The given board was not valid. It contains two identical numbers in one unit"
        except IndexError:
            print """
Usage:
    PySuSolve.py [--solve or --generate][<board> or <difficulty>][--string (optional)][--verbose]
    Start without argument for a graphical interface"""

    elif sys.argv[1]=="--generate":
        try:
            difficulty=int(sys.argv[2])
            GeneratedBoard=GenerateBoard(difficulty)
            AsString=0
            try:
                if sys.argv[3]=="--string":
                    AsString=1
                    #output as string instead of board

                    #Make string
                    boardstr=""
                    for cell in GeneratedBoard:
                        if cell in (1,2,3,4,5,6,7,8,9):
                            boardstr+=str(cell)
                        elif cell=="":
                            boardstr+="."
                    #Output string:
                    print boardstr
            except IndexError:
                pass
            if not AsString==1:
                PrintBoard(GeneratedBoard)
        except IndexError:
            print """
Usage:
    PySuSolve.py [--solve or --generate][<board> or <difficulty>][--string (optional)]
    Start without argument for a graphical interface"""
    else:
        print """
Usage:
    PySuSolve.py [--solve or --generate][<board> or <difficulty>][--string (optional)]
    Start without argument for a graphical interface"""


    sys.exit()


import pygame
from pygame.locals import *
import os
import hashlib
import base64
import Tkinter, Tkconstants, tkFileDialog
import time
pygame.init()
screen=pygame.display.set_mode(SCREENSIZE,0,32)
pygame.display.set_caption("PySuSolve", "PySS") #Set title
icon=pygame.image.load(os.path.dirname(os.path.realpath(sys.argv[0]))+"/PySuSolve.png").convert() #Path to icon
pygame.display.set_icon(icon)
font = pygame.font.SysFont(FONTUSED, int(ScaleFont*float(FONTBASIS)/12))
SelectedField=[0,0]
DrawBoard(BoardNumbers)
Enterpressed=0
clock=pygame.time.Clock()
Verbose=1
while 1:


    #Eventquoue
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()

        elif event.type==KEYDOWN:
            if event.key in (K_1, K_KP1) :
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=1
            elif event.key in (K_2, K_KP2):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=2
            elif event.key in (K_3, K_KP3):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=3
            elif event.key in (K_4, K_KP4):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=4
            elif event.key in (K_5, K_KP5):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=5
            elif event.key in (K_6, K_KP6):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=6
            elif event.key in (K_7, K_KP7):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=7
            elif event.key in (K_8, K_KP8):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=8
            elif event.key in (K_9, K_KP9):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=9
            elif event.key in (K_DELETE, K_0, K_KP0):
                BoardNumbers[SelectedField[0]+SelectedField[1]*9]=""
            elif event.key==K_i: #Fetch board from the internet
                if not BoardNumbers[0]=="" and not BoardNumbers[1]=="":
                    wantednumbers=int(BoardNumbers[0])*10+int(BoardNumbers[1])
                elif BoardNumbers[0]=="" and not BoardNumbers[1]=="":
                    wantednumbers=int(BoardNumbers[1])
                elif  BoardNumbers[1]=="" and not BoardNumbers[0]=="":
                    wantednumbers= int(BoardNumbers[0])*10
                else:
                    wantednumbers=17 #if no difficulty intered, use 17
                if wantednumbers<17:
                    wantednumbers=17 #we can't have less than 17
                elif wantednumbers>81:
                    wantednumbers=81
                if not wantednumbers==17:
                    difficulty=1 #only one difficulty when more than 17 numbers
                else:
                    if not (BoardNumbers[2]=="" or BoardNumbers[2]>=6):
                        difficulty=int(BoardNumbers[2])
                    else:
                        difficulty=5 #use 5 if no value entered, or value is higher than 5
                temp=FetchInternetGeneratedBoard((wantednumbers,difficulty))
                if not temp==-1:
                    BoardNumbers=temp

            elif event.key==K_s:
                #Save current board to file.
                #File is saved in ./SavedBoards/--FileName--
                #--FileName-- is the md5sum of the board (with . used for blank)

                #Create string of board
                boardstr=""
                for i in range(81):
                        if not BoardNumbers[i]=="":
                            boardstr+=str(BoardNumbers[i])
                        else:
                            boardstr+="."

                #Create md5sum (and condense a little. This is not collisionproof, but collisions is unlikely
                boardmd5=base64.urlsafe_b64encode(hashlib.md5(boardstr).digest())[:-10]

                #open and create file
                root=Tkinter.Tk()
                fileName = tkFileDialog.asksaveasfilename(parent=root, initialfile=boardmd5,title="Save the board as")
                root.withdraw()
                if len(fileName ) > 0:
                    print "Saved as "+ fileName
                    f=open(fileName,'w+')
                    f.write(boardstr)
                    f.close()
                break
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
                BoardNumbers=[""]*81
            elif event.key==K_a: #make dialog to choose solving algorithm
                CurrentState=ChooseSolvingAlgorithm(CurrentState)
                #print CurrentState
                break
            elif event.key in (K_RETURN, K_KP_ENTER):
                Ready=CheckMissplacements(BoardNumbers,0)
                #count number of entered numbers, we have to have at least 16 (comment out if you want to solve anyway!)
                numbers=[]
                for i in range(81):
                        numbers.append(BoardNumbers[i])
                enteredNumbers=81-numbers.count("")
                #if enteredNumbers<=-1:
                #    Ready=(4,enteredNumbers)
                #print Ready #debug
                DrawBoard(BoardNumbers,Ready)
                Enterpressed=1
                if Ready==0:
                    #print SolveBoard()
                    SolvedBoard=SolveBoard(BoardNumbers)
                    DrawSolvedBoard(SolvedBoard,BoardNumbers)
                    #print SolvedBoard
                    if not SolvedBoard in (-1,-2): 
                        print  SolvedBoard[-1]
                        Temp=[""]*81

                        #Print the solved Board
                        for i in range(81):
                            Temp[i]=SolvedBoard[i][0]
                        PrintBoard(Temp)

            elif event.key==K_l: #Load from a user chosen file
                root=Tkinter.Tk()
                fileName = tkFileDialog.askopenfilename(parent=root,title='Open Board')
                root.withdraw()
                print "Loaded " +fileName
                try:
                    file=open(fileName,'r')
                except IOError:
                    break #File does not exist
                if len(fileName)>0:
                    BoardNumbers=[""]*81
                    current=0
                    while True:
                        thischar=file.read(1)
                        if thischar=="" or current>80:
                            break   #Break if we reach end of file
                        if thischar in ('0','1','2','3','4','5','6','7','8','9','.'):
                            if not thischar in ('.','0'):
                                BoardNumbers[current]=int(thischar)
                            else:
                                BoardNumbers[current]=""
                            current+=1
                    file.close()

            elif event.key==K_g: #Generate a new board
                if not BoardNumbers[0]=="" and not BoardNumbers[1]=="":
                    difficulty=int(BoardNumbers[0])*10+int(BoardNumbers[1])
                elif BoardNumbers[0]=="" and not BoardNumbers[1]=="":
                    difficulty=int(BoardNumbers[1])
                elif  BoardNumbers[1]=="" and not BoardNumbers[0]=="":
                    difficulty= int(BoardNumbers[0])*10
                else:
                    print [BoardNumbers[0],BoardNumbers[1]]

                
                #print "difficulty: "+str(difficulty)
                Graphics=0
                GeneratedBoard=GenerateBoard(difficulty)
                Graphics=1
                #Fill The Board Into BoardNumbers
                current=0
                for cell in GeneratedBoard:
                    if cell=="":
                        BoardNumbers[current]=""
                    else:
                        BoardNumbers[current]=int(cell)
                    current+=1
                






            if Enterpressed==0:
                DrawBoard(BoardNumbers)
            Enterpressed=0


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:

                #print event.pos #debug
                #print ("Field number="+str(int(float(event.pos[0])/SCREENSIZE[0]*9))+","+str(int(float(event.pos[1])/SCREENSIZE[1]*9))) #debug
                SelectedField=[int(float(event.pos[0])/SCREENSIZE[0]*9),int(float(event.pos[1])/SCREENSIZE[1]*9)]
                DrawBoard(BoardNumbers)

    clock.tick(60)


