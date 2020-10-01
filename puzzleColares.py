# -*- coding: utf-8 -*-

import random
from searchPlus import *

class Bead(object):
    
    def __init__(self, colour):
        self._colour = colour

    def getColour(self):
        return self._colour
    
    def setColour(self, colour):
        self._colour = colour

    def __str__(self):
        return "\u001b[38;5;"+str(self._colour)+"mO\u001b[0m"



class Necklace(object):
    
    """ necklace: necklace to clone
        colourBeadsDist: quick and dirty way to initialize a necklace with a 
                         distribution of coloured beads using a dictionary"""
    def __init__(self, necklace=None, colourBeadsDist={1:10,2:9,3:1}):
            
        if necklace != None:
            raise NotImplementedError
        else:
            self._numBeads = sum(colourBeadsDist.values())
            self._beads = [];
            for k in colourBeadsDist.keys():
                for i in range(colourBeadsDist[k]):
                    self._beads.append(Bead(k));


    def randomizeColors(self):
        for i in range(len(self.numBeads)):
            a = random.choice(self._beads)
            b = random.choice(self._beads)
            while a == b:
                b = random.choice(self._beads)
            
    
    def getNumBeads(self):
        return self._numBeads


    def getBead(self, k):
        return self._beads[k]
    
    
    def getBeads(self):
        return self._beads


    def getBeadColours(self):
        return [b.getColour() for b in self._beads]
    
    
    def getBeadColourDistribution(self):
        bcs = self.getBeadColours()
        colourSet = set(bcs)
        cdist =  {}
        for c in colourSet:
            cdist[c] = bcs.count(c)
        return cdist


    def removeBead(self, k):
        if (isinstance(k, int)):
            self._beads.pop(k)
            self._numBeads -= 1
            return
        if (isinstance(k, Bead)):
            self._beads.remove(k)
            self.numBeads -= 1
            return
        raise Exception("k is neither [int] or [Bead]!")


    def appendBead(self, bead):
        self.beads.append(bead)


    def insertBead(self, i, bead):
        self._beads.insert(i, bead)
        self._numBeads += 1


    def replaceBead(self, i, bead):
        self.removeBead(i)
        self.insertBead(i, bead)


    """ Rotate colours in given direction (negative = clockwise)
        direction: integer giving magnitude of rotation"""
    def rotateColours(self, direction):
        if (direction < 0):
            for k in range(-direction):
                colours = [b.getColour() for b in self._beads]
                colours = colours[1:self._numBeads]+[colours[0]]
                for i in range(self._numBeads):
                    self._beads[i].setColour(colours[i])
        else:
            for k in range(direction):
                colours = [b.getColour() for b in self._beads]
                colours = [colours[-1]] + colours[0:self._numBeads-1]
                for i in range(self._numBeads):
                    self._beads[i].setColour(colours[i])


    def __str__(self):
        return "".join([str(x) for x in self._beads])+"\u001b[0m"



