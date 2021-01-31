import numpy as np
import random

class Person:
    def __init__(self, area, infection_rate, fatality_rate, recover_period, death_period, intelligent=False):
        # Position variables
        self.x = random.randrange(0, area.shape[1])
        self.y = random.randrange(0, area.shape[0])

        # Intelligent
        self.intelligent = intelligent
        
        # Status
        self.infected = False
        self.inmune = False
        self.alive = True
        self.period = 0

        # Shared variables
        self.infection_rate = infection_rate
        self.fatality_rate = fatality_rate
        self.recover_period = recover_period
        self.death_period = death_period

        self.set_position(area)

    def set_position(self, area):
        if self.infected and self.alive:
            # Set infection area in current position
            area[
                (self.y-int(self.infection_rate*100)):(self.y+int(self.infection_rate*100)), 
                (self.x-int(self.infection_rate*100)):(self.x+int(self.infection_rate*100))] = 1
            self.period += 1

    def move(self, area):
        if self.infected:
            # Clear previous infection area
            area[
                (self.y-int(self.infection_rate*100)):(self.y+int(self.infection_rate*100)), 
                (self.x-int(self.infection_rate*100)):(self.x+int(self.infection_rate*100))] = 0
        
        if self.alive:
            if self.intelligent:
                pos = area[
                    np.maximum(0, self.y-10):np.minimum(area.shape[0], self.y+10), 
                    np.maximum(0, self.x-10):np.minimum(area.shape[1], self.x+10)]
                    
                # Find minimum infection area 
                try:
                    optimal_move = np.where(pos == np.min(pos))

                    # We make sure that the people won't stack together
                    i = random.randrange(0, len(optimal_move[0]))
                   
                    y = optimal_move[0][i] 
                    x = optimal_move[1][i] 

                    self.y = np.minimum(area.shape[0]-1, np.maximum(0, self.y + y - pos.shape[0] // 2))
                    self.x = np.minimum(area.shape[1]-1, np.maximum(0, self.x + x - pos.shape[1] // 2))

                except Exception:
                    accepted = False
                    while not accepted:
                        x, y = random.randrange(-10, 10), random.randrange(-10, 10)
                        try:
                            area_check = area[self.y+y, self.x+x]
                            self.y = (self.y + y) % area.shape[0] 
                            self.x = (self.x + x) % area.shape[1]
                            accepted = True
                        except Exception:
                            pass
            else:
                # Move randomly
                accepted = False
                while not accepted:
                    x, y = random.randrange(-10, 10), random.randrange(-10, 10)
                    try:
                        area_check = area[self.y+y, self.x+x]
                        self.y = (self.y + y) % area.shape[0] 
                        self.x = (self.x + x) % area.shape[1]
                        accepted = True
                    except Exception:
                        pass

        self.set_position(area)

    def infection_risk(self, area):
        if self.alive and (not self.infected) and (not self.inmune) and (area[self.y, self.x] >= 1):
            self.infected = True
            self.set_position(area)

            return True

    def death_risk(self, area):
        if self.infected and random.uniform(0, 1 + self.fatality_rate) >= 1 and (self.period >= self.death_period):
            self.alive = False
            self.infected = False

            # Clear previous infection area
            area[
                (self.y-int(self.infection_rate*100)):(self.y+int(self.infection_rate*100)), 
                (self.x-int(self.infection_rate*100)):(self.x+int(self.infection_rate*100))] = 0

            return True

    def recover(self, area):
        if self.infected and (random.uniform(0, 1 + (1-self.fatality_rate))) >= 1 and (self.period >= self.recover_period):
            self.infected = False
            self.inmune = True

            # Clear previous infection area
            area[
                (self.y-int(self.infection_rate*100)):(self.y+int(self.infection_rate*100)), 
                (self.x-int(self.infection_rate*100)):(self.x+int(self.infection_rate*100))] = 0

            return True