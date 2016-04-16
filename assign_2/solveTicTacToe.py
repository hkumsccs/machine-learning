""" Solve Tic Tac Toe misere version

Idea:

Initial data:

game.board = ((0,1,2,3,4,5,6,7,8),(0,1,2,3,4,5,6,7,8),(0,1,2,3,4,5,6,7,8))
game.playerIndex = 0

while(game is not end) { 
  update( game, game.playerIndex )
  game.playerIndex = ( game.playerIndex + 1 ) % 2
}

"""
import copy
import numpy as np

class Configuration:
  def __init__(self, board, depth):
    self.board = copy.deepcopy(board)
    self.depth = copy.deepcopy(depth)

class Game:
  def __init__(self):
    self.board = (['0','1','2','3','4','5','6','7','8'], ['0','1','2','3','4','5','6','7','8'], ['0','1','2','3','4','5','6','7','8'])
    self.playerIndex = 0
    self.depth = 3

  def copy(self):
    g = Game()
    g.board = self.board
    g.depth = self.depth
    g.playerIndex = self.playerIndex
    return g

  def isEnd(self):
    # End only when all three boards are dead
    if countAliveBoard(self.board) == 0:
      # Trick: See the bottom of main in loop, check end is run after the player index is increased
      if self.playerIndex == 1:
        print "You win the AI !" 
      else:
        print "AI win the game !"
      return True
    
    return False 

def countAliveBoard(board):
  count = 0
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      count += 1
  return count

#
def parseMutate(board, input):
  # Type check (is it a string)
  if not isinstance(input, str):
    return False
  # Length check (is it a string with length 2)
  if len(input) != 2:
    return False
  # Type check
  if input[0] not in set(["A", "B", "C"]) or input[1] not in set(["0", "1", "2", "3", "4", "5", "6", "7", "8"]):
    return False
  # Check whether the ord is already occupied
  index = int(input[1])
  id = ord(input[0]) - 65
  # Check if the board is not dead and is occupied
  if not isBoardAlive(board[id]) or board[id][index] != input[1]:
    return False 
  # Mutate the original board globally
  board[id][index] = 'X'
  return True 

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
  if board[4] == 'X' and ((board[0] == 'X' and board[8] == 'X') or (board[2] == 'X' and board[6] == 'X')):
    return False 

  return True 

def update (game, playerIndex):
  if playerIndex == 0:
    aiOutput = brain(copy.deepcopy(game))
    parseMutate(game.board, aiOutput)
    print "AI: {0}".format(aiOutput)
  else:
    isValidInput = False 
    while not isValidInput:
      isValidInput = parseMutate(game.board, raw_input('Your move: '))

def draw (board):
  head = ''
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      head += "{0}:      ".format(chr(id + 65))
  print head
  for row in range(0, 3):
    display = ''
    for id in range(0, 3):
      if isBoardAlive(board[id]):
        display += "{0} {1} {2}   ".format(board[id][3*row], board[id][3*row+1], board[id][3*row+2])
    print display

#############################################################################################
def brain (game):
  # Do not want to mutate the original reference
  return minimax(game, 0, 0)[0] 

def minimax(game, agentIdx, layer):

    config = Configuration(game.board, game.depth)

    if 2 <= agentIdx:
      agentIdx = 0 # Pacman's turn again

    layer += 1 

    if layer == config.depth or countAliveBoard(game.board) == 0:
      return (0, evaluationFunction(config.board, agentIdx))
     
    if agentIdx == 0:
      return eval('MAX', config, agentIdx, layer)
    else:
      return eval('MIN', config, agentIdx, layer)

def eval(type, game, agentIdx, layer):

    legalMoves = getLegalMoves(game.board)
    # Terminal node checking, no legal move anymore
    if len(legalMoves) == 0:
      return (0, evaluationFunction(game.board, agentIdx))

    if type == 'MIN':
      # Worst max is inf (Initialize)
      v = (None, float("inf"))
    else:
      # Worst max is -inf (Initialize)
      v = (None, -float("inf"))

    for action in legalMoves:
      successor = generateSuccessor(game, action)
      #print layer 
      result = minimax(successor, agentIdx+1, layer)[1]
      #print "result {0}".format(result)
      if type == 'MIN':
        nextv = min(v[1], result)
      else:
        nextv = max(v[1], result)

      if nextv is not v[1]:
        v = (action, nextv)

    return v 

def getLegalMoves (board):
  # If the board is already dead, it won't show the board id 
  # result = {}
  result = []
  for id in range(0, 3):
    if isBoardAlive(board[id]):
      result += ["{0}{1}".format(chr(id+65), i) for i, x in enumerate(board[id]) if x != 'X']
  return result

def generateSuccessor(game, action):
  # Check whether the ord is already occupied
  board = copy.deepcopy(game.board)
  depth = copy.deepcopy(game.depth)

  index = int(action[1])
  id = ord(action[0]) - 65
  # No need to check if the board is not dead and is occupied
  # Mutate the original board globally
  board[id][index] = 'X'
  return Configuration(board, depth) 

