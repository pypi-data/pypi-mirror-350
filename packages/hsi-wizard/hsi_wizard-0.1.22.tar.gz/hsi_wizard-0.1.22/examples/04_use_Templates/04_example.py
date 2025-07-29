import wizard
import numpy as np


# create a dc
dc = wizard.DataCube(np.random.rand(20, 640, 460))

print('DataCube:')
print(dc)

# load and execute the template
dc.execute_template('03_example.yml')

print('Processed Datacube:')
print(dc)