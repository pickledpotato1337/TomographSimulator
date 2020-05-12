import numpy as Numpy


#grid thousands by thousands fill circular, figure out how
#methods go horizintal
#go vertical
#go diagonal
#4 in total for each type of scan due to repetition in scanning paths
#output as 2d numpy array saved into csv
#method for creating output it as follows
#fill the array according to phantom
#traverse the array, creating a density map
#from each direction, apply formula for decrease of beam intensity
#I=I(0)e^(-ud)
#where Io-initial value of beam intensity
#u-absorption coefficient supplied by phantom
#distance per 1 grid is supplied to constructor
#initial beam intensity supplied to constructor
#beam density calculated goes to csv file


class ImageGrid:

    def __init__(self, resolution, densityPerGrid, beamIntensity):
        self.imageArray=Numpy.ones((resolution, resolution))
        self.density=densityPerGrid
        self.intensity=beamIntensity
        self.imageScan=[]
        self.dimension=resolution


    def FillPhantomTest(self):
        self.DeclareRectangle(20, 15, 15, 5, 18)
        self.DeclareCircle(15, 15, 15, 13)
        self.DeclareCircle(15, 15, 10, 10)
        return

    def ScanLinear(self):
        w=self.W()
        nw=self.NW()
        n=self.N()
        ne=self.NE()
        self.imageScan=[w, nw, n, ne]
        imageScanArray=Numpy.array(self.imageScan)


        #write to file
        Numpy.savetxt("image.csv", imageScanArray, delimiter="  ")
        #done
        return
    def ScanBeam(self, distanceToObject):
        wB=self.Wb(distanceToObject)
        nwB=self.NWb(distanceToObject)
        nB=self.Nb(distanceToObject)
        neB=self.NEb(distanceToObject)
        self.imageScan=[wB, nwB, nB, neB]
        imageScanArray = Numpy.array(self.imageScan)
        Numpy.savetxt("image.csv", imageScanArray, delimiter="  ")
        return

    def NE(self):
        neRes = []
        ctr1=0

        for i in reversed(range(self.dimension)):
            ctr1+=1
            lineRes = []
            j = self.dimension-1
            while ((i < self.dimension) & (j < self.dimension)):
                lineRes.append(self.AbsorptionFormula(self.imageArray[i, j]))
                i += 1
                j -= 1
            if (len(lineRes) > 0):
                aux = sum(lineRes)
                neRes.append(aux)
            else:
                neRes.append(0);

        return neRes

    def N(self):
        flipped=self.imageArray
        Numpy.transpose(flipped)
        nRes = []
        for i in range(self.dimension):
            aux=0
            for j in range(self.dimension):
                aux += self.AbsorptionFormula(self.imageArray[i,j])
            nRes.append(aux)

        return nRes

    def NW(self):
        nwRes = []
        for i in range(self.dimension):
            lineRes=[]
            j=0
            while ((i < self.dimension) & (j < self.dimension)):
                lineRes.append(self.AbsorptionFormula(self.imageArray[i, j]))
                i+=1
                j+=1
            if(len(lineRes)>0):
                aux=sum(lineRes)
                nwRes.append(aux)
            else:
                nwRes.append(0);

        return nwRes

    def W(self):
        wRes=[]
        for i in range(self.dimension):
            aux=0
            for j in range(self.dimension):
                aux+=self.AbsorptionFormula(self.imageArray[i,j])
            wRes.append(aux)

        return wRes

    #For beam scan

    def NEb(self, distanceToObject):
        nebRes=[]
        radius=distanceToObject+(self.dimension/2)
        xSource=radius*0.7071+(self.dimension/2)
        for i in range(self.dimension):
            for h in range(i):
                for k in range(self.dimension):
                    if (self.BeamFormula(0, i, xSource, xSource, k, h) == 1):
                        nebRes.append(self.AbsorptionFormula(self.imageArray[h, k]))
        for j in range(self.dimension):
            for m in range(j):
                for n in range(self.dimension):
                    if (self.BeamFormula(j, 0, xSource, xSource, n, m) == 1):
                        nebRes.append(self.AbsorptionFormula(self.imageArray[m, n]))



        return nebRes

    def Nb(self, distanceToObject):
        nbRes=[]
        for i in range(self.dimension):
             for h in range(i):
                for k in range(self.dimension//2):
                    if(self.BeamFormula(0,i, distanceToObject, self.dimension/2, k,h)==1):
                        nbRes.append(self.AbsorptionFormula(self.imageArray[h, k]))
        for j in range(self.dimension):
            for m in range(j):
                for n in range(self.dimension //2):
                    if (self.BeamFormula(j, 0, distanceToObject, self.dimension / 2, n, m) == 1):
                        nbRes.append(self.AbsorptionFormula(self.imageArray[m, n]))

        for l in range(self.dimension):
            for o in range(l):
                for p in range(self.dimension // 2):
                    if (self.BeamFormula(self.dimension-1, l, distanceToObject, self.dimension / 2, p, o) == 1):
                        nbRes.append(self.AbsorptionFormula(self.imageArray[o, p]))

        return nbRes


    def NWb(self, distanceToObject):
        nwbRes=[]
        radius = distanceToObject + (self.dimension / 2)
        xSource = radius * (-1)*0.7071 + (self.dimension / 2)
        ySource = radius  * 0.7071 + (self.dimension / 2)
        for j in range(self.dimension):
            for m in range(j):
                for n in range(self.dimension):
                    if (self.BeamFormula(j, 0, ySource, xSource, n, m) == 1):
                        nbRes.append(self.AbsorptionFormula(self.imageArray[m, n]))
        for l in range(self.dimension):
            for o in range(l):
                for p in range(self.dimension):
                    if (self.BeamFormula(self.dimension - 1, l, ySource, xSource, p, o) == 1):
                        nbRes.append(self.AbsorptionFormula(self.imageArray[o, p]))
        return nwbRes


    def Wb(self, distanceToObject):
        wbRes=[]
        for i in range(self.dimension):
            for h in range(i):
                for k in range(self.dimension // 2):
                    if (self.BeamFormula(i, 0, distanceToObject, self.dimension / 2, k, h) == 1):
                        wbRes.append(self.AbsorptionFormula(self.imageArray[h, k]))
        for j in range(self.dimension):
            for m in range(j):
                for n in range(self.dimension // 2):
                    if (self.BeamFormula(0, j, distanceToObject, self.dimension / 2, n, m) == 1):
                        wbRes.append(self.AbsorptionFormula(self.imageArray[m, n]))

        for l in range(self.dimension):
            for o in range(l):
                for p in range(self.dimension // 2):
                    if (self.BeamFormula(l, self.dimension - 1, distanceToObject, self.dimension / 2, p, o) == 1):
                        wbRes.append(self.AbsorptionFormula(self.imageArray[o, p]))
        return wbRes

    def DeclareRectangle(self, startX, startY, heigth, width, value):
        self.imageArray[startY:startY+heigth, startX:startX+width]=value
        return

    def DeclareCircle(self, centerX, centerY, radius, value):
        #for ranges inside of the radius, check if it's value is lower than
        gridElement=self.imageArray[centerY-radius:centerY+radius, centerX-radius:centerX+radius]
        for i in range(len(gridElement)):
            for j in range(len(gridElement[0])):
                if(self.CircleFormula(i,j, centerX, centerY, radius)==1):
                    gridElement[i,j]=value

        self.imageArray[centerY-radius:centerY+radius, centerX-radius:centerX+radius]=gridElement
        return

    def CircleFormula(self, yPos, xPos, centerX, centerY, radius):
        if((yPos-centerY)**2 + (xPos-centerX)**2<radius**2):
            return 1
        return 0


    def AbsorptionFormula(self, gridValue):
        multiplier=Numpy.exp(-1*gridValue*self.density)

        return self.intensity*multiplier

    def BeamFormula(self, xStart, yStart, yEmitter, xEmitter, xCoordinate, yCoordinate):
        yEmitter*=-1

        parameter=(yStart-yEmitter)/(xStart-xEmitter)
        addition=xStart*parameter+yStart
        if(xCoordinate*parameter+addition-yCoordinate<1.5):
            return 1
        return 0