def evaluationFunction (board, playerIndex):
  board = copy.deepcopy(board)
  score = 0
  
  if countAliveBoard(board) == 0:
    if playerIndex == 1:
      score -= 3000
    else:
      score += 3000

  v = 1 
  for b in board: 
    v *= getFingerprint(b)

  a, b, c, d = 2, 3, 5, 7
  if v == c*c or v == a or v == b*b or v == b*c:
    if playerIndex == 0:
      score += 500

  return score 

# The input board is being treated (e.g. rotated/fliped)
def getFingerprint (currentBoard):
  # Set a,b,c,d to prime number first
  a, b, c, d = 2, 3, 5, 7
  board = copy.deepcopy(currentBoard)
  for rotation in range(0, 3):
    rBoard = rotate90(board, rotation)
    for board in [rBoard, fliplr(rBoard), flipud(rBoard)]:
      if board == ['.','.','.','.','.','.','.','.','.']:
        return c
      if board == ['.','.','.','.','X','.','.','.','.']:
        return c*c
      if board == ['X','X','.','.','.','.','.','.','.']:
        return a*d 
      if board == ['X','.','X','.','.','.','.','.','.']:
        return b 
      if board == ['X','.','.','.','X','.','.','.','.']:
        return b 
      if board == ['X','.','.','.','.','X','.','.','.']:
        return b
      if board == ['X','.','.','.','.','.','.','.','X']:
        return a 
      if board == ['.','X','.','X','.','.','.','.','.']:
        return a 
      if board == ['.','X','.','.','X','.','.','.','.']:
        return b 
      if board == ['.','X','.','.','.','.','.','X','.']:
        return a 
      if board == ['X','X','.','X','.','.','.','.','.']:
        return b
      if board == ['X','X','.','.','X','.','.','.','.']:
        return a*b
      if board == ['X','X','.','.','.','X','.','.','.']:
        return d
      if board == ['X','X','.','.','.','.','X','.','.']:
        return a
      if board == ['X','X','.','.','.','.','.','X','.']:
        return d
      if board == ['X','X','.','.','.','.','.','.','X']:
        return d
      if board == ['X','.','X','.','X','.','.','.','.']:
        return a
      if board == ['X','.','X','.','.','.','X','.','.']:
        return a*b
      if board == ['X','.','X','.','.','.','.','X','.']:
        return a 
      if board == ['X','.','.','.','X','X','.','.','.']:
        return a
      if board == ['.','X','.','X','X','.','.','.','.']:
        return a*b
      if board == ['.','X','.','X','.','X','.','.','.']:
        return b
      if board == ['X','X','.','X','X','.','.','.','.']:
        return a 
      if board == ['X','X','.','X','.','X','.','.','.']:
        return a
      if board == ['X','X','.','X','.','.','.','.','X']:
        return a
      if board == ['X','X','.','.','X','X','.','.','.']:
        return b
      if board == ['X','X','.','.','X','.','X','.','.']:
        return b 
      if board == ['X','X','.','.','.','X','X','.','.']:
        return b
      if board == ['X','X','.','.','.','X','.','X','.']:
        return a*b
      if board == ['X','X','.','.','.','X','.','.','X']:
        return a*b
      if board == ['X','X','.','.','.','.','X','X','.']:
        return b
      if board == ['X','X','.','.','.','.','X','.','X']:
        return b
      if board == ['X','X','.','.','.','.','.','X','X']:
        return a 
      if board == ['X','.','X','.','X','.','.','X','.']:
        return b
      if board == ['X','.','X','.','.','.','X','.','X']:
        return a
      if board == ['X','.','.','.','X','X','.','X','.']:
        return b
      if board == ['.','X','.','X','.','X','.','X','.']:
        return a 
      if board == ['X','X','.','X','.','X','.','X','.']:
        return b 
      if board == ['X','X','.','X','.','X','.','.','X']:
        return b 
      if board == ['X','X','.','.','X','X','X','.','.']:
        return a
      if board == ['X','X','.','.','.','X','X','X','.']:
        return a 
      if board == ['X','X','.','.','.','X','X','.','X']:
        return a
      if board == ['X','X','.','X','.','X','.','X','X']:
        return a
  return 1

# Rotate 90 with given time anti-clockwise
def rotate90 (board, time):
  board1x9 = ['.' if i != 'X' else 'X' for i in board]
  board3x3 = np.resize(board1x9, (3,3))
  rotateboard3x3 = np.rot90(board3x3, time)
  return np.resize(rotateboard3x3, (1,9)).tolist()

def fliplr (board1x9):
  #board1x9 = ['.' if i != 'X' else 'X' for i in board]
  board3x3 = np.resize(board1x9, (3,3))  
  flipboard3x3 = np.fliplr(board3x3) 
  return np.resize(flipboard3x3, (1,9)).tolist() # returns flipped board in 1x9 list format

def flipud (board1x9):
  #board1x9 = ['.' if i != 'X' else 'X' for i in board]
  board3x3 = np.resize(board1x9, (3,3))  
  flipboard3x3 = np.flipud(board3x3) 
  return np.resize(flipboard3x3, (1,9)).tolist() # returns flipped board in 1x9 list format
##############################################################################################

# Start main
if __name__ == "__main__":
  game = Game()
  while not game.isEnd():
    update(game, game.playerIndex)
    draw(game.board)
    game.playerIndex = (game.playerIndex + 1) % 2