class IntersectedNecklacesState(object):
    
    """ dimension: number of necklaces
        numBeads: number of beads in each necklace. Must be divisible by 4
        initConf: list of lists of integers (colour codes) according to following rules
                1. each sub-list represents a necklace
                2. necklaces have common bead colours (shared beads) as follows:
                    2.1 left necklace highest shared bead index is numBeads/2+insersection+1
                    2.1 right necklace lowest shared bead index is 0
                3. total number of colours defined in necklaces set is 2*dimension
                4. color distribution is numbeads/2 for two colours and numbeads/2-1 for the remaining ones
                Example for two rings with 20 beads:
                [[2,1,1,1,1,1,1,1,1,<3>,2,2,2,<2>,2,2,2,2,2,2],
                 [<2>,3,3,3,<3>,3,3,3,3,3,,3,4,4,4,4,4,4,4,4,4]]
                shared beads are signaled for convenience """
                
    def __init__(self, dimension=2, numBeads=20, initConf=None):

        self._dimension = dimension
        self._numBeads = numBeads
        self._intersection = int(numBeads/4) - 2
            
        self._generateRandomConfiguration()
        
        if initConf != None:
            
            # test initConf
            if len(initConf) != self._dimension:
                raise Exception("Initial configuration dimension different from puzzle dimension")
            for l in initConf:
                if len(l) != self._numBeads:
                    raise Exception("Wrong number of beads at "+str(l))
            
            # apply initConf
            for i in range(self._dimension):
                clist = initConf[i]
                necklace = self._necklaces[i]
                for j in range(self._numBeads):
                    necklace.getBead(j).setColour(clist[j])
            
            # further tests on initConf
            cdist = self.getColourDistribution()
            if (len(cdist) != 2*self._dimension):
                raise Exception("Wrong number of colours: "+str(cdist))
            if (len([c for c in cdist.values() if c == int(self._numBeads/2)]) != 2):
                raise Exception("Wrong colour distribution: "+str(cdist))
            if (len([c for c in cdist.values() if c == int(self._numBeads/2)-1]) != 2*self._dimension-2):
                raise Exception("Wrong colour distribution: "+str(cdist))


    def _generateRandomConfiguration(self):
            # generate independent necklaces
            self._necklaces = [Necklace(colourBeadsDist={1:self._numBeads}) for i in range(self._dimension)]
            
            # intersect necklaces
            for i in range(1,len(self._necklaces)):
                leftNecklace = self._necklaces[i-1]
                rightNecklace = self._necklaces[i]
                leftNecklace_k = int(self._numBeads/2) + self._intersection + 1
                leftNecklace_j = leftNecklace_k - self._intersection - 1
                rightNecklace_k = 0
                rightNecklace_j = self._intersection + 1
                rightNecklace.replaceBead(rightNecklace_j, leftNecklace.getBead(leftNecklace_j))
                rightNecklace.replaceBead(rightNecklace_k, leftNecklace.getBead(leftNecklace_k))
            
            # randomize colours
            numColours = self._dimension * 2
            cdim = int(self._numBeads / 2)
            colours = [1 for i in range(cdim)]
            colours += [2 for i in range(cdim)]
            cdim -= 1
            for j in range(3, numColours+1):
                colours += [j for i in range(cdim)]
            
            beads = []
            for necklace in self._necklaces:
                for b in necklace.getBeads():
                    if b not in beads:
                        beads.append(b)
            beads = list(beads)
            while len(colours) > 0:
                c = random.choice(colours)
                colours.remove(c)
                b = beads.pop()
                b.setColour(c)


    def getNecklaces(self):
        return self._necklaces


    def rotateColours(self, iNecklace, direction):
        self._necklaces[iNecklace].rotateColours(direction)


    def getOrderedBeads(self):
        orderedBeads = []
        for necklace in self._necklaces:
            for b in necklace.getBeads():
                if b not in orderedBeads:
                    orderedBeads.append(b)
        return orderedBeads


    def getOrderedBeadColours(self):
        return [b.getColour() for b in self.getOrderedBeads()]


    def getColourDistribution(self):
        allBeadColours = self.getOrderedBeadColours()
        colourSet = set(allBeadColours)
        cdist = {}
        for c in colourSet:
            cdist[c] = allBeadColours.count(c)
        return cdist


    def i_am_a_goal_state(self):
        """Goal is attained when each necklace has two colours condensed 
        in full sequences (complete set)."""
        # get colour distributions
        scdist = self.getColourDistribution()
        for necklace in self.getNecklaces():
            ncdist = necklace.getBeadColourDistribution()
            # must have at least two complete colours
            completeColours = [c for c in ncdist.keys() if scdist[c] == ncdist[c]]
            if len(completeColours) != 2:
                return False
                    
        # all have two complete colours
        # now lets test for full sequences
        for necklace in self.getNecklaces():
            nbColours = necklace.getBeadColours()
            ncdist = necklace.getBeadColourDistribution()
            completeColours = [c for c in ncdist.keys() if scdist[c] == ncdist[c]]
            for c in completeColours:
                ic = nbColours.index(c)
                ccount = 1
                niter = 0
                iup = ic
                idown = ic
                while (nbColours[iup] == c or nbColours[idown] == c):
                    niter += 1
                    iup = (ic + niter) % len(nbColours)
                    idown = (ic - niter) % len(nbColours)
                    if nbColours[iup] == c:
                        ccount += 1
                    if nbColours[idown] == c:
                        ccount += 1
                if ccount != scdist[c]:
                    return False
        # all have two complete colours in full sequence
        return True


    def __str__(self):
        height = self._intersection + 2
        length = int((self._numBeads - 2*height) / 2)
        scrLength = length + 1
        fullLength = scrLength * self._dimension + 4
        
        # blank screen buffer
        scr = [ [" " for i in range(fullLength)] for j in range(height+2) ]
        
        for i in range(self._dimension):
            necklace = self._necklaces[i]
            for j in range(self._numBeads):
                bead = necklace.getBead(j)
                # transform from (i,j) to scr (<l>ine, <c>olumn)
                if (j < 1):
                    l = 1 + j
                    c = i * scrLength + 1
                elif (j < height-1):
                    l = 1 + j
                    c = i * scrLength
                elif (j < height):
                    l = height
                    c = i * scrLength + 1
                elif (j < height+length):
                    l = height + 1
                    c = i * scrLength + (j-length) + 2
                elif (j < height+length+1):
                    l = height
                    c = i * scrLength + length + 2
                elif (j < height+length+height-1):
                    l = height - (j - (height+length))
                    c = i * scrLength + length + 3
                elif (j < height+length+height):
                    l = height - (j - (height+length))
                    c = i * scrLength + length + 2
                else:
                    l = 0
                    c = i * scrLength + length - (j - (height+length+height)) + 1
                scr[l][c] = str(bead)
        return "\n".join(["".join(line) for line in scr])
    
    
    """ Only compares colour values, not the bead objetcs themselves"""
    def __eq__(self, o):
        return tuple(self.getOrderedBeadColours()) == tuple(o.getOrderedBeadColours())


    def listifyed(self):
        return [[b.getColour() for b in necklace.getBeads()] for necklace in self._necklaces]



