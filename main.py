import time

import pygame
from enum import Enum
import random


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


scale = 20
window_width = 1920
window_height = 1080
refresh_controller = pygame.time.Clock()
snake_position = [500, 500]
snake_body = [[500, 500],
              [500, 500 + scale],
              [500, 500 + 2*scale]
              ]
global food_position
food_position = [240, 240]
global score
score = 0
speed = 10

pygame.init()
pygame.display.set_caption("Snake OOSP")
window = pygame.display.set_mode((window_width, window_height))

def handle_keys(movement_direction):
    new_movement_direction = movement_direction
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_UP and movement_direction != Direction.DOWN:
            new_movement_direction = Direction.UP
        if event.key == pygame.K_DOWN and movement_direction != Direction.UP:
            new_movement_direction = Direction.DOWN
        if event.key == pygame.K_RIGHT and movement_direction != Direction.LEFT:
            new_movement_direction = Direction.RIGHT
        if event.key == pygame.K_LEFT and movement_direction != Direction.RIGHT:
            new_movement_direction = Direction.LEFT
    return new_movement_direction


def move_snake(direction):
    if direction == Direction.LEFT:
        snake_position[0] -= scale
    if direction == Direction.RIGHT:
        snake_position[0] += scale
    if direction == Direction.UP:
        snake_position[1] -= scale
    if direction == Direction.DOWN:
        snake_position[1] += scale
    snake_body.insert(0, list(snake_position))


def generate_new_food():
    global food_position
    food_position = [random.randrange(30, window_width // scale) * scale,
                     random.randrange(30, window_height // scale) * scale
                     ]


def get_food():
    global score
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10
        generate_new_food()
    else:
        # If no food was eaten, remove end of snake
        snake_body.pop()


def repaint():
    window.fill(pygame.Color(0, 0, 0))
    for body in snake_body:
        pygame.draw.rect(window, pygame.Color(0, 0, 255), pygame.Rect(body[0] - scale/2, body[1] - scale/2, scale, scale))
    pygame.draw.circle(window, pygame.Color(255, 0, 0), (food_position[0], food_position[1]), scale / 2)
        #pygame.draw.circle(window, pygame.Color(0, 0, 255), (body[0], body[1]), scale / 2)
    #pygame.draw.rect(window, pygame.Color(255, 0, 0), pygame.Rect(food_position[0] - scale/2, food_position[1] - scale/2, scale, scale))


def game_over_message():
    #TODO
    font = pygame.font.SysFont('Arial', scale * 5)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2)
    window.blit(render, rect)
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()
    exit(0)


def game_over():
    if snake_position[0] < 0 or snake_position[0] > window_width - 10:
        game_over_message()
    if snake_position[1] < 0 or snake_position[1] > window_height - 10:
        game_over_message()
    for blob in snake_body[1:]:
        if snake_position[0] == blob[0] and snake_position[1] == blob[1]:
            game_over_message()

def paint_hud():
    font = pygame.font.SysFont("Arial", scale)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    window.blit(render, rect)
    pygame.display.flip()


def game_loop():
    movement_direction = Direction.UP
    while True:
        movement_direction = handle_keys(movement_direction)
        move_snake(movement_direction)
        get_food()
        repaint()
        game_over()
        paint_hud()
        pygame.display.update()
        refresh_controller.tick(speed)

def main_menu():
    while True:
        mouse_position = pygame.mouse.get_pos()
        window.fill("black")

        window.blit()



def options():
    pass

if __name__ == "__main__":
    game_loop()
