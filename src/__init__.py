'''
the presence of __init__.py in src makes src a package rather than just a folder

this enables relative imports within src

'''

#preloading modules using relative imports

from .inventory import Lot, Inventory
from .demand import IntermittentDemand
from .simulation import Simulation


