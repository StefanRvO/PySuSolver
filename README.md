A Sudoku solver written in python



THIS IS FREE AND OPEN SOURCE SOFTWARE

LICENSED UNDER THE BEERWARE LICENSE



By Stefan Ravn van Overeem


############
This is sudoko solver written in python, using pygame for graphics
It aims to be able to solve all sodukos and as fast as possible

###########



#Controls


##i:
Fetches a board from the url http://kjell.haxx.se/sudoku/
These boards are true sodukos, they have only one solution
The difficulty of the board is choosen be the first 3 numbers entered in the interfaces left top corner.
The first 2 is how many numbers should be on the board, and the last is difficulty when only 17 numbers is choosen (1-5)
##b:
Opens a dolog box where a board of the form 1......6..32.5.67.4....2...5..7..4..2....5. can be entered. Empty fields are . or 0.
##s:
Saves the board.
Sugestion to safename is th md5sum (cutted down a little for shortness)
##c:
Clear the board
##a:
Opens a dialog where the used solving algorithms can be choosen
If both bruteforce and bruteforce random is choosen, you can cancel out of bruteforcerandom by pressing ESC and continue to normal bruteforce
##ENTER:
Starts the solving
##l:
Loads a board
##g:
Generate a board. These boards are not true sodukos, as they have no unique solutions
##ESC:
cancel the solving




#General about solving


If choosen, the solver first try to solve the board with logic, if it can't it continues to bruteforcing

bruteforcerandom tries to solv the board logical but places som random numbers to help it.
it is generally faster on boards with a small amount of solved cells
Should not be used on multiple solution boards. It may never finish if used on these.

Normal bruteforce just tries all possible placements. It will allways find a solution.
may be very slow at boards with few solved cells
is usually faster an boards with many solved cells


