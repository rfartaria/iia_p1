# -*- coding: utf-8 -*-

import random

class Bead(object):
    
    def __init__(self, colour):
        self._colour = colour

    def getColour(self):
        return self._colour
    
    def setColour(self, colour):
        self._colour = colour

    def __str__(self):
        return "\u001b[38;5;"+str(self._colour)+"m"+ \
            str(self._colour)+ \
            "\u001b[38;5;m"



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


    """ Rotate colours clockwise (negative) """
    def rotateColoursRight(self):
        colours = [b.getColour() for b in self._beads]
        colours = [colours[-1]] + colours[0:self._numBeads-1]
        for i in range(self._numBeads):
            self._beads[i].setColour(colours[i])


    """ Rotate colours counter-clockwise (positive) """
    def rotateColoursLeft(self):
        colours = [b.getColour() for b in self._beads]
        colours = colours[1:self._numBeads]+[colours[0]]
        for i in range(self._numBeads):
            self._beads[i].setColour(colours[i])

    def __str__(self):
        return " ".join([str(x) for x in self._beads])+"\u001b[0m"



class IntersectedNecklacesState(object):
    
    """ dimension: number of necklaces
        numBeads: number of beads in each necklace. Must be even number
        intersection: how many beads are in the arch resulting from the intersection.
            Has to be an odd integer smaller than numBeads/2-3
        initConf: list of Necklace instances
            conditions for a valid configuration are:
                1. each necklace has dimension numBeads
                2. each neclace shares two beads with its neghbours compatible with
                    intersection parameter
                3. total number of colours defined in necklaces set is 2*dimension
                4. color distribution is numbeads/2 for two colours and numbeads/2-1 for the remaining ones"""
    def __init__(self, dimension=2, numBeads=20, intersection=3, initConf=None):

        self._dimension = dimension
        self._numBeads = numBeads
        self._intersection = intersection
            
        if initConf != None:
                raise NotImplementedError
        
        self._generateRandomConfiguration()

    
    def _generateRandomConfiguration(self):
            # generate independent necklaces
            self._necklaces = [Necklace(colourBeadsDist={1:self._numBeads}) for i in range(self._numBeads)]
            
            # intersect necklaces
            for i in range(1,len(self._necklaces)):
                leftNecklace = self._necklaces[i-1]
                rightNecklace = self._necklaces[i]
                leftNecklace_k = int(self._numBeads/2) + self._intersection + 1
                leftNecklace_j = leftNecklace_k - self._intersection - 1
                rightNecklace_j = 0
                rightNecklace_k = self._intersection + 1
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
                beads += necklace.getBeads()
            beads = set(beads) # remove duplicates
            beads = list(beads)
            while len(colours) > 0:
                c = random.choice(colours)
                colours.remove(c)
                b = beads.pop()
                b.setColour(c)
    
    def __str__(self):
        

if __name__ == "__main__":
    
    necklace = Necklace()
    print(necklace)
    necklace.rotateColoursRight()
    print(necklace)
    necklace.rotateColoursLeft()
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
    instate = IntersectedNecklacesState(dimension=2, numBeads=20, intersection=3)
    print(instate)
    
    