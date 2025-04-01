#simulation file
#import classes
from inventory import Inventory, Lot
from demand import IntermittentDemand

#define demand
Demand = IntermittentDemand(rate = 0.4, mean = 1000, stdev = 100, fresh=12) #12 weeks fresh = 90 days

#generate demand for 1 year
D100 = Demand.generate(51, seed=1)

#create sim instance for date tracking
sim = Simulation()

#set starting inventory:
Inv = Inventory(sim)
Inv.replenish(qty=5000, thc=0.3, leadtime=0)

for i in range(50):
    sim.advance_time()

    starting = Inv.qtyavailable(Demand.fresh)
    short = Inv.sell_fifo(demand=D100[i], fresh=Demand.fresh,)
    ending = Inv.qtyavailable(Demand.fresh)
    dmd = D100[i]
    filled = starting - ending

    print(f"day = {sim.date}, \tdemand = {dmd}, \tstarting = {starting}, \tfilled = {filled}, \tending = {ending}, \tshort = {short}")

