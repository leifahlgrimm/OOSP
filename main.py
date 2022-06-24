import pygame, sys, random
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


# the scale of the grid
scale = 40
# window properties
window_width = 1000
window_height = 1000
global cell_number_width
cell_number_width = window_width / scale
global cell_number_height
cell_number_height = window_height / scale
refresh_controller = pygame.time.Clock()
global speed
speed = 5

# colors
global background_color
background_color= (175,215,70)
global grass_color
grass_color = (167, 209, 61)

# snake starting points
snake_position = [window_width / 2 - scale / 2, window_height / 2 - scale / 2]
snake_body = [[window_width / 2 - scale / 2, window_height / 2 - scale / 2],
              [window_width / 2 - scale / 2, window_height / 2 - scale / 2 + scale],
              [window_width / 2 - scale / 2, window_height / 2 - scale / 2 + 2 * scale]
              ]
# food starting point
global food_position
food_position = [random.randrange(1, window_width // scale) * scale,
                 random.randrange(1, window_height // scale) * scale
                 ]
global score
score = 0
global active
active = True

pygame.init()
pygame.display.set_caption("Snake OOSP")
screen = pygame.display.set_mode((window_width, window_height), pygame.SCALED | pygame.FULLSCREEN, vsync=1)

# load food graphic
apple = pygame.image.load('img/apple.png').convert_alpha()

# load snake graphics
global head
global tail
# head graphics
head_up = pygame.image.load('img/head_up.png').convert_alpha()
head_down = pygame.image.load('img/head_down.png').convert_alpha()
head_right = pygame.image.load('img/head_right.png').convert_alpha()
head_left = pygame.image.load('img/head_left.png').convert_alpha()
# tail graphics
tail_up = pygame.image.load('img/tail_up.png').convert_alpha()
tail_down = pygame.image.load('img/tail_down.png').convert_alpha()
tail_right = pygame.image.load('img/tail_right.png').convert_alpha()
tail_left = pygame.image.load('img/tail_left.png').convert_alpha()
# body graphics
body_vertical = pygame.image.load('img/body_vertical.png').convert_alpha()
body_horizontal = pygame.image.load('img/body_horizontal.png').convert_alpha()
body_tr = pygame.image.load('img/body_tr.png').convert_alpha()
body_tl = pygame.image.load('img/body_tl.png').convert_alpha()
body_br = pygame.image.load('img/body_br.png').convert_alpha()
body_bl = pygame.image.load('img/body_bl.png').convert_alpha()

# load sounds
crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
background_music = pygame.mixer.Sound('sound/background.mp3')
background_music.play(-1, 0, 3000)
background_music.set_volume(.3)


def paint_checked_pattern():
    global grass_color
    for row in range (int(cell_number_height)):
        if row % 2 == 0:
            for col in range(int(cell_number_width)):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * scale, row * scale, scale, scale)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(int(cell_number_width)):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * scale, row * scale, scale, scale)
                    pygame.draw.rect(screen, grass_color, grass_rect)


def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        screen.fill(pygame.Color(background_color))
        paint_checked_pattern()
        font = pygame.font.SysFont('Arial', scale)
        render = font.render(f"Paused, to continue press Space, to quit press Q", True, pygame.Color(0, 0, 0))
        rect = render.get_rect()
        rect.midtop = (window_width / 2, window_height / 2)
        screen.blit(render, rect)
        pygame.display.update()
        refresh_controller.tick(speed)


def handle_keys(movement_direction):
    global speed
    new_movement_direction = movement_direction
    for event in pygame.event.get():
        # if key/button is pressed
        if event.type == pygame.KEYDOWN:
            # movement keys
            if event.key == pygame.K_UP and movement_direction != Direction.DOWN:
                new_movement_direction = Direction.UP
            if event.key == pygame.K_DOWN and movement_direction != Direction.UP:
                new_movement_direction = Direction.DOWN
            if event.key == pygame.K_RIGHT and movement_direction != Direction.LEFT:
                new_movement_direction = Direction.RIGHT
            if event.key == pygame.K_LEFT and movement_direction != Direction.RIGHT:
                new_movement_direction = Direction.LEFT
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                pause_game()
        # exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return new_movement_direction


