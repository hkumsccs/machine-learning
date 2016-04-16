from copy import deepcopy
import numpy as np

DEPTH = 3
NUM_AGENT = 2
# Misere quotient in the paper, pick prime numbers (arbitrary)
QA, QB, QC, QD = 3, 7, 2, 5

def isEnd(board):
  # End only when all three boards are dead
  return countAliveBoard(board) == 0

def isBoardAlive(board):
  # Dead check in 3 rows
  for row in range(0, 3):
    if board[3*row] == 'X' and board[3*row+1] == 'X' and board[3*row+2] == 'X':
      return False
  # Dead check in 3 columns
  for col in range(0, 3):
    if board[col] == 'X' and board[col+3] == 'X' and board[col+6] == 'X':
      return False 
  # Dead check in 2 diagonal
  if board[4] == 'X' and board[0] == 'X' and board[8] == 'X':
    return False
  if board[2] == 'X' and board[4] == 'X' and board[6] == 'X':
    return False 

  return True 

def countAliveBoard(board):
  count = 0
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      count += 1
  return count

def draw (board):
  head = ''
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      head += '{0}:      '.format(chr(id + 65))
  print head
  for row in range(0, 3):
    display = ''
    for id in range(0, 3):
      if isBoardAlive(board[id]):
        display += '{0} {1} {2}   '.format(board[id][3*row], board[id][3*row+1], board[id][3*row+2])
    print display

def parseMutate(board, inputVal): # Type check (is it a string)
  if not isinstance(inputVal, str):
    return False
  # Length check (is it a string with length 2)
  if len(inputVal) != 2:
    return False
  # Type check
  if inputVal[0] not in set(['A', 'B', 'C']) or inputVal[1] not in set(['0', '1', '2', '3', '4', '5', '6', '7', '8']):
    return False
  # Check whether the ord is already occupied
  index = int(inputVal[1])
  id = ord(inputVal[0]) - 65
  # Check if the board is not dead and is occupied
  if not isBoardAlive(board[id]) or board[id][index] != inputVal[1]:
    return False 
  # Mutate the original board globally
  board[id][index] = 'X'
  return True 

def getLegalMoves (board):
  # If the board is already dead, it won't show the board id 
  result = []
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      result += ['{0}{1}'.format(chr(id+65), i) for i, x in enumerate(board[id]) if x != 'X']
  return result

def generateSuccessor(board, action):
  # Check whether the ord is already occupied
  newBoard = deepcopy(board)
  index, id = int(action[1]), ord(action[0]) - 65
  newBoard[id][index] = 'X'
  return newBoard 

def computeQuotient(board):
  v = 1
  for b in board:
    v *= getFingerprint(b)
  return v

def isPset(q):
  return q == QC*QC or q == QA or q == QB*QB or q == QB*QC

def evaluationFunction (board, playerIndex):
  score = 0
  if countAliveBoard(board) == 0:
    if playerIndex == 0:
      score -= 3000
    else:
      score += 3000

  if isPset(computeQuotient(board)) and playerIndex == 0:
    score += 500
  return score 

def minimax(board, depth, playerIndex, ab):

  if isEnd(board) or depth == DEPTH:
    return (None, evaluationFunction(board, playerIndex))

  if isPset(computeQuotient(board)) and depth > 0:
    return (None, evaluationFunction(board, playerIndex))
  
  legalMoves = getLegalMoves(board)

  if(playerIndex == 1):
    return evalMax(board, legalMoves, depth + 1, ab)
  else:
    return evalMin(board, legalMoves, depth + 1, ab)

def evalMax (board, legalMoves, depth, ab):
  v = (None, -float('inf'))
  for lmove in legalMoves:
    nodev = minimax(generateSuccessor(board, lmove), depth, 0, ab)
    if nodev[1] > ab[1]:
      return (lmove, nodev[1])
    ab = (max(ab[0], nodev[1]), ab[1])
    if nodev[1] > v[1]:
      v = (lmove, nodev[1])
  return v

def evalMin (board, legalMoves, depth, ab):
  v = (None, float('inf'))
  for lmove in legalMoves:
    nodev = minimax(generateSuccessor(board, lmove), depth, 1, ab)
    if nodev[1] < ab[0]:
      return (lmove, nodev[1])
    ab = (ab[0], min(ab[1], nodev[1]))
    if nodev[1] < v[1]:
      v = (lmove, nodev[1])
  return v

