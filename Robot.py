from RobotFileld import *
from Graph import * 
from Strategy import *
import numpy as np
from enum import Enum
import random


class MoveStrategy(Enum):
    PASSIVE = 0
    ACTIVE = 1

class Robot:
    
    OBSERVE_RADIUS: float = 4.0

    def __init__(self, field: RobotField, location: GridLocation, goal: GridLocation, 
                 strategy = NashStrategy(), calc_profit = SimpleProfit()):
        self._field = field
        self.location = location
        self.goal = goal
        self.move_strategy = MoveStrategy.PASSIVE
        self.main_way = location
        self.strategy = strategy
        self.calculate_profit = calc_profit 
        self._update_main_way()


    def get_ways(self):
        #robot can stay in place
        neighbors = [self.location]
        if self.location != self.goal:
            neighbors += list(self._field.neighbors(self.location))
        return neighbors 


    def get_direction(self):
        x = self.main_way[0] - self.location[0]
        y = self.main_way[1] - self.location[1]
        return (x, y)


    def _update_main_way(self):
        # define main way
        came_from, cost_so_far = a_star_search(self._field, self.location, self.goal)
        path = reconstruct_path(came_from, self.location, self.goal)
        # next value after path is main
        if len(path) > 1:
            self.main_way = path[1]
        else:
            self.main_way = self.location


    def create_profit_mtx(self, main_profits, adjacent_profits):
        profit_mtx = []
        if(len(adjacent_profits) == 0):
            for main in main_profits:
                profit_mtx.append([main])
            return profit_mtx
        
        for main_profit in main_profits:
            line = []
            for adj_profit in adjacent_profits:
                final_profit = main_profit - adj_profit
                line.append(final_profit)
            profit_mtx.append(line)
        return profit_mtx


    def get_strategy_profits(self, ways: list[GridLocation]):
        return self.calculate_profit(self._field, ways,self.main_way)


    def get_crossed_strategy_profits(self, robots):
        if(self.location == self.goal):
            return ({0, self.location}, [2])

        ways = list(self._field.neighbors(self.location))
        # robot can stay in place
        ways.append(self.location)
        robots_locations = list(map(lambda x: x.location, robots))
        ways = list(filter(lambda x: x not in robots_locations, ways))

        # filter all neighbor strategies for passive robots 
        if(self.move_strategy == MoveStrategy.PASSIVE):
            for robot in robots:
               # robot always able to stand in location
               neighbors = list(filter(lambda x: x != self.location, robot.get_ways()))
               ways = list(filter(lambda x: x not in neighbors, ways)) 
    
        return self.get_strategy_profits(ways)
            

    def distance(self, robot):
        def loc_distance(loc1: GridLocation, loc2: GridLocation) -> float:
            return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)
        return loc_distance(self.location, robot.location)


    def do_next_step(self, robots) -> GridLocation:
        if(self.location == self.goal):
            return self.location
        
        (profit_coords, profits) =  self.get_crossed_strategy_profits(robots)

        robots_profits = []
        # consider only closest robot locations
        for robot in robots:
            dist = self.distance(robot)
            if(dist <= self.OBSERVE_RADIUS):
                self._field.push_robot_location(robot.location)
                (_, robot_profits) = robot.get_strategy_profits(robot.get_ways())
                robots_profits += robot_profits
        
        # create profit matrix
        profit_matrix = self.create_profit_mtx(profits, robots_profits)
        if len(profit_matrix) == 0:
            return self.location
        
        profit_matrix = np.array(profit_matrix, dtype=int)
        
        # get strategy index from profit matrix
        strategy_num = self.strategy.choose_strategy(profit_matrix)
        
        #update robot location
        self.location = profit_coords[strategy_num]
        self._update_main_way()
        self._field.clear_robots_locations()

        # return strategy coords
        return self.location  
    
    
    