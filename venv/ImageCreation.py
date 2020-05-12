import SimulationGrid as Sg
import numpy as np
img1=Sg.ImageGrid(40, 1, 10)

img1.FillPhantomTest()

img1.ScanLinear()

img1.ScanBeam(21)