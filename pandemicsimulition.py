import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from celluloid import Camera 

from person import Person

class Pandemic:
    def __init__(self, area_shape, num_of_people, infection_rate, fatality_rate, recover_period, death_period, intelligent=False):
        self.area = np.zeros(area_shape)
        self.num_of_people = num_of_people
        self.infection_rate = infection_rate
        self.fatality_rate = fatality_rate
        self.recover_period = recover_period
        self.death_period = death_period
        self.intelligent = intelligent

        self.infections = []
        self.recoveries = []
        self.deaths = []

        self.people = self.generate_people()


    def generate_people(self):
        arr = []
        for i in range(self.num_of_people):
            arr.append(Person(self.area, self.infection_rate, self.fatality_rate, self.recover_period, self.death_period, self.intelligent))
        return arr


    def run(self, print_resaults=True, animate=False):

        infections = 0
        recoveries = 0
        deaths = 0
        
        self.people[0].infected = True
        self.people[0].set_position(self.area)
        infections += 1

        self.infections.append(infections)
        self.recoveries.append(recoveries)
        self.deaths.append(deaths)

        fig = plt.figure()
        camera = Camera(fig)

        while infections != recoveries + deaths:
            for person in self.people:
                person.move(self.area)
    
                if person.infection_risk(self.area):
                    infections += 1

                if person.death_risk(self.area):
                    deaths += 1

                if person.recover(self.area):
                    recoveries += 1

                if animate:
                    color = '#0083ff'
                    if not person.alive:
                        color = '#82878c'
                    elif person.infected:
                        color = '#ff0000' 
                    plt.scatter(person.x, person.y, marker='.' if person.alive else 'x', color=color)
            camera.snap()

            self.infections.append(infections)
            self.recoveries.append(recoveries)
            self.deaths.append(deaths)

            if print_resaults:
                print(f'Current infecteions: {infections - (recoveries + deaths)} | Infections: {infections} | Recoveries: {recoveries} | Deaths: {deaths}')
            
        if animate:
            animation = camera.animate()
            animation.save('pandemic.gif', fps=5, writer = 'imagemagick')


    def reset(self):
        self.people = self.generate_people()
        self.area = np.zeros(self.area.shape)

        self.infections = []
        self.recoveries = []
        self.deaths = []


    def plot_resaults(self):
        plt.plot(self.infections, color='#2d70ff', label='Infections')
        plt.plot(self.recoveries, color='#ffab2d', label='Recoveries')
        plt.plot(self.deaths, color='#ff2d2d', label='Deaths')
        
        plt.legend()
        plt.grid()
        plt.show()


    def save(self, filename):
        df = pd.DataFrame()

        df['Infections'] = self.infections
        df['Recoveries'] = self.recoveries
        df['Deaths'] = self.deaths

        df.to_csv(filename)