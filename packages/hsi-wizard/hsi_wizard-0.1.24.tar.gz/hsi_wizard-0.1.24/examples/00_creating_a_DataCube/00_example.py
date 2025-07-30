import wizard
import numpy as np

# creating some data with the shape 20, 8, 9
some_randome_data = np.zeros(shape=(20, 8, 9))

# create a DataCube
dc = wizard.DataCube(some_randome_data, name='Hello DataCube')

# print dc
print(dc)

