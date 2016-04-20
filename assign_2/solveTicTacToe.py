# Edit by Tony Ngan (COMP7404 Assignment 2) 
"""
Import packages here
"""
from copy import deepcopy
import numpy as np
"""
Global constants is defined here
"""
DEPTH = 3
NUM_AGENT = 2
QA, QB, QC, QD = 2, 3, 5, 7 # Misere quotient in the paper, pick prime numbers (arbitrary)
"""
@param{board} an array

End only when all three boards are dead
"""
def isEnd(board):
  return countAliveBoard(board) == 0
"""
@param{board} an array

A helper function which checks if a single board is alive
"""
def isBoardAlive(board):
  for row in range(0, 3):
    if board[3*row] == 'X' and board[3*row+1] == 'X' and board[3*row+2] == 'X':
      return False
  for col in range(0, 3):
    if board[col] == 'X' and board[col+3] == 'X' and board[col+6] == 'X':
      return False 
  if board[4] == 'X' and board[0] == 'X' and board[8] == 'X':
    return False
  if board[2] == 'X' and board[4] == 'X' and board[6] == 'X':
    return False 
  return True 
"""
@param{board} an array

Count how many board is alive
"""
def countAliveBoard(board):
  count = 0
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      count += 1
  return count
"""
@param{board} an array

Output the board in the screen
"""
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
"""
@param{board} an array
@param{inputVal} a string 

Intepret and parse the input (e.g. A1, B2) with various type checking 
"""
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
"""
@param{board} an array

Get all the legal moves in the board, output is an array (e.g. ['A1','B3','C5'])
"""
def getLegalMoves (board):
  # If the board is already dead, it won't show the board id 
  result = []
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      result += ['{0}{1}'.format(chr(id+65), i) for i, x in enumerate(board[id]) if x != 'X']
  return result
"""
@param{board} an array
@param{action} a valid board index (e.g. 'A2')

Generate the successor board based on the current board and action
"""
def generateSuccessor(board, action):
  # Check whether the ord is already occupied
  newBoard = deepcopy(board)
  index, id = int(action[1]), ord(action[0]) - 65
  newBoard[id][index] = 'X'
  return newBoard 
"""
@param{board} an array

Linear algebra for the quotient computation of those three boards, should ignore the dead board (always 1) 
"""
def computeQuotient(board):
  v = 1
  for b in board:
    v *= getFingerprint(b)
  return v
"""
@param{q} quotient

Check if the value is in the P-set
"""
def isPset(q):
  return q == QC*QC or q == QA or q == QB*QB or q == QB*QC
"""
@param{board} an array 
@param{playerIndex} indicates which player is playing (AI:0, HUMAN:1)

Evaluation function returns a score based on the current board
"""
def evaluationFunction (board, playerIndex):
  score = 0
  if countAliveBoard(board) == 0:
    if playerIndex == 1:
      score -= 3000
    else:
      score += 3000

  if isPset(computeQuotient(board)) and playerIndex == 1:
    score += 500
  return score 
"""
@param{board} an array
@param{depth} current depth 
@param{playerIndex} indicates which player is playing (AI:0, HUMAN:1)
@param{ab} a tuple indicates the current alpha and beta value for pruning

Recursive minimax approach until the terminal node or reaching the depth limit
"""
def minimax(board, depth, playerIndex, ab):
  if isEnd(board) or depth == DEPTH:
    return (None, evaluationFunction(board, playerIndex))
  # take action if p-set is found
  if isPset(computeQuotient(board)) and depth > 0:
    return (None, evaluationFunction(board, playerIndex))
  legalMoves = getLegalMoves(board)
  if(playerIndex == 0):
    return evalMax(board, legalMoves, depth + 1, ab)
  else:
    return evalMin(board, legalMoves, depth + 1, ab)
"""
@param{board} an array
@param{depth} current depth 
@param{playerIndex} indicates which player is playing (AI:0, HUMAN:1)
@param{ab} a tuple indicates the current alpha and beta value for pruning

Executes the max node
"""
def evalMax (board, legalMoves, depth, ab):
  v = (None, -float('inf'))
  for lmove in legalMoves:
    nodev = minimax(generateSuccessor(board, lmove), depth, 1, ab)
    if nodev[1] > ab[1]:
      return (lmove, nodev[1])
    ab = (max(ab[0], nodev[1]), ab[1])
    if nodev[1] > v[1]:
      v = (lmove, nodev[1])
  return v
"""
@param{board} an array
@param{depth} current depth 
@param{playerIndex} indicates which player is playing (AI:0, HUMAN:1)
@param{ab} a tuple indicates the current alpha and beta value for pruning

Executes the min node
"""
def evalMin (board, legalMoves, depth, ab):
  v = (None, float('inf'))
  for lmove in legalMoves:
    nodev = minimax(generateSuccessor(board, lmove), depth, 0, ab)
    if nodev[1] < ab[0]:
      return (lmove, nodev[1])
    ab = (ab[0], min(ab[1], nodev[1]))
    if nodev[1] < v[1]:
      v = (lmove, nodev[1])
  return v
"""
@param{currentBoard} an array

Get the pattern from all possible rotated and fliped (up-down/right-left) board
43 unique patterns are proposed in the paper
Default is set to 1
"""
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
"""
@param{board} an array
@param{time} how many time of rotation (anti-clockwise) 

Rotate 90 with given time anti-clockwise using native methods
"""
def rotate90 (board, time):
  board = deepcopy(board)
  board1x9 = ['.' if i != 'X' else 'X' for i in board]
  board3x3 = np.resize(board1x9, (3,3))
  rotateboard3x3 = np.rot90(board3x3, time)
  return np.resize(rotateboard3x3, (1,9)).tolist()[0]
"""
@param{board} an array
@param{mode} flip mode (RL: right-left, UD: up-down) 

Flip the board based on the input mode
"""
def flip (board, mode):
  board1x9 = deepcopy(board)
  board3x3 = np.resize(board1x9, (3,3))  
  if mode == 'RL':
    flipboard3x3 = np.fliplr(board3x3) 
  else:
    flipboard3x3 = np.flipud(board3x3)
  return np.resize(flipboard3x3, (1,9)).tolist()[0] # returns flipped board in 1x9 list format
"""
Run the code starting from here
"""
if __name__ == "__main__":
  board= (['0','1','2','3','4','5','6','7','8'],['0','1','2','3','4','5','6','7','8'],['0','1','2','3','4','5','6','7','8']) # inital the board
  playerIndex = 0
  while(not isEnd(board)):
    if playerIndex == 0:
      aiOutput = minimax(board, 0, playerIndex, (-float("inf"), float("inf")))[0]
      parseMutate(board, aiOutput)
      print 'AI: {0}'.format(aiOutput)
    else:
      isValidInput, isFirstTime = False, True
      while not isValidInput:
        if not isFirstTime:
          print 'Invalid input ! Please check and input again !'
        isValidInput, isFirstTime = parseMutate(board, raw_input('Your move: ')), False

    playerIndex = (playerIndex + 1) % 2
    draw(board)

  if playerIndex == 1:
    # Never go here (supposed)
    print 'Omg, You win !' 
  else:
    print 'AI win !'
