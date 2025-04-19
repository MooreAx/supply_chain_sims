#simulation file
#import classes
from src import *
import pandas as pd
import copy

#define demand
ON = IntermittentDemand(customer = "ON", rate = 0.3, mean = 1000, stdev = 100, fresh=12, fcbias = 0) #12 weeks fresh = 90 days
SK = IntermittentDemand(customer = "SK", rate = 1, mean = 50, stdev = 10, fresh=50, fcbias = 0) #12 weeks fresh = 90 days

MDL = (1000*0.3 + 50*1)*4 #mean demand during lead time
SS = 500 #safety stock


#generate demand for 1 year
ON50 = ON.generate(1000, seed=3)
SK50 = SK.generate(1000, seed=4)

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

#we don't wait for inventory to age out and then order. we calculate
#future inventory levels based on FC and aging, and then schedule production
#to fill any anticipated shortages.

#forecast netting - to determine production scheduling
def forecast_netting(inventory, fcst=None, lag=None):
    inv_copy = copy.deepcopy(inventory)
    s = inv_copy.sim

    #do not use LCD for now
    total_short = []
    print(f"--forecast netting - sim date = {sim.date}")
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
        print(f"|  sim_date = {sim.date:>2}, fnetdate = {s.date:>2}, demand = {d:>5}, short = {short:>5}")

    allshort = sum(total_short)
    print(f"--total short = {allshort}")
    return allshort


#simulate

horizon = len(AD.components[0]["demand"])

for i in range(horizon):
    sim.advance_time()

    #run forecast netting
    short = forecast_netting(Inv)
    
    if short > 0: #order to cover short
        Inv.replenish(qty=5000, thc=0.3, leadtime=4)

    #contiuous inventory review
    #if Inv.qtyavailable(max_age = 12) < (MDL+SS):
        
    
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