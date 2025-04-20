import scipy.stats as st
from .demand import IntermittentDemand, AggregateDemand

def get_safetystock_1(intdmd, leadtime, service_level):
    #calculates safety stock for total demand, ignoring freshness requirement

    total_variance = 0
    total_mean = 0
    for component in intdmd:
        total_variance += component.variance_per_period()
        total_mean += component.mean * component.rate #mean demand per period

    #variance of total demand over the lead time:
    sigma_l = (total_variance * leadtime)**0.5
    mean_l = total_mean * leadtime

    #get zscore from service level
    z = st.norm.ppf(service_level)
    ss = z * sigma_l

    print("\n")
    print(f"Mean lead time demand =     {mean_l}")
    print(f"stdev lead time demand =    {sigma_l}")
    print(f"Z score =                   {z}")
    print(f"Safety stock =              {ss}")
    print("\n")
    
    return ss

def get_safetystock_2(intdmd, leadtime, service_level):
    #calculates safety stock per freshness requirement
    pass