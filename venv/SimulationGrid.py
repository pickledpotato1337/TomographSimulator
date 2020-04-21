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
        tangent=2*distanceToObject/self.dimension

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

    def NEb(self):
        return
    def Nb(self):
        for i in range(self.dimension):
            westEdge=self.imageArray[i,0]
            duplicate=i
            j=0
            #while((i>0)&(j>=0)):
        return

        return
    def NWb(self):
        return
    def Wb(self):
        return

    def DeclareRectangle(self, startX, startY, heigth, width, value):
        self.imageArray[startY:startY+heigth, startX:startX+heigth]=value
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

    def BeamFormula(self, xStart, yStart, heightToEmitter, tangent, xCoordinate, yCoordinate):
        return 1
        return 0

