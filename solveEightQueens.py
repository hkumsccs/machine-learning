import random
import copy
import operator
from optparse import OptionParser

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        solutionCounter = 0
        lectureCase = [[]]
        if lectureExample:
            lectureCase = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "q", ".", ".", ".", "."],
            ["q", ".", ".", ".", "q", ".", ".", "."],
            [".", "q", ".", ".", ".", "q", ".", "q"],
            [".", ".", "q", ".", ".", ".", "q", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ]
        for i in range(0,numberOfRuns):
            if self.search(Board(lectureCase), verbose).getNumberOfAttacks() == 0:
                solutionCounter+=1
        print "Solved:",solutionCounter,"/",numberOfRuns

    def search(self, board, verbose):
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print "iteration ",i
                print newBoard.toString()
                print newBoard.getCostBoard().toString()
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks) = newBoard.getBetterBoard()
            i+=1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [["." for i in range(0,8)] for j in range(0,8)]
        for i in range(0,8):
            tmpSquareArray[random.randint(0,7)][i] = "q"
        return tmpSquareArray
          
    def toString(self):
        s = ""
        for i in range(0,8):
            for j in range(0,8):
                s += str(self.squareArray[i][j]) + " "
            s += "\n"
        return s + "# attacks: "+str(self.getNumberOfAttacks())

    def getCostBoard(self):
        costBoard = copy.deepcopy(self)
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        if self.getNumberOfAttacks() != 0:
            #TODO: put your code here...
            costBoard = self.getCostBoard().squareArray
            minCostPosition = []
            n = len(self.squareArray)
            
            info = [(item, row, col) if item != 'q' else (9999, row, col) for row, sublist in enumerate(costBoard) for col, item in enumerate(sublist)]
            minCost = min(info , key=operator.itemgetter(0))[0]
            minCostPositionInfo = [v for i, v in enumerate(info) if v[0] == minCost]
            smvi, smvr, smvc = minCostPositionInfo[random.randint(0, len(minCostPositionInfo) - 1)]

            # Update
            for r in range(0, n):
                if r == smvr:
                    self.squareArray[r][smvc] = "q"
                else:
                    self.squareArray[r][smvc] = "."

            return (self, minCost)
        else:
            return (self, 0)

    def getNumberOfAttacks(self):
        #TODO: put your code here...
        count = 0
        n = len(self.squareArray)
        queens = [-1] * n
        #Record the queen column position
        for r in range(0,n):
            for c in range(0,n):
                if self.squareArray[r][c] == "q":
                    queens[c] = r

        for r in range(0,n):
            for c in range(r+1,n):
                if queens[r] == queens[c] or abs(r-c) == abs(queens[r]-queens[c]):
                    count += 1

        return count 

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(0)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
