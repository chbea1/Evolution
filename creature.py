import pygame
import random
import numpy as np
import pandas as pd
import math
sign = lambda x: (1, -1)[x < 0]
import time

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



class Creature:
    mutation_chance = 0.02
    death_chance = 0.01
    default_energy = 9000
    standard_variability = 1


    @staticmethod
    def born(world,speed,mv,cp,size,color,sense):
        self = Creature(world)
        self.world = world
        self.speed = speed
        self.speed_X = self.speed/2
        self.speed_y = self.speed/2
        self.movement_variability = mv
        self.current_position = cp.copy()
        self.energy = Creature.default_energy
        self.size = size
        self.color = color.copy()
        self.sense = sense
        return self

    def __init__(self,world,speed=3,color=[0,0,0]):
        self.world = world
        self.speed = speed
        self.speed_x = self.speed/2
        self.speed_y = self.speed/2
        self.movement_variability = Creature.standard_variability
        self.current_position = [random.randint(0,world.size[0]),random.randint(0,world.size[1])]
        self.energy = Creature.default_energy
        self.size = 3
        self.color = color
        self.sense = 50
        self.changeDirection()
        self.age = 100

    def reproduce(self):
        speed = self.speed
        size = self.size
        color = self.color.copy()
        sense = self.sense
        variablility = self.movement_variability

        if random.uniform(0,1) < Creature.mutation_chance:
            speed = random.uniform(0,10)
            color = list(np.random.choice(range(256), size=3))
            print("SPEED MUTATION")

            variablility = random.uniform(0,1)
            color = list(np.random.choice(range(256), size=3))
            print("VARIABILITY MUTATION")

            size = random.uniform(0,10)
            color = list(np.random.choice(range(256), size=3))
            print("SIZE MUTATION")



        self.world.register(Creature.born(self.world,abs(speed),variablility,self.current_position,abs(size),color,sense))

    def energy_per_move(self):
        # print("Energy : " + str(math.pow(self.speed,2) * math.pow(self.size,3)) +" -- size : "+ str(self.size))
        return math.pow(self.speed,2) * math.pow(self.size,3)


    def move(self):
        self.age -= 1
        if self.age < 0:
            self.world.unregister(self)
        if self.energy < 0:
            self.world.unregister(self)
        self.energy -= self.energy_per_move()

        x,y = self.current_position
        near_food = self.world.near(x,y,self.sense)
        # if near_food:
        #     nx = x - near_food[0]
        #     ny = y - near_food[1]
        # else:
        nx = x - self.speed_x
        ny = y - self.speed_y


        # self.changeDirection()

        if random.uniform(0,1) < self.movement_variability/10:
            self.speed_x = -self.speed_x
        if random.uniform(0,1) < self.movement_variability/10:
            self.speed_y = -self.speed_y

        if nx < self.world.size[0] and nx > 0 :
            self.current_position[0] = (int)(nx)
        else:
            self.speed_x = -self.speed_x
        if ny < self.world.size[1] and ny > 0:
            self.current_position[1] = (int)(ny)
        else:
            self.speed_y = -self.speed_y


        if self.size > 5:
            foodAt = 0
        else:
            foodAt = self.world.foodAt(self.current_position[0],self.current_position[1])
        othersAt = self.world.creatureAt(self)


        if foodAt > 0 or othersAt > 0:
            if self.energy > Creature.default_energy * 0.5:
                self.reproduce()
            else:
                self.energy +=  100 * foodAt
                self.energy += 200 * othersAt
                # print("energy: " + str(self.energy))

        # print("Y:" + str(self.speed_y))
        # print("X:" + str(self.speed_x))
        pygame.draw.circle(self.world.screen, self.color, self.current_position, (int)(self.size))


    def changeDirection(self):
        prod = random.uniform(0, 1)
        if prod < self.movement_variability:
            change = random.uniform(-1,1)
            self.speed_y += change
            self.speed_x += change
