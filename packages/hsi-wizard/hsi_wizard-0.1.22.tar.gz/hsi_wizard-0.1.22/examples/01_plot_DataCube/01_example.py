import wizard
import numpy as np

# creating some radnome data
dc = wizard.DataCube(np.random.rand(20, 8, 9))

# plot data
wizard.plotter(dc)