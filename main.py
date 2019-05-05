# Import a library of functions called 'pygame'
import pygame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import time
from creature import Creature,World


sign = lambda x: (1, -1)[x < 0]

class World:
    poplimit = 500
    food_limit = 200

    def __init__(self):
        self.ticker = time.time()

        self.size = (800,600)
        self.screen = pygame.display.set_mode(self.size)
        self.limit = World.food_limit
        self.init_food()

    def init_food(self):
        self.food = []
        for i in range(0,self.limit):
            self.food.append([random.randint(0,self.size[0]),random.randint(0,self.size[1])])

    def near(self,x,y,range):
        for f in self.food:
            if x < f[0] + range and x > f[0] - range and y  < f[1] + range and y > f[1] - range:
                return (x - f[0] , y - f[1])
        return None

    def creatureAt(self,creature):
        x,y = creature.current_position
        count = 0
        for pop in self.population:
            if creature != pop:
                f = pop.current_position
                if  pop.size < creature.size and x != f[0] and y != f[1] and x < f[0] + 20 and x > f[0] - 20 and y < f[1] + 20 and y > f[1] - 20:
                    self.population.remove(pop)
                    count += 1
        return count

    def foodAt(self,x,y):
        count = 0
        for f in self.food:
            if x < f[0] + 20 and x > f[0] - 20 and y  < f[1] + 20 and y > f[1] - 20 :
                self.food.remove(f)
                count += 1
        return count

    def refresh(self):

        self.food.append([random.randint(0, self.size[0]), random.randint(0, self.size[1])])
        self.food.append([random.randint(0, self.size[0]), random.randint(0, self.size[1])])
        self.food.append([random.randint(0, self.size[0]), random.randint(0, self.size[1])])
        self.screen.fill((255, 255, 255))
        for f in self.food:
            pygame.draw.circle(self.screen, (0,255,0), f, 2)


    def populate(self,creatures):
        self.population = creatures

    def unregister(self,creature):
        self.population.remove(creature)

    def register(self,creature):
        if len(self.population) < World.poplimit:
            self.population.append(creature)

    def population_speeds(self):
        speeds = []
        for p in self.population:
            speeds.append(p.speed)
        d = {'x': list(range(0,len(speeds))), 'y': speeds}
        pdnumsqr = pd.DataFrame(d)
        return pdnumsqr

    def average_speed(self):
        sum = 0
        for p in self.population:
            sum += p.speed
        return sum/len(self.population)

    def population_sizes(self):
        speeds = []
        for p in self.population:
            speeds.append(p.size)
        d = {'x': list(range(0,len(speeds))), 'y': speeds}
        pdnumsqr = pd.DataFrame(d)
        return pdnumsqr



pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

world = World()

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()


world.populate([Creature(world,speed=1,color=[0,0,0])])
while not done:
    clock.tick(30)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                sns.barplot(x='x', y='y', data=world.population_speeds())
                plt.show()
            if event.key == pygame.K_w:
                sns.barplot(x='x', y='y', data=world.population_sizes())
                plt.show()

    world.refresh()
    for creature in world.population:
        creature.move()
    pygame.display.update()
    pygame.display.flip()


# Be IDLE friendly
pygame.quit()