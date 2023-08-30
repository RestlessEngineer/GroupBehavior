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
import pygame
from PIL import Image
import math
import time


def evaluate_dimensions():
    # Evaluate the width and the height of the squares.
    square_width = (resolution[0] / map_size[0]) - line_width * ((map_size[0] + 1) / map_size[0])
    square_height = (resolution[1] / map_size[1]) - line_width * ((map_size[1] + 1) / map_size[1])
    return (square_width, square_height)


def convert_column_to_x(column, square_width):
    x = line_width * (column + 1) + square_width * column
    return x


def convert_row_to_y(row, square_height):
    y = line_width * (row + 1) + square_height * row
    return y


def draw_squares(color: tuple[int, int, int]):
    square_width, square_height = evaluate_dimensions()
    for row in range(map_size[0]):
        for column in range(map_size[1]):
            x = convert_column_to_x(column, square_width)
            y = convert_row_to_y(row, square_height)
            geometry = (x, y, square_width, square_height)
            pygame.draw.rect(screen, color, geometry)


def draw_robot(location: GridLocation, direction: GridLocation, color: GridLocation):
    square_width, square_height = evaluate_dimensions()
    (y, x) = location
    x_core = convert_column_to_x(x, square_width) + square_width//2
    y_core = convert_row_to_y(y, square_height) + square_height//2
    
    x_top = x_core + square_width//3 - 5
    y_top = y_core
    
    x_left = x_core - square_width//4 + 3
    y_left = y_core + square_height//4 

    x_right = x_core - square_width//4 + 3
    y_right = y_core - square_height//4

    rect = (x_core - square_width//3, y_core - square_height//3, square_width*2//3, square_height*2//3)
    pygame.draw.rect(screen, color, rect, 2)

    if direction != (0,0):
        angle = np.sum(np.array(direction)*np.array([math.pi/2, math.pi]))
        top = np.array([x_top, y_top])
        left = np.array([x_left, y_left])
        right = np.array([x_right, y_right])
        if angle != math.pi:
            rot = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
            core = np.array([x_core, y_core])
            top = np.matmul(rot, top - core) + core
            left = np.matmul(rot, left - core) + core
            right = np.matmul(rot, right - core) + core
        pygame.draw.polygon(screen, color, [np.rint(top), np.rint(right), np.rint(left)])
    else:
        pygame.draw.circle(screen, color, (x_core, y_core), radius=min(square_width//4, square_height//4))
         
    

def draw_goal(goal: GridLocation, color: tuple[int,int,int]):
    square_width, square_height = evaluate_dimensions()
    (y, x) = goal
    x_core = convert_column_to_x(x, square_width) + square_width//2
    y_core = convert_row_to_y(y, square_height) + square_height//2 
    pygame.draw.circle(screen, color, (x_core, y_core), radius=min(square_width//4, square_height//4))


def draw_robots(robots: list[Robot], colors: list[tuple[int,int,int]]):
    for (i, robot) in enumerate(robots):
        draw_robot(robot.location, robot.get_direction(), colors[i])
        draw_goal(robot.goal, colors[i])


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


    simulation = Simulation(field, robots)
    colors = [(255,69,0), (0,139,139), (255,165,0), (0,100,0), (128,0,0),
              (0,255,255), (128,128,0), (255,0,255), (0,204,0), (128,128,128),
              (255,140,0), (240,230,140), (255,99,71), (178,34,34), (47,79,79)]

    resolution = (800, 800)
    map_size = (field.height, field.width)
    screen = pygame.display.set_mode(resolution)
    line_width = 1
    clock = pygame.time.Clock()  # to set max FPS

    clock.tick(1)  # max FPS = 60
    screen.fill((100, 100, 100))  # Fill screen with black color.
    robots = simulation._robots
    draw_squares((240, 240, 240))
    draw_robots(robots, colors)

    pil_string_image = pygame.image.tostring(screen, "RGBA",False)
    pil_image = Image.frombytes("RGBA",resolution,pil_string_image)
    frames = [pil_image]
    pygame.display.flip()  # Update the screen.

    while not simulation.is_all_robots_on_goals():

        simulation.do_step()
        robots = simulation._robots
        draw_squares((240, 240, 240))
        draw_robots(robots, colors)
        pygame.display.flip()  # Update the screen.
        pil_string_image = pygame.image.tostring(screen, "RGBA",False)
        pil_image = Image.frombytes("RGBA",resolution,pil_string_image)
        frames.append(pil_image)
        time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    # Берем первый кадр и в него добавляем оставшееся кадры.
    frames[0].save(
        current_dir + os.path.sep + 'route.gif',
        save_all=True,
        append_images=frames[1:],  # Срез который игнорирует первый кадр.
        optimize=True,
        duration=1000,
        loop=0
    )