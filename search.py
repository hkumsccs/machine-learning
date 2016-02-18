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

# Abstract method to do backtracking
# FIXME Refactor this method to keep simple
def backTrackAlgorithm(stateRoute, currentRoute):
    bp, trick = 0, False 
    for bp in range(min(len(stateRoute), len(currentRoute))):
        if stateRoute[bp] != currentRoute[bp]:
            trick = False 
            del currentRoute[bp:]
            break
        else:
            trick = True

    return currentRoute + stateRoute[bp+1 if trick else bp:]

# Abstract method to implemnt GFS
def graphSearchAlgorithm(problem, fringe, priority = False, explored = set(), currentRoute = []):
    # Initialize frontier using initial state of problem ,explore set to be empty ,a path list as the result
    apply(fringe.push, [[problem.getStartState()]] + ([0] if priority else []))
    # While frontier is not empty
    while not fringe.isEmpty():
        # Choose a leaf node and remove it from fringe
        stateRoute, stateCost = fringe.pop(), 0
        # If node is not in the explored set
        if stateRoute[-1] not in explored:
            # Add node to explored set
            explored.add(stateRoute[-1])
            # Start backtracking
            currentRoute = backTrackAlgorithm(list(stateRoute), list(currentRoute)) 
            # If node contains a goal state then return corresponding solution
            if problem.isGoalState(stateRoute[-1]): break
            # Expand the node, adding the resulting node
            for nextState, nextDirection, nextStateCost in problem.getSuccessors(stateRoute[-1]):
                if len(set([nextState]) - explored) != 0:
                    #fringe.push((nextState, currentRoute + [nextDirection]))
                    apply(fringe.push, [currentRoute + [nextState]] + ([stateCost + nextStateCost] if priority else []))
            
    return [ getDirection(stateRoute[i], stateRoute[i-1]) for i in range(1, len(stateRoute)) ]

def getDirection(l, r):
    if(r[0]-l[0] == 1): return 'West'
    if(r[0]-l[0] == -1): return 'East'
    if(r[1]-l[1] == 1): return 'South'
    if(r[1]-l[1] == -1): return 'North'

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
    return graphSearchAlgorithm(problem, util.Stack())

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return graphSearchAlgorithm(problem, util.Queue())

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    return graphSearchAlgorithm(problem, util.PriorityQueue(), True)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    return graphSearchAlgorithm(problem, util.PriorityQueueWithFunction(heuristic))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
