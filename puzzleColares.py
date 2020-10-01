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
        return "\u001b[38;5;"+str(self._colour)+"mO\u001b[38;5;m"



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
        numBeads: number of beads in each necklace. Must be even number
        intersection: how many beads are in the arch resulting from the intersection.
            Has to be an odd integer smaller than numBeads/2-3
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
                
    def __init__(self, dimension=2, numBeads=20, intersection=3, initConf=None):

        self._dimension = dimension
        self._numBeads = numBeads
        self._intersection = intersection
            
        if initConf != None:
                raise NotImplementedError
        
        self._generateRandomConfiguration()

    
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
                try:
                    scr[l][c] = str(bead)
                except IndexError:
                    print("i:"+str(i)+" j:"+str(j))
                    print("l:"+str(l)+" c:"+str(c))
                    raise IndexError
        return "\n".join(["".join(line) for line in scr])

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
    instate = IntersectedNecklacesState(dimension=2, numBeads=20, intersection=3)
    print(instate)
    instate.rotateColours(0,1)
    print(instate)
    instate.rotateColours(1,-1)
    print(instate)
    
    