# movement is done by always adding the snake position to the very front of it
# and keeping it there in case food was eaten or removing it if no food was eaten in eat_food()
def move_snake(direction):
    if active:
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
    food_position = [random.randrange(1, window_width // scale) * scale,
                     random.randrange(1, window_height // scale) * scale
                     ]


def eat_food():
    global score, active
    if active:
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 10
            crunch_sound.play()
            generate_new_food()
        else:
            # If no food was eaten, remove end of snake
            snake_body.pop()


def update_head_graphics():
    global head
    head_x_direction = (snake_body[1][0] - snake_body[0][0]) / scale
    head_y_direction = (snake_body[1][1] - snake_body[0][1]) / scale

    if head_x_direction == 1.0:
        head = head_left
    elif head_x_direction == -1.0:
        head = head_right
    elif head_y_direction == 1.0:
        head = head_up
    elif head_y_direction == -1.0:
        head = head_down


def update_tail_graphics():
    global tail
    tail_x_direction = (snake_body[-2][0] - snake_body[-1][0]) / scale
    tail_y_direction = (snake_body[-2][1] - snake_body[-1][1]) / scale

    if tail_x_direction == 1.0:
        tail = tail_left
    elif tail_x_direction == -1.0:
        tail = tail_right
    elif tail_y_direction == 1.0:
        tail = tail_up
    elif tail_y_direction == -1.0:
        tail = tail_down


def repaint():
    # paint background
    screen.fill(pygame.Color(background_color))
    paint_checked_pattern()

    # paint snake head and body
    for index, body in enumerate(snake_body):
        body_rect = pygame.Rect(body[0], body[1], scale, scale)

        # draw head
        if index == 0:
            update_head_graphics()
            screen.blit(head, body_rect)

        # draw tail
        elif index == len(snake_body) - 1:
            update_tail_graphics()
            screen.blit(tail, body_rect)

        # draw body
        else:
            previous_body = snake_body[index + 1]
            next_body = snake_body[index - 1]

            # draw vertical body parts
            if previous_body[0] == next_body[0]:
                screen.blit(body_vertical, body_rect)
            # draw horizontal body parts
            elif previous_body[1] == next_body[1]:
                screen.blit(body_horizontal, body_rect)
            # draw corners
            else:
                # get previous body positions relative to current body
                previous_body_x = (previous_body[0] - body[0]) / scale
                previous_body_y = (previous_body[1] - body[1]) / scale
                # get next body positions relative to current body
                next_body_x = (next_body[0] - body[0]) / scale
                next_body_y = (next_body[1] - body[1]) / scale

                # draw bottom right corner
                if previous_body_x == -1.0 and next_body_y == -1.0 or previous_body_y == -1.0 and next_body_x == -1.0:
                    screen.blit(body_tl, body_rect)
                # draw top right corner
                elif previous_body_y == 1.0 and next_body_x == -1.0 or previous_body_x == -1.0 and next_body_y == 1.0:
                    screen.blit(body_bl, body_rect)
                # draw top left corner
                elif previous_body_x == 1.0 and next_body_y == 1.0 or previous_body_y == 1.0 and next_body_x == 1.0:
                    screen.blit(body_br, body_rect)
                # draw bottom left corner
                elif previous_body_y == -1.0 and next_body_x == 1.0 or previous_body_x == 1.0 and next_body_y == -1.0:
                    screen.blit(body_tr, body_rect)
    # paint food
    fruit_rect = pygame.Rect(food_position[0], food_position[1], scale, scale)
    screen.blit(apple, fruit_rect)


def game_over_message():
    font = pygame.font.SysFont('Arial', scale * 5)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2)
    screen.blit(render, rect)
    pygame.display.flip()


def game_over():
    # out of window
    if snake_position[0] < 0 or snake_position[0] > window_width:
        game_over_message()
    if snake_position[1] < 0 or snake_position[1] > window_height:
        game_over_message()
    for blob in snake_body[1:]:
        if snake_position[0] == blob[0] and snake_position[1] == blob[1]:
            game_over_message()


def paint_hud():
    font = pygame.font.SysFont("Arial", scale)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    screen.blit(render, rect)
    pygame.display.flip()


def game_loop():
    movement_direction = Direction.UP
    while True:
        movement_direction = handle_keys(movement_direction)
        move_snake(movement_direction)
        eat_food()
        repaint()
        paint_hud()
        game_over()
        pygame.display.update()
        refresh_controller.tick(speed)


def main_menu_loop():
    menu = True
    while menu:
        mouse_position = pygame.mouse.get_pos()

        screen.fill(pygame.Color(background_color))
        paint_checked_pattern()

        play_text =

        pygame.display.update()
        refresh_controller.tick(speed)


if __name__ == "__main__":
    main_menu_loop()
    # game_loop()
