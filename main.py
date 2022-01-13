#Flow
#1. Display aruco marker and detect board dimentions 
#2. Measure distance of board 
#3. Display screen and board
#4. Loop while true
#   4.1 Detect hand position and gesture
#   4.2 Update display accordingly
from Setup import *
from drow import syncBackground

def main():
    print("start")
    module=HTM()
    syncBackground()
    #corners=GetBoardDimention()
    #boardDistance=GetBoardDistance(module)
    #end of setup
    #startBoard()
    
    

if __name__ == "__main__":
    main()