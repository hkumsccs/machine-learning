""" Solve Tic Tac Toe misere version

Idea:

Initial data:

game.status = ((0,1,2,3,4,5,6,7,8),(0,1,2,3,4,5,6,7,8),(0,1,2,3,4,5,6,7,8))
game.aiboard = [] # keep tracking
game.playerboard = [] # keep tracking
game.playerIndex = 0
game.status = 0 (draw) -1 (ai wins) 1 (player wins)

while(game is not end) { 

  update( game, game.playerIndex )

  game.playerIndex = ( game.playerIndex + 1 ) % 2

}

"""
import copy

class Game:
  def __init__(self):
    self.board = (['0','1','2','3','4','5','6','7','8'], ['0','1','2','3','4','5','6','7','8'], ['0','1','2','3','4','5','6','7','8'])
    #self.aiboard = [] # keep tracking
    #self.playerboard = [] # keep tracking
    self.playerIndex = 0
    self.status = [1, 1, 1]
    self.depth = 2

  def copy(self):
    g = Game()
    g.board = self.board
    g.status = self.status
    g.depth = self.depth
    g.playerIndex = self.playerIndex
    return g

  def isEnd(self):
    # End only when all three boards are dead
    if len([i for i, x in enumerate(self.status) if x == 0]) == 3:
      # Trick: See the bottom of main in loop, check end is run after the player index is increased
      if self.playerIndex == 1:
        print "You win the AI !" 
      else:
        print "AI win the game !"
      return True
    
    return False 

#
def parseMutate(status, board, input):
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
  if status[id] == 0 or board[id][index] != input[1]:
    return False 
  # Mutate the original board globally
  board[id][index] = 'X'
  return True 

def eliminateDeadBoard(board, status):
  for id in [i for i, x in enumerate(status) if x == 1]:
    # Dead check in 3 rows
    for row in range(0, 3):
      if board[id][3*row] == 'X' and board[id][3*row+1] == 'X' and board[id][3*row+2] == 'X':
        status[id] = 0
        return
    # Dead check in 3 columns
    for col in range(0, 3):
      if board[id][col] == 'X' and board[id][col+3] == 'X' and board[id][col+6] == 'X':
        status[id] = 0
        return
    # Dead check in 2 diagonal
    if board[id][4] == 'X' and ((board[id][0] == 'X' and board[id][8] == 'X') or (board[id][2] == 'X' and board[id][6] == 'X')):
      status[id] = 0
      return

def update (game, playerIndex):
  if playerIndex == 0:
    aiOutput = brain(copy.deepcopy(game))
    parseMutate(game.status, game.board, aiOutput)
    print "AI: {0}".format(aiOutput)
  else:
    isValidInput = False 
    while not isValidInput:
      isValidInput = parseMutate(game.status, game.board, raw_input('Your move: '))
  
  eliminateDeadBoard(game.board, game.status)   

def draw (status, board):
  head = ''
  for id in range(0, 3):
    if status[id] == 1:
      head += "{0}:      ".format(chr(id + 65))
  print head
  for row in range(0, 3):
    display = ''
    for id in range(0, 3):
      if status[id] == 1:
        display += "{0} {1} {2}   ".format(board[id][3*row], board[id][3*row+1], board[id][3*row+2])
    print display

#############################################################################################
def brain (game):
  # Do not want to mutate the original reference
  return minimax(game, 0, 0)[0] 

def minimax(game, agentIdx, layer):
    if 2 <= agentIdx:
      agentIdx = 0 # Pacman's turn again
      layer += 1 

    if layer == game.depth:
      return (0, evaluationFunction(game))
     
    if agentIdx == 0:
      return eval('MAX', game, agentIdx, layer)
    else:
      return eval('MIN', game, agentIdx, layer)

def eval(type, game, agentIdx, layer):

    # Terminal node checking, no legal move anymore
    if len(getLegalMoves(game.board, game.status)) == 0:
      return (0, evaluationFunction(game))

    if type == 'MIN':
      # Worst max is inf (Initialize)
      v = ("unknown", float("inf"))
    else:
      # Worst max is -inf (Initialize)
      v = ("unknown", -float("inf"))

    for action in getLegalMoves(game.board, game.status):

      result = minimax(generateSuccessor(game, action), agentIdx+1, layer)[1]

      if type == 'MIN':
        nextv = min(v[1], result)
      else:
        nextv = max(v[1], result)

      if nextv is not v[1]:
        v = (action, nextv)

    return v 

def getLegalMoves (board, status):
  # Return something like { "A": [], "B": [], "C": [] } 
  # If the board is already dead, it won't show the board id 
  # result = {}
  result = []
  for id in [i for i, x in enumerate(status) if x == 1]:
    result += ["{0}{1}".format(chr(id+65), i) for i, x in enumerate(board[id]) if x != 'X']
  return result

def generateSuccessor(game, action):
  # Check whether the ord is already occupied
  index = int(action[1])
  id = ord(action[0]) - 65
  # No need to check if the board is not dead and is occupied
  # Mutate the original board globally
  game.board[id][index] = 'X'
  return game

def evaluationFunction (game):

  return 1
##############################################################################################

# Start main
if __name__ == "__main__":
  game = Game()
  while not game.isEnd():
    update(game, game.playerIndex)
    draw(game.status, game.board)
    game.playerIndex = (game.playerIndex + 1) % 2

