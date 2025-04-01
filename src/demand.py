import random
import numpy as np

def mround(x, multiple):
    return [round(n / multiple) * multiple for n in x]

class IntermittentDemand:
    """
    This class generates intermittent demand using a Poisson distribution for the number of purchase orders (POs)
    and a normal distribution for the units per PO."
    """

    def __init__(self, rate, mean, stdev, fresh):
        self.rate = rate # poisson rate, i.e. lambda
        self.mean = mean    # mean (normal distribution)
        self.stdev = stdev  # standard deviation (normal distribution)
        self.fresh = fresh

    def generate(self, n, seed = None):
        # Returns total units demanded for n perids

        rng = np.random.default_rng(seed = seed) #random number generator

        pos = []
        pos_units = []
        pos_totals = []

        for _ in range (n):
            #get pos per period (Poisson)
            count = rng.poisson(self.rate)
            pos.append(count)

            #get units per po (normal)
            if count > 0:
                po_units = mround(list(rng.normal(self.mean, self.stdev, size=count)), 6)
                po_units = [6 if x < 0 else x for x in po_units] #replace negative values with 6
            else:
                po_units = [0]

            pos_units.extend(po_units)
            
            #get total units
            pos_totals.append(sum(po_units))

        print(pos)
        print(pos_units)
        print(pos_totals)
        return pos_totals

'''

example = IntermittentDemand(rate = 0.4, mean = 100, stdev = 100, fresh=30)
example.generate(20)


ON = IntermittentDemand(rate = 0.4, mean = 1000, stdev = 100, fresh=30)
SK = IntermittentDemand(rate = 0.4, mean = 100, stdev = 10, fresh=30)

ON.generate(1)
SK.generate(1)

print(SK.fresh)

'''