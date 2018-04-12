#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *
import random
import copy
# 
#  * A bayesian network
#  * @author Panqu
#  
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    # 
    #     * Mapping of random variables to nodes in the network
    #     
    varMap = None

    # 
    #     * Edges in this network
    #     
    edges = None

    # 
    #     * Nodes in the network with no parents
    #     
    rootNodes = None

    # 
    #     * Default constructor initializes empty network
    #     
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    # 
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #     
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    # 
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #     
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    # 
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #     
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #     
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """
        #  TODO

        # Number of times queryVar=T in event x
        count = float(0)

        # Number of times x is consistent with givenVars
        normalizeCount = float(0)

        # Do numSamples amount of tests
        j = 0
        while j < numSamples:
            consistent = True
            x = self.priorSample()
            for var in givenVars:
                if x[var.getName()] != givenVars[var]:
                    consistent = False

            if consistent:
                if x[queryVar.getName()]:
                    count += 1
                normalizeCount += 1

            j += 1

        return count / normalizeCount

    # Randomly generates values for each node and creates an event
    # Returns an event called assignments
    def priorSample(self):

        # Event that is returned
        assignments = {}

        # Allows to check nodes in topological order
        queue = []

        # Add sample of root nodes to list
        for root in self.rootNodes:
            # Creates random value for root nodes
            parResult = random.random() < root.cpt.probability
            assignments[root.variable.getName()] = parResult

            # Add children to queue
            for children in root.getChildren():
                queue.append(children)

        # Generates random values for each node
        while len(queue) > 0:
            curNode = queue.pop(0)
            for curChildren in curNode.getChildren():
                queue.append(curChildren)

            result = random.random() < curNode.cpt.getProbability(assignments, True)
            assignments[curNode.variable.getName()] = result

        return assignments


    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        #  TODO

        # Number of times queryVar=T in event x
        count = 0.0

        # Total weight that gets returned from weightedSample
        normalizeCount = 0.0

        # Do numSamples amount of tests
        j = 0
        while j < numSamples:
            event, weight = self.weightedSample(givenVars)
            if event[queryVar.getName()]:
                count += weight
            normalizeCount += weight

            j += 1

        return count / normalizeCount

    # Creates an event with the givenVar set to passed in values
    # Then generates random values for unassigned nodes
    # Returns an event called assignment, along with the
    # corresponding weight for the event.
    def weightedSample(self, givenVars):

        # Weight associated with the event
        weight = 1.0

        # Event to be returned
        assignments = {}

        # Allows to check nodes in topological order
        queue = []

        # Assign givenVar values to assignments
        for var in givenVars:
            assignments[var.getName()] = givenVars[var]

        # Add sample of root node to list and if root
        # is unassigned, randomly assign it a value
        for root in self.rootNodes:

            # Checks if root is a givenVar
            evidenceVar = False
            for var in givenVars:
                if root.getVariable().getName() == var.getName():
                    evidenceVar = True

            # If givenVar, calculate the weight, else assign random value
            if evidenceVar:
                value = givenVars[root.getVariable()]
                weight *= root.cpt.getProbability(assignments, value)
            else:
                parResult = random.random() < root.cpt.probability
                assignments[root.variable.getName()] = parResult

            # Append children to the queue
            for children in root.getChildren():
                if children not in queue:
                    queue.append(children)

        # Calculate weights (if a givenVar) or assigns a random value (if unassigned)
        # to all nodes
        while len(queue) > 0:
            curNode = queue.pop(0)

            # Append children to the queue
            for curChildren in curNode.getChildren():
                if curChildren not in queue:
                    queue.append(curChildren)

            # Checks if curNode is a givenVar
            evidenceVar2 = False
            for var in givenVars:
                if curNode.getVariable().getName() == var.getName():
                    evidenceVar2 = True

            # If givenVar, calculate the weight, else assign random value
            if evidenceVar2:
                value = givenVars[curNode.getVariable()]
                weight *= curNode.cpt.getProbability(assignments, value)
            else:
                result = random.random() < curNode.cpt.getProbability(assignments, True)
                assignments[curNode.variable.getName()] = result

        return assignments, weight

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using Gibbs sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numTrials Number of Gibbs trials to perform, where a single trial consists of assignments to ALL
    #       non-evidence variables (ie. not a single state change, but a state change of all non-evidence variables)
    #     
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """
        #  TODO

        # Number of times queryVar=T in event x
        count = 0.0

        # Number of trials that were generated
        normalizeCount = 0.0

        # A list of nonevidence variables
        nonevidences = []

        # Current state of each node value
        curState = {}

        # Adds givenVars to the current state
        for keys in givenVars.keys():
            curState[keys.getName()] = givenVars[keys]

        # initialized curState with random values for nonevidence variables
        for vars in self.varMap:
            if not curState.has_key(vars.getName()):
                ranBool = random.random()
                a = (ranBool < self.varMap.get(vars).getProbability(curState, True))
                curState[vars.getName()] = a
                nonevidences.append(vars)

        # Do numTrials number of samples
        j = 0
        while j < numTrials:

            # Loop through all nonevidence variables and calculate the markov blanket
            for nonev in nonevidences:
                rand = random.random()
                probabilityTrue = self.varMap.get(nonev).getProbability(curState, True)
                for childrenT in self.varMap.get(nonev).getChildren():
                    probabilityTrue *= childrenT.getProbability(curState, curState[childrenT.getVariable().getName()])

                probabilityFalse = self.varMap.get(nonev).getProbability(curState, False)
                for childrenF in self.varMap.get(nonev).getChildren():
                    probabilityFalse *= childrenF.getProbability(curState, curState[childrenF.getVariable().getName()])

                probability = probabilityTrue / (probabilityTrue + probabilityFalse)
                b = rand < probability
                curState[nonev.getName()] = b

            alpha = 1
            for keys in givenVars.keys():
                alpha *= self.varMap.get(keys).getProbability(curState, curState[keys.getName()])

            # Increment count if queryVar = True in current state
            if curState[queryVar.getName()]:
                count += alpha
            normalizeCount += alpha

            j += 1

        return count / normalizeCount