import copy
from .simulation import Simulation
from .inventory import Inventory
from .demand import AggregateDemand

#we don't wait for inventory to age out and then order. we calculate
#future inventory levels based on FC and aging, and then schedule production
#to fill any anticipated shortages.

#forecast netting - to determine production scheduling
def forecast_netting(AD, inventory, fcst=None, lag=None):
    inv_copy = copy.deepcopy(inventory)
    s = inv_copy.sim

    #do not use LCD for now
    total_short = []
    print(f"--forecast netting - sim date = {inventory.sim.date}")
    for j in range(4):
        s.advance_time()
        short = 0
        d = 0

        for dcomp in AD.components:
            f = dcomp["fresh"]
            dmd = dcomp["forecast"] #net against forecast
            cust = dcomp["customer"]
                        
            starting = inv_copy.qtyavailable(f)
            short += inv_copy.sell_fifo(demand=dmd[j], fresh=f)
            ending = inv_copy.qtyavailable(f)
            d += dmd[j]
            filled = starting - ending
        total_short.append(short)
        print(f"|  sim_date = {inventory.sim.date:>2}, fnetdate = {s.date:>2}, demand = {d:>5}, short = {short:>5}")

    allshort = sum(total_short)
    print(f"--total short = {allshort}")
    return allshort



