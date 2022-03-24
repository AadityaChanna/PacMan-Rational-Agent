# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)

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
        remaining food (newFood) and Pacman position after moving (newPos).

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(self.index, action)
        newPos = successorGameState.getPacmanPosition(self.index)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        if successorGameState.isWin():
            return 500
        
        if currentGameState.generateSuccessor(self, 0, action).isWin():
            return -500

        newGhostList = []
        for x in newGhostStates:
            newGhostList.append(x.getPosition())
        
        distanceGhost = []
        for x in newGhostList:
            distanceGhost.append(util.manhattanDistance(newPos, x))

        currentGhostList = []
        for x in currentGameState.getGhostStates():
            currentGhostList.append(x.getPosition())

        distanceCurrentGhosts = []
        for x in currentGhostList:
            distanceCurrentGhosts.append(util.manhattanDistance(currentGameState.getPacmanPosition(self.index)), x)

        score = 0
        if action == Directions.STOP:
            score -= 1
        if min(distanceGhost) < min(distanceCurrentGhosts):
            score -= 300
        
        if len(newFood.asList()[0]) < len(currentGameState.getFood()[0]):
            score += 200
        
        else:
            if len(min(util.manhattanDistance(newPos, newFood.asList()[0]))) < len(min(util.manhattanDistance(newPos, currentGameState.getFood()[0]))):
                score += 200
            else:
                score -= 100
              
        
        
        return score


        util.raiseNotDefined()


def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()[index]

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index = 0, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = index # Pacman is always agent index 0
        self.evaluationFunction = lambda state:util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)



class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    You implementation here
    """

    def evaluationFunction2(self, futureGameState, currentGameState):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        
        # Useful information you can extract from a GameState (pacman.py)
        newPos = futureGameState.getPacmanPosition(self.index)
        currPos = currentGameState.getPacmanPosition(self.index)
        newFood = futureGameState.getFood()
        newGhostStates = futureGameState.getGhostStates()
        newCapsule = futureGameState.getCapsules()
        
        if futureGameState.isWin():
            return 9999999
        
        if futureGameState.isLose():
            return -999999


        score = self.evaluationFunction(currentGameState)
        newGhostList = []
        for x in newGhostStates:
            newGhostList.append(x.getPosition())
        
        distanceGhost = []
        for x in newGhostList:
            distanceGhost.append(util.manhattanDistance(newPos, x))

        currentGhostList = []
        for x in currentGameState.getGhostStates():
            currentGhostList.append(x.getPosition())

        distanceCurrentGhosts = []
        for x in currentGhostList:
            distanceCurrentGhosts.append(util.manhattanDistance(currentGameState.getPacmanPosition(self.index), x))

        newFoodList = []
        for x in newFood:
            newFoodList.append(x)

        distanceFood = []
        for x in newFoodList:
            distanceFood.append(util.manhattanDistance(newPos ,x))

        currentFoodList = []
        for x in currentGameState.getFood():
            currentFoodList.append(x)

        currentDistanceFood = []
        for x in currentFoodList:
            currentDistanceFood.append(util.manhattanDistance(currentGameState.getPacmanPosition(self.index), x))

        newCapsuleList = []
        for x in newCapsule:
            newCapsuleList.append(x)

        if len(newCapsuleList) != 0: 
            distanceCapsule = []
            for x in newCapsuleList:
                distanceCapsule.append(util.manhattanDistance(newPos ,x))

            currentCapsuleList = []
            for x in currentGameState.getCapsules():
                currentCapsuleList.append(x)

            currentDistanceCapsule = []
            for x in currentCapsuleList:
                currentDistanceCapsule.append(util.manhattanDistance(currentGameState.getPacmanPosition(self.index), x))

            if len(currentCapsuleList) > len(newCapsuleList):
                score += (200 * (len(currentFoodList) +1))
            elif (min(currentDistanceCapsule) - min(distanceCapsule)) != 0:
                score += (300 * (len(currentFoodList) +1) * 1/(min(currentDistanceCapsule) - min(distanceCapsule)))
    

        if min(distanceGhost) < min(distanceCurrentGhosts):
            score -= 30

        if len(newFoodList) < len(currentFoodList):
            score += 100 * (len(currentFoodList) - len(newFoodList))
        
        elif (min(currentDistanceFood) - min(distanceFood)) != 0:
            score += 300 * 1/(min(currentDistanceFood) - min(distanceFood))
              
        
        
        return score

    
        score = 1    * currentScore + \
                -1.5 * distanceToClosestFood + \
                -2    * (1./distanceToClosestActiveGhost) + \
                -2    * distanceToClosestScaredGhost + \
                -20 * numberOfCapsulesLeft + \
                -4    * numberOfFoodsLeft
        
    
    def minFunc(self, index2, depth, gameState, oldGame):
            minVal = 99999999999
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction2(gameState, oldGame)
            legalMoves = gameState.getLegalActions(index2)
            legalNextState = [gameState.generateSuccessor(index2, action) for action in legalMoves]
            for newState in legalNextState:
                if index2 == gameState.getNumAgents() - 1:
                    minVal = min(minVal, self.maxFunc(depth + 1, newState, oldGame))
                else:
                    minVal = min(minVal, self.minFunc(index2 + 1, depth, newState, oldGame))
                    
            return minVal
    
    def maxFunc(self, depth, gameState, oldGame):
        maxVal = -99999999999
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction2(gameState, oldGame)
        if depth == self.depth:
            return self.evaluationFunction2(gameState, oldGame)
        legalMoves = gameState.getLegalActions(self.index)
        legalNextState = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        for newState in legalNextState:
            maxVal = max(maxVal, self.minFunc(1, depth, newState, oldGame))
        return maxVal

    def getAction(self, gameState):
        index = self.index # pacman index
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        Some functions you may need:
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legalMoves = gameState.getLegalActions(agent)
        legalNextState = [gameState.generateSuccessor(agent, action)
                          for action in legalMoves]
        """


        score = -9999999999
        action = ' '
        legalMoves = gameState.getLegalActions(index)
        legalNextState = [gameState.generateSuccessor(index, action) for action in legalMoves]
        for newAction in legalMoves:
            newGame = gameState.generateSuccessor(index, newAction)
            newScore = self.minFunc(1, 0, newGame, gameState)
            if score < newScore:
                score = newScore
                action = newAction

        print("Number of Pacmans:", gameState.getNumPacman(), ", Number of ghosts:", gameState.getNumGhosts())
        print(score)
        return action
        util.raiseNotDefined()


    


        
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




