class Simulation:
    def __init__(self):
        self.date = 0
    
    def advance_time(self, increment=1):
        self.date += increment