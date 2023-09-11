from Robot import Robot, MoveStrategy
from RobotFileld import RobotField
from View import View
from Graph import Location
import random
import itertools

class Simulation:


    def __init__(self, field: RobotField, 
                 robots: list[Robot], 
                 colors: list[tuple[int, int, ]], 
                 view: View,
                 infinity: bool = False):
        
        self._field = field
        self._robots = robots
        # TODO: put colors in another place
        self._colors = colors
        self._view = view
        self._infinity = infinity


    def do_step(self):
        robots = self._robots.copy()
        
        adjacencyList = self._make_adjastment()
        strategies = setting_active(adjacencyList, self._robots)
        for (robot, strategy) in strategies.items():
            if strategy == 1:
                robot.move_strategy = MoveStrategy.ACTIVE

        for robot in self._robots:
            except_one = list(filter(lambda x: x != robot, robots))
            robot.do_next_step(except_one)
        
        self._update_strategy()
        

    def _update_strategy(self):
        for robot in self._robots:
            if robot.location == robot.goal:
                robot.move_strategy = MoveStrategy.ONGOAL

        for robot in filter(lambda x: x.move_strategy is not MoveStrategy.ONGOAL,
                             self._robots):
            robot.move_strategy = MoveStrategy.PASSIVE



    def show(self):
        self._view.draw_field(self._field)
        #draw all robots
        for (i, robot) in enumerate(self._robots):
            self._view.draw_robot(self._field, robot.location, 
                                  robot.get_direction(), self._colors[i])
            self._view.draw_goal(self._field, robot.goal, self._colors[i])
        
        self._view.update_screen()


    def is_all_robots_on_goals(self):
        if self._infinity:
            for robot in filter(lambda x: x.goal == x.location, self._robots):
                robot.goal = self._update_goal(robot)
            return False
        
        for robot in self._robots:
            if robot.location != robot.goal:
                return False
        return True


    def _update_goal(self, robot: Robot) -> Location:
        goals = [robot.goal for robot in self._robots]
        x_range = range(self._field.width)
        y_range = range(self._field.height)
        coords = list(itertools.product(x_range, y_range))
        free_coords = list(filter(lambda x: x not in goals, coords))
        new_goal = random.sample(free_coords,1)[0]
        return new_goal


    def _make_adjastment(self):
        adjacencyList = {}
        for vertex in self._robots:
            adjacencyList[vertex] = []
        
        robots = self._robots.copy()
        for robot in self._robots:
            except_one = list(filter(lambda x: x != robot, robots))
            for other_robot in except_one:
                if robot.distance(other_robot) < 2 and \
                    robot.move_strategy is not MoveStrategy.ONGOAL:
                    
                    adjacencyList[robot].append(other_robot)
        return adjacencyList


def setting_active(adjacency: dict[int, list[int]], vertices: set[int]):
    queue = []
    states = {}
    for val in vertices:
        states[val] = -1

    #every isolate nodes is passive
    for (key, adj) in adjacency.items():
        if len(adj) == 0:
            states[key] = 0   

    min = 10000
    for (_, adj) in adjacency.items():
        if len(adj) < min and len(adj) > 0:
            min = len(adj)
    
    for (key, adj) in adjacency.items():
        if min == len(adj):
            queue.append(key)
    
    while len(queue) > 0:
        node = queue.pop(0)
        if states[node] == -1:
            states[node] = 1
            for adj in adjacency[node]:
                states[adj] = 0
                queue.append(adj)
        elif states[node] == 0:
            for adj in adjacency[node]:
                if states[adj] == -1:
                    queue.append(adj)

    return states





