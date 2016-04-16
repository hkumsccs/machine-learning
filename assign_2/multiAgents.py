# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (currentPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = currentGameState.getFood().asList()
        successorPacPos = successorGameState.getPacmanPosition()

        for ghostState in newGhostStates:
          if ghostState.getPosition() == successorPacPos:
            return -float("inf") # Avoid Ghost eats Pacman, very conservative in map having capsules

        numFood = len(foodList)

        pacFoodDist = [-2 * util.manhattanDistance(foodPos, currentPos) for foodPos in foodList]

        return max(pacFoodDist) 

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        startDepth = 0
        currentAgentIdx = 0 # Pacman goes first
        return self.minimax(gameState, currentAgentIdx, startDepth)[0]

    def minimax(self, gameState, agentIdx, layer):
        numAgents = gameState.getNumAgents()
        
        if numAgents <= agentIdx:
          agentIdx = 0 # Pacman's turn again
          layer += 1 

        if layer == self.depth:
          return (0, self.evaluationFunction(gameState))
         
        if agentIdx == 0:
          return self.eval('MAX', gameState, agentIdx, layer)
        else:
          return self.eval('MIN', gameState, agentIdx, layer)

    def eval(self, type, gameState, agentIdx, layer):

        # Terminal node checking, no legal move anymore
        if not gameState.getLegalActions(agentIdx):
          return (0, self.evaluationFunction(gameState))

        if type == 'MIN':
          # Worst max is inf (Initialize)
          decision = (Directions.STOP, float("inf"))
        else:
          # Worst max is -inf (Initialize)
          decision = (Directions.STOP, -float("inf"))

        for action in gameState.getLegalActions(agentIdx):
          if action != Directions.STOP:
            result = self.minimax(gameState.generateSuccessor(agentIdx, action), agentIdx + 1, layer)[1]

            if type == 'MIN':
              nextDecision = min(decision[1], result)
            else:
              nextDecision = max(decision[1], result)

            if nextDecision is not decision[1]:
              decision = (action, nextDecision)

        return decision 


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        startDepth = 0
        currentAgentIdx = 0 # Pacman goes first
        return self.minimax(gameState, currentAgentIdx, startDepth, (-float("inf"), float("inf")))[0]

    def minimax(self, gameState, agentIdx, layer, ab):
        numAgents = gameState.getNumAgents()
        
        if numAgents <= agentIdx:
          agentIdx = 0 # Pacman's turn again
          layer += 1 

        # ab-pruning doesn't limit the depth (maybe)
        if layer == self.depth or gameState.isLose() or gameState.isWin():
          return (0, self.evaluationFunction(gameState))
         
        if agentIdx == 0:
          return self.eval('MAX', gameState, agentIdx, layer, ab)
        else:
          return self.eval('MIN', gameState, agentIdx, layer, ab)

    def eval(self, type, gameState, agentIdx, layer, ab):

        # Terminal node checking, no legal move anymore
        if not gameState.getLegalActions(agentIdx):
          return (0, self.evaluationFunction(gameState))

        if type == 'MIN':
          # Worst max is inf (Initialize)
          decision = (Directions.STOP, float("inf"))
        else:
          # Worst max is -inf (Initialize)
          decision = (Directions.STOP, -float("inf"))

        for action in gameState.getLegalActions(agentIdx):
          if action != Directions.STOP:
            result = self.minimax(gameState.generateSuccessor(agentIdx, action), agentIdx + 1, layer, ab)[1]

            if type == 'MIN':
              nextDecision = min(decision[1], result)
            else:
              nextDecision = max(decision[1], result)

            if nextDecision is not decision[1]:
              decision = (action, nextDecision)

            if type == 'MIN':
              if decision[1] < ab[0]:
                return decision
              ab = (ab[0], min(ab[1], decision[1]))
            else:
              if decision[1] > ab[1]:
                return decision
              ab = (max(ab[0], decision[1]), ab[1])

        return decision 


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        startDepth = 0
        currentAgentIdx = 0 # Pacman goes first
        return self.expectimax(gameState, currentAgentIdx, startDepth)[0]

    def expectimax(self, gameState, agentIdx, layer):
        numAgents = gameState.getNumAgents()
        
        if numAgents <= agentIdx:
          agentIdx = 0 # Pacman's turn again
          layer += 1 

        if layer == self.depth:
          return (0, self.evaluationFunction(gameState))
         
        if agentIdx == 0:
          return self.eval('MAX', gameState, agentIdx, layer)
        else:
          return self.eval('EMAX', gameState, agentIdx, layer)

    def eval(self, type, gameState, agentIdx, layer):

        # Terminal node checking, no legal move anymore
        if not gameState.getLegalActions(agentIdx):
          return (0, self.evaluationFunction(gameState))

        if type == 'EMAX':
          # Worst expectimax is 0 (Initialize)
          decision = (Directions.STOP, 0)
        else:
          # Worst max is -inf (Initialize)
          decision = (Directions.STOP, -float("inf"))

        for action in gameState.getLegalActions(agentIdx):
          if action != Directions.STOP:
            result = self.expectimax(gameState.generateSuccessor(agentIdx, action), agentIdx + 1, layer)[1]

            if type == 'EMAX':
              decision = (decision[0], decision[1] + (1./len(gameState.getLegalActions(agentIdx))) * result)
            else:
              nextDecision = max(decision[1], result)
              if nextDecision is not decision[1]:
                decision = (action, nextDecision)

        return decision 

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return - float("inf")
    score = scoreEvaluationFunction(currentGameState)
    newFood = currentGameState.getFood()
    foodPos = newFood.asList()
    closestfood = float("inf")
    for pos in foodPos:
        thisdist = util.manhattanDistance(pos, currentGameState.getPacmanPosition())
        if (thisdist < closestfood):
            closestfood = thisdist
    numghosts = currentGameState.getNumAgents() - 1
    i = 1
    disttoghost = float("inf")
    while i <= numghosts:
        nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
        disttoghost = min(disttoghost, nextdist)
        i += 1
    score += max(disttoghost, 4) * 2
    score -= closestfood * 1.5
    capsulelocations = currentGameState.getCapsules()
    score -= 4 * len(foodPos)
    score -= 3.5 * len(capsulelocations)
    return score


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

