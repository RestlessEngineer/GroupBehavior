from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
parent_parent_dir = parent_dir[:parent_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_parent_dir)

from Robot import *
from RobotFileld import *
from Simulation import *
from View import *
import time


if __name__ == '__main__':

    field = RobotField(10, 10)
    robots = []

    robots.append(Robot(field, (8,1),  (1,7)))
    robots.append(Robot(field, (6,1),  (4,8)))
    robots.append(Robot(field, (7,3),  (1,2)))
    robots.append(Robot(field, (6,5),  (4,1)))
    robots.append(Robot(field, (8,5),  (2,5)))
    robots.append(Robot(field, (8,8),  (3,1)))
    robots.append(Robot(field, (5,3),  (2,8)))
    robots.append(Robot(field, (3,2),  (9,7)))
    robots.append(Robot(field, (3,7),  (8,3)))
    robots.append(Robot(field, (3,4),  (9,5)))
    robots.append(Robot(field, (1,4),  (5,1)))
    robots.append(Robot(field, (1,1),  (4,6)))
    robots.append(Robot(field, (1,6),  (7,6)))
    robots.append(Robot(field, (5,7),  (7,4)))
    robots.append(Robot(field, (1,8),  (7,1)))

    colors = [(255,69,0), (0,139,139), (255,165,0), (0,100,0), (128,0,0),
              (0,255,255), (128,128,0), (255,0,255), (0,204,0), (128,128,128),
              (255,140,0), (240,230,140), (255,99,71), (178,34,34), (47,79,79)]
    
    view = View((800, 800), (100, 100, 100), (245, 245, 245), save_gif=True)

    simulation = Simulation(field, robots, colors, view, True)
    
    # for start step
    simulation.show()
    time.sleep(1)

    while not simulation.is_all_robots_on_goals():
        simulation.do_step()
        simulation.show()
        time.sleep(1)