def getFingerprint (currentBoard):
  board = deepcopy(currentBoard)
  for rotation in range(0, 4):
    rBoard = rotate90(board, rotation)
    for board in [rBoard, flip(rBoard, 'RL'), flip(rBoard, 'UD')]:
      if board == ['.','.','.','.','.','.','.','.','.']:
        return QC 
      if board == ['.','.','.','.','X','.','.','.','.']:
        return QC*QC
      if board == ['X','X','.','.','.','.','.','.','.']:
        return QA*QD 
      if board == ['X','.','X','.','.','.','.','.','.']:
        return QB 
      if board == ['X','.','.','.','X','.','.','.','.']:
        return QB 
      if board == ['X','.','.','.','.','X','.','.','.']:
        return QB
      if board == ['X','.','.','.','.','.','.','.','X']:
        return QA 
      if board == ['.','X','.','X','.','.','.','.','.']:
        return QA 
      if board == ['.','X','.','.','X','.','.','.','.']:
        return QB 
      if board == ['.','X','.','.','.','.','.','X','.']:
        return QA 
      if board == ['X','X','.','X','.','.','.','.','.']:
        return QB
      if board == ['X','X','.','.','X','.','.','.','.']:
        return QA*QB
      if board == ['X','X','.','.','.','X','.','.','.']:
        return QD
      if board == ['X','X','.','.','.','.','X','.','.']:
        return QA
      if board == ['X','X','.','.','.','.','.','X','.']:
        return QD
      if board == ['X','X','.','.','.','.','.','.','X']:
        return QD
      if board == ['X','.','X','.','X','.','.','.','.']:
        return QA
      if board == ['X','.','X','.','.','.','X','.','.']:
        return QA*QB
      if board == ['X','.','X','.','.','.','.','X','.']:
        return QA 
      if board == ['X','.','.','.','X','X','.','.','.']:
        return QA
      if board == ['.','X','.','X','X','.','.','.','.']:
        return QA*QB
      if board == ['.','X','.','X','.','X','.','.','.']:
        return QB
      if board == ['X','X','.','X','X','.','.','.','.']:
        return QA 
      if board == ['X','X','.','X','.','X','.','.','.']:
        return QA
      if board == ['X','X','.','X','.','.','.','.','X']:
        return QA
      if board == ['X','X','.','.','X','X','.','.','.']:
        return QB
      if board == ['X','X','.','.','X','.','X','.','.']:
        return QB 
      if board == ['X','X','.','.','.','X','X','.','.']:
        return QB
      if board == ['X','X','.','.','.','X','.','X','.']:
        return QA*QB
      if board == ['X','X','.','.','.','X','.','.','X']:
        return QA*QB
      if board == ['X','X','.','.','.','.','X','X','.']:
        return QB
      if board == ['X','X','.','.','.','.','X','.','X']:
        return QB
      if board == ['X','X','.','.','.','.','.','X','X']:
        return QA 
      if board == ['X','.','X','.','X','.','.','X','.']:
        return QB
      if board == ['X','.','X','.','.','.','X','.','X']:
        return QA
      if board == ['X','.','.','.','X','X','.','X','.']:
        return QB
      if board == ['.','X','.','X','.','X','.','X','.']:
        return QA 
      if board == ['X','X','.','X','.','X','.','X','.']:
        return QB 
      if board == ['X','X','.','X','.','X','.','.','X']:
        return QB 
      if board == ['X','X','.','.','X','X','X','.','.']:
        return QA
      if board == ['X','X','.','.','.','X','X','X','.']:
        return QA 
      if board == ['X','X','.','.','.','X','X','.','X']:
        return QA
      if board == ['X','X','.','X','.','X','.','X','X']:
        return QA

  return 1

# Rotate 90 with given time anti-clockwise
def rotate90 (board, time):
  board = deepcopy(board)
  board1x9 = ['.' if i != 'X' else 'X' for i in board]
  board3x3 = np.resize(board1x9, (3,3))
  rotateboard3x3 = np.rot90(board3x3, time)
  return np.resize(rotateboard3x3, (1,9)).tolist()[0]

def flip (board, mode):
  board1x9 = deepcopy(board)
  board3x3 = np.resize(board1x9, (3,3))  
  if mode == 'RL':
    flipboard3x3 = np.fliplr(board3x3) 
  else:
    flipboard3x3 = np.flipud(board3x3)
  return np.resize(flipboard3x3, (1,9)).tolist()[0] # returns flipped board in 1x9 list format

#run the game
if __name__ == "__main__":

  #inital the board
  board= (['0','1','2','3','4','5','6','7','8'],['0','1','2','3','4','5','6','7','8'],['0','1','2','3','4','5','6','7','8'])
  playerIndex = 1

  while(not isEnd(board)):
    if playerIndex == 1:
      aiOutput = minimax(board, 0, playerIndex, (-float("inf"), float("inf")))[0]
      parseMutate(board, aiOutput)
      print 'AI: {0}'.format(aiOutput)
    else:
      isValidInput = False                                              
      while not isValidInput:
        isValidInput = parseMutate(board, raw_input('Your move: '))

    playerIndex = (playerIndex + 1) % 2
    draw(board)

  if playerIndex == 0:
    # Never go here (supposed)
    print 'Omg, You win !' 
  else:
    print 'AI win !'
