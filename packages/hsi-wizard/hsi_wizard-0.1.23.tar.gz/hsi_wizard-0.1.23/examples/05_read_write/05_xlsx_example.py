import os

import wizard
import numpy as np
from wizard._utils._loader import xlsx

# define dc
dc = wizard.DataCube(np.random.rand(22, 10,8))

# wrtie dc to xlsx file
xlsx._write_xlsx(dc, filename='test.xlsx')

# read dc from xlsx
new_dc = xlsx._read_xlsx('test.xlsx')

# compare data
print(dc.shape)
print(new_dc.shape)

# delete files
os.remove('test.xlsx')

