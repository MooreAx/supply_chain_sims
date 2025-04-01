#simulation file


#import classes
from inventory import Inventory, Lot
from demand import IntermittentDemand

#define demand
Demand = IntermittentDemand(rate = 0.4, mean = 1000, stdev = 100, fresh=12) #12 weeks fresh = 90 days
#generate demand for 1 year
D100 = Demand.generate(51, seed=1)

#set starting inventory:
I = Inventory()
I.replenish(qty=5000, thc=0.3, leadtime=0, simdate=0)

for simdate in range(1, 50):
    starting = I.qtyavailable(Demand.fresh, simdate)
    short = I.sell_fifo(demand=D100[simdate], fresh=Demand.fresh, simdate=simdate)
    ending = I.qtyavailable(Demand.fresh, simdate)
    dmd = D100[simdate]
    filled = starting - ending

    print(f"day = {simdate}, \tdemand = {dmd}, \tstarting = {starting}, \tfilled = {filled}, \tending = {ending}, \tshort = {short}")

