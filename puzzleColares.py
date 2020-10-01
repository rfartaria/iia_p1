# -*- coding: utf-8 -*-

import random
from searchPlus import Problem

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


    def removeBead(self, k):
        if (isinstance(k, int)):
            self._beads.pop(k)
            self._numBeads -= 1
            return
        if (isinstance(k, Bead)):
            self._beads.remove(k)
            self.numBeads -= 1
            return
        raise "k is neither [int] or [Bead]!"


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
            
            # TODO: validate initConf as specified in project statement
            
            for i in range(self._dimension):
                clist = initConf[i]
                necklace = self._necklaces[i]
                for j in range(self._numBeads):
                    necklace.getBead(j).setColour(clist[j])
    
    
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
        selfOrderedBeads = []
        for necklace in self._necklaces:
            for b in necklace.getBeads():
                if b not in selfOrderedBeads:
                    selfOrderedBeads.append(b)
        oOrderedBeads = []
        for necklace in o.getNecklaces():
            for b in necklace.getBeads():
                if b not in oOrderedBeads:
                    oOrderedBeads.append(b)
        selfOrderedColours = [b.getColour() for b in selfOrderedBeads]
        oOrderedColours = [b.getColour() for b in oOrderedBeads]
        return tuple(selfOrderedColours) == tuple(oOrderedColours)


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
        return [('rotate', i, +1) for i in range(len(state.getNecklaces()))] + \
               [('rotate', i, -1) for i in range(len(state.getNecklaces()))]

    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        dimension = len(state.getNecklaces())
        numBeads = state.getNecklaces()[0].getNumBeads()
        newState = IntersectedNecklacesState(dimension=len(state.getNecklaces()), \
                        numBeads=state.getNecklaces()[0].getNumBeads(), \
                        initConf=state.listifyed())
        newState.rotateColours(iNecklace=action[1], direction=action[2])
        return newState
                                             
if __name__ == "__main__":
    random.seed(1234567)
    
    necklace = Necklace()
    print(necklace)
    necklace.rotateColours(-2)
    print(necklace)
    necklace.rotateColours(+2)
    print(necklace)
    
    # print("empty necklace:")
    # necklace = Necklace(colourBeadsDist={})
    # print(necklace)
    
    print()
    necklace1 = Necklace()
    necklace2 = Necklace()
    necklace2.replaceBead(0, necklace1.getBead(necklace1.getNumBeads()-1))
    print(necklace1)
    print(necklace2)
    
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
    instate = IntersectedNecklacesState(dimension=4, numBeads=32)
    print(instate)
    
    print()
    print("********* PUZZLE TESTS ***********")
    print()
    instate = IntersectedNecklacesState(dimension=2, numBeads=20)
    print("Initial state:")
    print(instate)
    puzzle = PuzzleColares(instate)
    print(puzzle.actions(instate))
    
    