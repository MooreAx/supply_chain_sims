import random
import numpy as np

def mround(x, multiple):
    return [round(n / multiple) * multiple for n in x]

class IntermittentDemand:
    def __init__(self, rate, stdev, mean):
        self.rate = rate # poisson rate, i.e. lambda (Poisson)
        self.stdev = stdev  # standard deviation (normal)
        self.mean = mean    # mean (normal)

    def generate(self, n):
        rng = np.random.default_rng(seed = 2) #random number generator

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

example = IntermittentDemand(rate = 0.4, stdev = 100, mean = 100)
example.generate(20)

