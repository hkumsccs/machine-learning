# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    return  [s,s,w,s,w,e,w,w,s,w]

def depthFirstSearch_v1(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #===================================
    from game import Directions
    s, w, e, n = Directions.SOUTH, Directions.WEST, Directions.EAST, Directions.NORTH
    backTrackDict = { s:n, n:s, w:e, e:w }
 
    # Initialize frontier using initial state of problem ,explore set to be empty ,a path list as the result
    frontier, explored, actions, backTrackActions = util.Stack(), set(), [], []
    frontier.push((problem.getStartState(), '', 0))

    # While frontier is not empty
    while not frontier.isEmpty():
        # Choose a leaf node and remove it from frontier
        currentState, action, depth = frontier.pop()
        # Backtrack
        # Why -1 because we have to eliminate the joint, for example
        #
        # joint (cost: 8) - p-1 (cost: 9 and no more to explore)
        #   |
        #  p-2  (cost: 9)
        #
        # When we do backtracking, we need 1 step backward (-1), 9 - 9 and need minus 1
        backStep = len(backTrackActions) - depth + 1
        if len(actions) != 0 and backStep > 0:
            reverse = map(lambda a: backTrackDict.get(a), backTrackActions[:-backStep-1:-1])
            del backTrackActions[-len(reverse):]
            actions = actions + reverse 
        # 
        if action != '':
            backTrackActions.append(action)
            actions.append(action)
        # If node contains a goal state then return corresponding solution
        if problem.isGoalState(currentState):
            break;
        # If node is not in the explored set
        if currentState not in explored:
            # Add node to explored set
            explored.add(currentState)
            # Expand the node, adding the resulting node
            for nextState, nextAction, nextStepCost in problem.getSuccessors(currentState):
                if len(set([nextState]) - explored) != 0:
                    frontier.push((nextState, nextAction, depth + 1))

    return actions 
    #===================================

def graphSearchAlgorithm():

    return None

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Initialize frontier using initial state of problem ,explore set to be empty ,a path list as the result
    frontier, explored, actions, backTrackActions = util.Stack(), set(), [], []
    frontier.push((problem.getStartState(), []))

    # While frontier is not empty
    while not frontier.isEmpty():
        # Choose a leaf node and remove it from frontier
        (state, stateRoute), bp, trick = frontier.pop(), 0, False
        # If node is not in the explored set
        if state not in explored:
            # Add node to explored set
            explored.add(state)
            # Common backtracking algorithm
            for bp in range(min(len(stateRoute),len(backTrackActions))):
                if stateRoute[bp] != backTrackActions[bp]:
                    del actions[-len(backTrackActions)+bp:]
                    trick = False 
                    break
                else:
                    trick = True

            backTrackActions = list(stateRoute) # Cache the current for next round backtracking
            actions = list(actions) + stateRoute[bp+1 if trick else bp:]
                 
            # If node contains a goal state then return corresponding solution
            if problem.isGoalState(state):
                break
            # Expand the node, adding the resulting node
            for nextState, nextAction, nextStepCost in problem.getSuccessors(state):
                if len(set([nextState]) - explored) != 0:
                    frontier.push((nextState, list(stateRoute) + [nextAction]))

    return actions 

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    # Initialize frontier using initial state of problem ,explore set to be empty ,a path list as the result
    frontier, explored, actions, backTrackActions = util.Queue(), set(), [], []
    frontier.push((problem.getStartState(), [], 0))
    # While frontier is not empty
    while not frontier.isEmpty():
        # Choose a leaf node and remove it from frontier
        (state, stateRoute, depth), bp, trick = frontier.pop(), 0, False
        # 
        # If node is not in the explored set
        if state not in explored:
            # Add node to explored set
            explored.add(state)
            # Common backtracking algorithm
            for bp in range(min(len(stateRoute),len(backTrackActions))):
                if stateRoute[bp] != backTrackActions[bp]:
                    del actions[-len(backTrackActions)+bp:]
                    trick = False 
                    break
                else:
                    trick = True

            backTrackActions = list(stateRoute) # Cache the current for next round backtracking
            actions = list(actions) + stateRoute[bp+1 if trick else bp:]
                 
            # If node contains a goal state then return corresponding solution
            if problem.isGoalState(state):
                break
            # Expand the node, adding the resulting node
            for nextState, nextAction, nextStepCost in problem.getSuccessors(state):
                if len(set([nextState]) - explored) != 0:
                    frontier.push((nextState, list(stateRoute) + [nextAction], depth + 1))

    return actions 

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
