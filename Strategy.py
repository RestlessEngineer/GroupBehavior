from RobotFileld import *
from Graph import * 
import numpy as np
import random

class Strategy:
    # define the best strategy
    def choose_strategy(self, profit_matix) -> int:
        pass
        

class NashStrategy(Strategy): 
    # min max trategy from game theory https://en.wikipedia.org/wiki/Nash_equilibrium
    def choose_strategy(self, profit_matix) -> int:
    
        min_j = np.min(profit_matix, axis=1)
        max_i = np.max(profit_matix, axis=0)
        
        # max_i min_j (mtx_{ij})
        maxmin = np.max(min_j)

        # max_i min_j (mtx_{ij})
        minmax = np.min(max_i)

        if(maxmin != minmax):
            raise Exception(f'not pure solution. minmax: {minmax}, maxmin: {maxmin}')

        strategies = []
        for (i, val) in enumerate(min_j):
            if val == minmax:
                strategies.append(i)

        if len(strategies) == 1:
            return int(strategies[0])

        #if there is more than one solution we have to chose one of them accidentally
        return int(random.choice(strategies))


class CalculateProfit:
    
    def __call__(self, field: RobotField, robot, robots) -> tuple[list[Location], list[float]]:
        pass


class SimpleProfit(CalculateProfit):

    def __call__(self, field: RobotField, ways: list[Location], main_way) -> tuple[list[Location], list[float]]:    
    
        profit_coords = {}
        profits = []
        for (i, way) in enumerate(ways):
            came_from, cost_so_far = a_star_search(field, main_way, way)
            path = reconstruct_path(came_from, main_way, way)
            profit = 2 - len(path)
            profits.append(profit)
            profit_coords[i] = way

        return (profit_coords, profits)


class ZeroCenterProfit(CalculateProfit):
    
    def __call__(self, field: RobotField, ways: list[Location], main_way) -> tuple[list[Location], list[float]]:    
        profit_coords = {}
        profits = []
        for (i, way) in enumerate(ways):
            if way != self.location:
                came_from, cost_so_far = a_star_search(field, main_way, way)
                path = reconstruct_path(came_from, main_way, way)
                profit = 2 - len(path)
                profits.append(profit)
                profit_coords[i] = way
            else:
                profit_coords[i] = way
                profit = 0
        
        return (profit_coords, profits)
