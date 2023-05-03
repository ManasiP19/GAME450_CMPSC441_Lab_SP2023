import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_elevation, elevation_to_rgba, get_combat_bg
from pygame_ai_player import PyGameAIPlayer
from response_generator import generate_dialogue

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size):
    elevation = get_elevation(size)
    landscape = elevation_to_rgba(elevation)
    # landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return elevation, pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def display_city_names(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


def get_route_cost(cities, current_city, dest_city, elevation):
    '''
    :param cities: two cities to calculate cost for
    :param elevation: elevations of the landscape
    :return: cost of route based on elevation
    '''
    city_elevations = []
    city_elevations.append(elevation[cities[current_city][0]][cities[current_city][1]])
    city_elevations.append(elevation[cities[dest_city][0]][cities[dest_city][1]])
    return (int)((city_elevations[1] - city_elevations[0]) * 200)

class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 0.5

    screen = setup_window(width, height, "Game World Gen Practice")

    elevation, landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    #player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    route_cost = 0
    shouldContinue = False
    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                for route in routes:
                    if route[0] == cities[state.current_city] and route[1] == cities[int(chr(action))]:
                        shouldContinue = True
                        break
                if shouldContinue == False:
                    print("No route from the current city to the selected city")
                else:
                    start = cities[state.current_city]
                    state.destination_city = int(chr(action))
                    destination = cities[state.destination_city]
                    player_sprite.set_location(cities[state.current_city])
                    state.travelling = True
                    print(
                        "Travelling from", state.current_city, "to", state.destination_city
                    )
                    player.money -= get_route_cost(cities, state.current_city, state.destination_city, elevation)
                    shouldContinue = False

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        display_city_names(cities, city_names)

        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)
                print('Money left', player.money)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            reward = run_pygame_combat(combat_surface, screen, player_sprite)
            player.money += reward * 20
            print('Money earned:', reward*20)
            print('Money left:', player.money)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if player.money < 0:
            print('GAME OVER! You do not have any money left')
            print(generate_dialogue("i lost"))
            break
        if state.current_city == end_city :
            print('You have reached the end of the game!')
            print('You have', player.money, 'left.')
            print('You Won!')
            print(generate_dialogue("i won"))
            break
