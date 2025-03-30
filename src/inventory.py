class Lot:
    def __init__(self, id, size, thc, leadtime, dateordered):
        self.id = id
        self.size = size
        self.thc = thc
        self.leadtime = leadtime
        self.dateordered = dateordered

        #new properties
        self.dateavailable = dateordered + leadtime
        self.qtyavailable = size
        self.qtysold = 0
    
    @property
    def available(self):
        return simdate >= self.dateavailable #simdate global variable
    
    @property
    def age(self):
        return simdate - self.dateavailable #simdate global variable
    
    #Methods
    def makesale(self, qty):
        if not self.available:
            raise Exception(f"Lot unavailable until {self.dateavailable}")
        elif self.qtyavailable < qty:
            raise Exception(f"Requesting {qty} but only {self.qtyavailable} available")
        else:
            self.qtyavailable -= qty
            self.qtysold += qty

    def __repr__(self):
        return f"Lot(id={self.id}, size={self.size}, thc={self.thc}, leadtime={self.leadtime}, dateordered={self.dateordered})"
    

class Inventory:
    def __init__(self):
        self.lots = [] #list of Lot objects

    def replenish(self, qty, thc, leadtime):
        #create a new lot and add it to the inventory
        lot = Lot(id=len(self.lots), size=qty, thc=thc, leadtime=leadtime, dateordered=simdate) #simdate global variable
        self.lots.append(lot)
        return lot
    
    def sell_fifo(self, demand):
        #make a sale from the oldest lots
        self.lots.sort(key=lambda lot: lot.age, reverse=True) #oldest first
        return self.fill_order(demand)
        
    def sell_lifo(self, demand):
        #make a sale from the newest lots
        self.lots.sort(key=lambda lot: lot.age, reverse=False) #youngest first
        return self.fill_order(demand)

    def sell_bifo(self, demand):
        #make a sale from highest-thc lots
        self.lots.sort(key=lambda lot: lot.thc, reverse=True) #highest thc first
        return self.fill_order(demand)

    def fill_order(self, demand):
        unfilled = demand
        filled = 0
        for lot in self.lots:
            if lot.available:
                if lot.qtyavailable >= unfilled:
                    lot.makesale(unfilled)
                    filled += unfilled
                    unfilled = 0
                    break #order fully filled
                elif lot.qtyavailable > 0:
                    lot.makesale(lot.qtyavailable)
                    filled += lot.qtyavailable
                    unfilled -= lot.qtyavailable
        return unfilled

    def __repr__(self):
        return f"Inventory(lots={self.lots})"