'''
Lab 5: PCG and Project Lab

This a combined procedural content generation and project lab. 
You will be creating the static components of the game that will be used in the project.
Use the landscape.py file to generate a landscape for the game using perlin noise.
Use the lab 2 cities_n_routes.py file to generate cities and routes for the game.
Draw the landscape, cities and routes on the screen using pygame.draw functions.
Look for triple quotes for instructions on what to do where.
The intention of this lab is to get you familiar with the pygame.draw functions, 
use perlin noise to generate a landscape and more importantly,
build a mindset of writing modular code.
This is the first time you will be creating code that you may use later in the project.
So, please try to write good modular code that you can reuse later.
You can always write non-modular code for the first time and then refactor it later.
'''

import sys
import pygame
import random
import numpy as np
from landscape import get_landscape
from pathlib import Path
sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


# TODO: Demo blittable surface helper function

''' Create helper functions here '''

def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface

def draw_cities(pygame_surface, city_locations):
    for i in range(len(city_locations)):
        pygame.draw.circle(surface=pygame_surface, color=red, center=city_locations[i], radius=5)

def draw_routes(pygame_surface, routes, city_locations_dict):
    for i in range(len(routes)):
        pygame.draw.line(surface=pygame_surface, start_pos=city_locations_dict[routes[i][0]], end_pos=city_locations_dict[routes[i][1]], color=white)

if __name__ == "__main__":
    pygame.init()
    size = width, height = 640, 480
    black = 1, 1, 1
    white = 255, 255, 255
    red = 255, 0, 0

    screen = pygame.display.set_mode(size)
    pygame_surface = get_landscape_surface

    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta',
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    city_locations = [] 
    routes = []

    ''' Setup cities and routes in here'''
    city_locations = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(city_names)

    city_locations_dict = {name: location for name, location in zip(city_names, city_locations)}
    random.shuffle(routes)
    routes = routes[:10] 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)
        screen.blit(pygame_surface, (0, 0))

        ''' draw cities '''
        draw_cities(pygame_surface, city_locations)

        ''' draw first 10 routes '''
        draw_routes(pygame_surface, routes, city_locations_dict)

        pygame.display.flip()
