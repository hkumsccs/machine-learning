"""
Solve Tic Tac Toe misere version

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
class Game:
  def __init__(self):
    self.board = (['0','1','2','3','4','5','6','7','8'], ['0','1','2','3','4','5','6','7','8'], ['0','1','2','3','4','5','6','7','8'])
    self.aiboard = [] # keep tracking
    self.playerboard = [] # keep tracking
    self.playerIndex = 0
    self.status = 0

  def isEnd(self):
    #TODO
    return False 

#
def parseInput (board, input):
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
  if board[id][index] != input[1]:
    return False 

  # Mutate the original board globally
  board[id][index] = 'X'
  return True 
   
def update (game, playerIndex):
  if playerIndex == 0:
    print 'AI: '
  else:
    isValidInput = False 
    while not isValidInput:
      isValidInput = parseInput(game.board, raw_input('Your move: '))

def brain (game):
  # TODO
  return "";

def draw (board):
  for row in range(0, 3):
    display = ''
    for id in range(0, 3):
      display += "{0} {1} {2}   ".format(board[id][3*row], board[id][3*row+1], board[id][3*row+2])
    print display

if __name__ == "__main__":
  game = Game()
  while not game.isEnd():
    update(game, game.playerIndex)
    draw(game.board)
    game.playerIndex = (game.playerIndex + 1) % 2

