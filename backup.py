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