class PuzzleColares(Problem):
    
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)


    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        return [{'name':'rotate', 'target':i, 'direction':+1, 'cost':1} for i in range(len(state.getNecklaces()))] + \
               [{'name':'rotate', 'target':i, 'direction':-1, 'cost':1} for i in range(len(state.getNecklaces()))]


    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        newState = IntersectedNecklacesState(dimension=len(state.getNecklaces()), \
                        numBeads=state.getNecklaces()[0].getNumBeads(), \
                        initConf=state.listifyed())
        newState.rotateColours(iNecklace=action['target'], direction=action['direction'])
        return newState
    
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + action['cost']


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        return state.i_am_a_goal_state()


    def display(self, state):
        """ Display state """
        print(state)


def exec(p,estado,accoes):
    """ Executa uma sequência de acções a partir do estado
        devolve um par (estado, custo) depois de imprimir
    """
    custo = 0
    for a in accoes:
        seg = p.result(estado,a)
        custo = p.path_cost(custo,estado,a,seg)
        estado = seg
    return (estado,custo)



if __name__ == "__main__":
    random.seed(1234567)
    
    print()
    print("********* NECKLACE TESTS ***********")
    print()
    necklace = Necklace()
    print(necklace)
    necklace.rotateColours(-2)
    print(necklace)
    necklace.rotateColours(+2)
    print(necklace)
    
    print()
    necklace1 = Necklace()
    necklace2 = Necklace()
    necklace2.replaceBead(0, necklace1.getBead(necklace1.getNumBeads()-1))
    print(necklace1)
    print(necklace2)
    
    print()
    print("********* STATE TESTS ***********")
    print()
    instate0 = IntersectedNecklacesState(dimension=2, numBeads=20)
    print("state listifyed = "+str(instate0.listifyed()))
    instate1 = IntersectedNecklacesState(dimension=2, numBeads=20, initConf=instate0.listifyed())
    print("instate0 == instate1: "+str(instate0 == instate1))
    print(instate1)
    print("rotate 0, +1")
    instate1.rotateColours(0,1)
    print(instate1)
    print("rotate 1, -1")
    instate1.rotateColours(1,-1)
    print(instate1)
    print("rotate 1, +1")
    instate1.rotateColours(1,+1)
    print(instate1)
    print("rotate 0, -1")
    instate1.rotateColours(0,-1)
    print(instate1)
    print("is the same as it started = "+str(instate0 == instate1))
    print()
    print("Wrong number of necklaces:")
    initcl = [[2,1,1,1,1,1,1,1,1,1,3,2,2,2,2,2,2,2,2,2]]
    try:
        state = IntersectedNecklacesState(dimension=2, numBeads=20, initConf=initcl)
    except Exception as e:
        print(e)
    print()
    print("Wrong number of beads:")
    initcl = [[2,1,1,1,1,1,1,1,1,1,3,2,2,2,2,2,2,2,2,2],
                 [2,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4]]
    try:
        state = IntersectedNecklacesState(dimension=2, numBeads=20, initConf=initcl)
    except Exception as e:
        print(e)
    print()
    print("Wrong colour distribution:")
    initcl = [[2,1,1,1,1,1,1,1,1,1,3,2,2,2,2,2,2,2,2,2],
                 [2,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4]]
    try:
        state = IntersectedNecklacesState(dimension=2, numBeads=20, initConf=initcl)
    except Exception as e:
        print(e)
        
    print()
    print("Four rings with 32 beads each:")
    instate = IntersectedNecklacesState(dimension=4, numBeads=32)
    print(instate)
    
    print()
    print("********* PUZZLE TESTS ***********")
    print()
    instate = IntersectedNecklacesState(dimension=2, numBeads=20)
    print("Initial state:")
    print(instate)
    puzzle = PuzzleColares(instate)
    print("Is goal state: "+ str(puzzle.goal_test(instate)))
    print()
    # using the one from project statement
    goalState = [[2,1,1,1,1,1,1,1,1,1,3,2,2,2,2,2,2,2,2,2],
                 [2,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4]]
    instate = IntersectedNecklacesState(dimension=2, numBeads=20, initConf=goalState)
    print("Initial state:")
    print(instate)
    puzzle = PuzzleColares(instate)
    print("Is goal state: "+ str(puzzle.goal_test(instate)))
    
    print()
    actions = [random.choice(puzzle.actions(instate)) for i in range(5)]
    print("Actions:")
    for action in actions:
        print(action)
    
    result = exec(puzzle, puzzle.initial, actions)
    print("Final state:")
    print(result[0])
    print ("cost = "+str(result[1]))
    
    print()
    initStateList = result[0].listifyed()
    instate = IntersectedNecklacesState(dimension=2, numBeads=20, initConf=initStateList)
    puzzle = PuzzleColares(instate)
    print("Initial state:")
    print(puzzle.initial)
    print()
    print("Performing breadth-first search...")
    print()
    resultNode = breadth_first_tree_search(puzzle)
    print("Final state:")
    print(resultNode.state)
    print("Actions performed:")
    for a in resultNode.solution():
        print(a)
    print ("cost = "+str(resultNode.path_cost))
    
    