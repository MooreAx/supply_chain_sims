#simulation file
#import classes
from src import *
import pandas as pd

#define demand
ON = IntermittentDemand(customer = "ON", rate = 0.3, mean = 1000, stdev = 100, fresh=12, fcbias = 0) #12 weeks fresh = 90 days
SK = IntermittentDemand(customer = "SK", rate = 1, mean = 50, stdev = 10, fresh=50, fcbias = 0) #12 weeks fresh = 90 days
MB = IntermittentDemand(customer = "MB", rate = 1, mean = 50, stdev = 10, fresh=50, fcbias = 0) #12 weeks fresh = 90 days


IntDemand_list = []
IntDemand_list.append(ON)
IntDemand_list.append(SK)
IntDemand_list.append(MB)

ss = get_safetystock_1(IntDemand_list, leadtime=4, service_level=0.95)

print("\n running ss2")
ss2 = get_safetystock_2(IntDemand_list, leadtime=4, service_level=0.95)

#i think we need to do safety stock per freshness requirement, not just total demand,
#and then reorder if onhand is less than ss for any of the components.

#generate demand for 1 year
ON50 = ON.generate(10, seed=3)
SK50 = SK.generate(10, seed=4)

AD = AggregateDemand()
AD.add(ON50)
AD.add(SK50)

#this aggregates demand and converts to data frame, with column names = fresh requirement
print("Aggregate demand:")
print(pd.DataFrame(AD.aggregate_demand))

print("\nAggregate forecast:")
print(pd.DataFrame(AD.aggregate_forecast))


# Initialize sales_log as a dictionary of lists (columns)
sales_log = {
    "date": [],
    "customer": [],
    "filled": [],
    "short": []
}

#create sim instance for date tracking
sim = Simulation()

#set starting inventory:
Inv = Inventory(sim)
Inv.replenish(qty=5000, thc=0.3, leadtime=0)

#simulate

horizon = len(AD.components[0]["demand"])

for i in range(horizon):
    sim.advance_time()

    #run forecast netting
    short = forecast_netting(AD, Inv)
    
    if short > 0: #order to cover short
        Inv.replenish(qty=5000, thc=0.3, leadtime=4)     
    
    for dcomp in AD.components:
        f = dcomp["fresh"]
        dmd = dcomp["demand"]
        cust = dcomp["customer"]
                       
        starting = Inv.qtyavailable(f)
        short = Inv.sell_fifo(demand=dmd[i], fresh=f)
        ending = Inv.qtyavailable(f)
        d = dmd[i]
        filled = starting - ending

        #log sale
        sales_log["date"].append(sim.date)
        sales_log["customer"].append(cust)
        sales_log["filled"].append(filled)
        sales_log["short"].append(short)

        print(f"day = {sim.date:>4}, customer = {cust}, fresh = {f:>2}, demand = {d:>5}, starting = {starting:>5}, filled = {filled:>5}, ending = {ending:>5}, short = {short:>5}")
      

# Convert the dictionary to a pandas DataFrame
df_sales = pd.DataFrame(sales_log)

# Print the resulting DataFrame
print(df_sales)

Inv.print_inventory()

total_demand = sum([sum(dcomp["demand"]) for dcomp in AD.components])
print(f"Total demand = {total_demand}")
print(f"Total sales = {sum(sales_log['filled'])}")
print(f"Total short = {sum(sales_log['short'])}")
print(f"Fill rate = {round((sum(sales_log['filled'])/total_demand), 3)}")