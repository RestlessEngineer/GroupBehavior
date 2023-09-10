from RobotFileld import RobotField
from Graph import Location, a_star_search, reconstruct_path 
from Robot import Robot
import numpy as np
import random
from scipy.optimize import linprog

class Strategy:
    # define the best strategy
    def choose_strategy(self, profit_matix) -> int:
        pass
        

class NashStrategy(Strategy): 
    
    def _probability_mixed_strategies(self, profit_matrix: np.array) -> tuple[list[float]]:  # noqa: E501
        min_profit = np.min(profit_matrix)
        #matrix must be positive
        if(min_profit <= 0):
            profit_matrix += -min_profit + 1
            min_profit = 1
        
        row, col = profit_matrix.shape
        A = -profit_matrix.transpose()
        b = -min_profit*np.ones(col)
        f = np.ones(row) # minimisated function 
        strategy_bounds = [(0, None)]*row
        res = linprog(f, A_ub=A, b_ub=b, bounds=strategy_bounds)
        return res.x/np.sum(res.x)



    def _solve_strategy(self, profit_matrix) -> tuple[list[int], list[float]]:
        
        min_j = np.min(profit_matrix, axis=1)
        max_i = np.max(profit_matrix, axis=0)
        
        # max_i min_j (mtx_{ij})
        maxmin = np.max(min_j)

        # max_i min_j (mtx_{ij})
        minmax = np.min(max_i)
        
        strategies = list(range(profit_matrix.shape[0]))

        if maxmin != minmax:
            probabilities = self._probability_mixed_strategies(profit_matrix)
            return (strategies, probabilities)
        
        probability = 1/len(list(filter(lambda x: x == minmax, min_j)))
        probabilities = list(map(lambda x: probability if x == minmax else 0, min_j)) 
        
        return (strategies, probabilities)

    
    # min max trategy from game theory https://en.wikipedia.org/wiki/Nash_equilibrium
    def choose_strategy(self, profit_matrix) -> int:
        strategies, probabilities = self._solve_strategy(profit_matrix)
        return int(random.choices(strategies, weights=probabilities)[0])


class CalculateProfit:
    
    def __call__(self, field: RobotField, robot: Robot, 
                 robots: list[Robot]) -> tuple[list[Location], list[float]]:
        pass


class SimpleProfit(CalculateProfit):

    def __call__(self, field: RobotField, ways: list[Location], 
                 main_way: Location) -> tuple[list[Location], list[float]]:    
    
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
    
    def __call__(self, field: RobotField, ways: list[Location], 
                 main_way: Location) -> tuple[list[Location], list[float]]:
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
