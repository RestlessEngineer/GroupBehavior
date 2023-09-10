from Graph import GridLocation
from RobotFileld import RobotField
import pygame
import numpy as np
from PIL import Image
import math
import os
from inspect import getsourcefile

class View:

    LINE_WIDTH: int = 1 #widht of line between squares

    def __init__(self, resolution: tuple[int, int], 
                 background: tuple[int, int, int] = (100, 100, 100), 
                 squre_color: tuple[int, int, int] = (245, 245, 245),
                 FPS: int = 1,
                 save_gif: bool = False):
        
        self._resolution = resolution
        self._background = background
        self._squre_color = squre_color

        self._clock = pygame.time.Clock()
        self._clock.tick(FPS) 
        
        self._gif_flag = save_gif

        self._screen = pygame.display.set_mode(self._resolution)
        self._screen.fill(self._background)

        self._frames = []


    def __del__(self):
        if len(self._frames) > 0:
            current_path = os.path.abspath(getsourcefile(lambda:0))
            current_dir = os.path.dirname(current_path)
            # Take first frame and put other ones 
            self._frames[0].save(
                current_dir + os.path.sep + 'route.gif',
                save_all=True,
                append_images=self._frames[1:],  # exept first frame
                optimize=True,
                duration=1000,
                loop=0
            )

    def _evaluate_dimensions(self, field: RobotField):
        # Evaluate the width and the height of the squares.
        square_width = (self._resolution[0] / field.width) \
            - self.LINE_WIDTH * ((field.width + 1) / field.width)
        square_height = (self._resolution[1] / field.height) \
            - self.LINE_WIDTH * ((field.height + 1) / field.height)
        return (square_width, square_height)


    def _convert_column_to_x(self, column, square_width):
        x = self.LINE_WIDTH * (column + 1) + square_width * column
        return x


    def _convert_row_to_y(self, row, square_height):
        y = self.LINE_WIDTH * (row + 1) + square_height * row
        return y


    def draw_field(self, field: RobotField):
        square_width, square_height = self._evaluate_dimensions(field)
        for row in range(field.width):
            for column in range(field.height):
                x = self._convert_column_to_x(column, square_width)
                y = self._convert_row_to_y(row, square_height)
                geometry = (x, y, square_width, square_height)
                pygame.draw.rect(self._screen, self._squre_color, geometry)


    def draw_robot(self, field: RobotField, location: GridLocation, 
                   direction: GridLocation, color: tuple[int, int, int]):
        square_width, square_height = self._evaluate_dimensions(field)
        (y, x) = location
        x_core = self._convert_column_to_x(x, square_width) + square_width//2
        y_core = self._convert_row_to_y(y, square_height) + square_height//2

        x_top = x_core + square_width//3 - 5
        y_top = y_core

        x_left = x_core - square_width//4 + 3
        y_left = y_core + square_height//4

        x_right = x_core - square_width//4 + 3
        y_right = y_core - square_height//4

        rect = (x_core - square_width//3, y_core - square_height//3,
                 square_width*2//3, square_height*2//3)
        pygame.draw.rect(self._screen, color, rect, 2)

        if direction != (0,0):
            angle = np.sum(np.array(direction)*np.array([math.pi/2, math.pi]))
            top = np.array([x_top, y_top])
            left = np.array([x_left, y_left])
            right = np.array([x_right, y_right])
            if angle != math.pi:
                rot = np.array([[math.cos(angle), -math.sin(angle)], 
                                [math.sin(angle), math.cos(angle)]])
                core = np.array([x_core, y_core])
                top = np.matmul(rot, top - core) + core
                left = np.matmul(rot, left - core) + core
                right = np.matmul(rot, right - core) + core
            pygame.draw.polygon(self._screen, color, 
                                [np.rint(top), np.rint(right), np.rint(left)])
        else:
            pygame.draw.circle(self._screen, color, (x_core, y_core),
                                radius=min(square_width//4, square_height//4))

    

    def draw_goal(self, field: RobotField, goal: GridLocation, 
                  color: tuple[int,int,int]):
        square_width, square_height = self._evaluate_dimensions(field)
        (y, x) = goal
        x_core = self._convert_column_to_x(x, square_width) + square_width//2
        y_core = self._convert_row_to_y(y, square_height) + square_height//2 
        pygame.draw.circle(self._screen, color, (x_core, y_core), 
                           radius=min(square_width//4, square_height//4))


    def update_screen(self):
        pygame.display.flip()  # Update the screen.
        if self._gif_flag is True:
            pil_string_image = pygame.image.tostring(self._screen, "RGBA",False)
            pil_image = Image.frombytes("RGBA", self._resolution, pil_string_image)
            self._frames.append(pil_image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    
