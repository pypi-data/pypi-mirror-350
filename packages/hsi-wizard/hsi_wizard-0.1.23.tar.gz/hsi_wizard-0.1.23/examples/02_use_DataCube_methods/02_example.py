import wizard
import numpy as np

# create a DataCube
dc = wizard.DataCube(np.random.rand(20, 640, 460))
dc.set_name('Test DataCube')

# plot DataCube
print(dc)

# resize DataCube
dc.resize(500,500)

# print dc
print(dc)