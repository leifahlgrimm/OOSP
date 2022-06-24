import pickle
import sys
import random
import pygame
import config
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


# window properties
cell_number_x = config.window_width / config.tile_size
cell_number_y = config.window_height / config.tile_size
refresh_controller = pygame.time.Clock()

# snake starting points
snake_position = None
snake_body = None
movement_direction = None
# food starting point
food_position = None
highscore = 0
score = 0

pygame.init()
pygame.display.set_caption(config.caption)
app_icon = pygame.image.load('img/head_up.png')
pygame.display.set_icon(app_icon)
screen = pygame.display.set_mode((config.window_width, config.window_height), pygame.SCALED, vsync=1)
game_state = None

# load food graphic
apple = pygame.image.load('img/apple.png').convert_alpha()

# load snake graphics
head = None
tail = None
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

# load sound effects and background music
crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
background_music = pygame.mixer.Sound('sound/background.mp3')
background_music.play(-1, 0, 3000)
background_music_running = True
background_music.set_volume(config.music_volume)


def exit_application():
    if score > highscore:
        with open('highscore.dat', 'wb') as highscore_file:
            pickle.dump(score, highscore_file)
    pygame.quit()
    sys.exit()


def generate_new_food():
    global food_position
    food_position = [random.randrange(1, config.window_width // config.tile_size) * config.tile_size,
                     random.randrange(1, config.window_height // config.tile_size) * config.tile_size
                     ]


def init_game():
    global snake_position
    global snake_body
    global score
    global movement_direction
    global highscore
    snake_position = [config.window_width / 2 - config.tile_size / 2, config.window_height / 2 - config.tile_size / 2]
    snake_body = [[config.window_width / 2 - config.tile_size / 2, config.window_height / 2 - config.tile_size / 2],
                  [config.window_width / 2 - config.tile_size / 2,
                   config.window_height / 2 - config.tile_size / 2 + config.tile_size],
                  [config.window_width / 2 - config.tile_size / 2,
                   config.window_height / 2 - config.tile_size / 2 + 2 * config.tile_size]
                  ]
    generate_new_food()
    score = 0
    movement_direction = Direction.UP
    try:
        with open('highscore.dat', 'rb') as highscore_file:
            highscore = pickle.load(highscore_file)
    except:
        highscore = 0


def paint_checked_pattern():
    for row in range(int(cell_number_y)):
        if row % 2 == 0:
            for col in range(int(cell_number_x)):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * config.tile_size, row * config.tile_size, config.tile_size,
                                             config.tile_size)
                    pygame.draw.rect(screen, config.grass_color, grass_rect)
        else:
            for col in range(int(cell_number_x)):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * config.tile_size, row * config.tile_size, config.tile_size,
                                             config.tile_size)
                    pygame.draw.rect(screen, config.grass_color, grass_rect)


def pause_game():
    global game_state
    game_state = "paused"
    while game_state == "paused":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_application()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "game"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    main_menu_loop()
                elif event.key == pygame.K_m:
                    toggle_background_music()

        # paint pause screen overlay
        font = pygame.font.Font(config.font, config.font_size_big)
        render = font.render(f"Paused", True, pygame.Color(config.font_color), pygame.Color(config.background_color))
        rect = render.get_rect()
        rect.center = (config.window_width / 2, config.window_height / 2)
        screen.blit(render, rect)

        font_small = pygame.font.Font(config.font, config.font_size_small)
        render_continue = font_small.render("To continue press Space", True, pygame.Color(config.font_color), pygame.Color(config.background_color))
        rect_continue = render_continue.get_rect()
        rect_continue.midtop = rect.midbottom
        screen.blit(render_continue, rect_continue)

        render_quit = font_small.render("To quit to main menu press Q or ESC", True, pygame.Color(config.font_color), pygame.Color(config.background_color))
        rect_quit = render_quit.get_rect()
        rect_quit.midtop = rect_continue.midbottom
        screen.blit(render_quit, rect_quit)

        pygame.display.update()
        refresh_controller.tick(config.speed)


def toggle_background_music():
    global background_music_running
    if background_music_running:
        background_music.stop()
        background_music_running = False
    else:
        background_music.play(-1, 0, 3000)
        background_music.set_volume(.3)
        background_music_running = True


def handle_keys():
    new_movement_direction = movement_direction
    for event in pygame.event.get():
        # if key/button is pressed
        if event.type == pygame.KEYDOWN:
            # during game stage
            if game_state == "game":
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and movement_direction != Direction.DOWN:
                    new_movement_direction = Direction.UP
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and movement_direction != Direction.UP:
                    new_movement_direction = Direction.DOWN
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and movement_direction != Direction.LEFT:
                    new_movement_direction = Direction.RIGHT
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and movement_direction != Direction.RIGHT:
                    new_movement_direction = Direction.LEFT
                if event.key == pygame.K_SPACE:
                    pause_game()
            # during main menu
            if game_state == "menu":
                if event.key == pygame.K_SPACE:
                    game_loop()
            # everywhere
            if event.key == pygame.K_m:
                toggle_background_music()
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                exit_application()
        # exit button
        if event.type == pygame.QUIT:
            exit_application()
    return new_movement_direction


# movement is done by always adding the snake position to the very front of it
# and keeping it there in case food was eaten or removing it if no food was eaten in eat_food()
def move_snake(direction):
    if True:
        if direction == Direction.LEFT:
            snake_position[0] -= config.tile_size
        if direction == Direction.RIGHT:
            snake_position[0] += config.tile_size
        if direction == Direction.UP:
            snake_position[1] -= config.tile_size
        if direction == Direction.DOWN:
            snake_position[1] += config.tile_size
        snake_body.insert(0, list(snake_position))


def eat_food():
    global score
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10
        crunch_sound.play()
        generate_new_food()
    else:
        # If no food was eaten, remove end of snake
        snake_body.pop()


def update_head_graphics():
    global head
    head_x_direction = (snake_body[1][0] - snake_body[0][0]) / config.tile_size
    head_y_direction = (snake_body[1][1] - snake_body[0][1]) / config.tile_size

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
    tail_x_direction = (snake_body[-2][0] - snake_body[-1][0]) / config.tile_size
    tail_y_direction = (snake_body[-2][1] - snake_body[-1][1]) / config.tile_size

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
    screen.fill(pygame.Color(config.background_color))
    paint_checked_pattern()

    # paint snake head and body
    for index, body in enumerate(snake_body):
        body_rect = pygame.Rect(body[0], body[1], config.tile_size, config.tile_size)

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
                previous_body_x = (previous_body[0] - body[0]) / config.tile_size
                previous_body_y = (previous_body[1] - body[1]) / config.tile_size
                # get next body positions relative to current body
                next_body_x = (next_body[0] - body[0]) / config.tile_size
                next_body_y = (next_body[1] - body[1]) / config.tile_size

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
    fruit_rect = pygame.Rect(food_position[0], food_position[1], config.tile_size, config.tile_size)
    screen.blit(apple, fruit_rect)


def game_over_screen():
    global game_state
    game_state = "game_over"
    if score > highscore:
        with open('highscore.dat', 'wb') as file:
            pickle.dump(score, file)
    while game_state == "game_over":
        # paint game over screen
        screen.fill(pygame.Color(config.background_color))
        paint_checked_pattern()

        font_score = pygame.font.Font(config.font, config.font_size_big)
        render_score = font_score.render(f"Score: {score}", True, pygame.Color(config.font_color),
                                         pygame.Color(config.background_color))
        rect_score = render_score.get_rect()
        rect_score.center = (config.window_width / 2, config.window_height / 2)
        screen.blit(render_score, rect_score)

        font_keys = pygame.font.Font(config.font, config.font_size_small)
        render_continue = font_keys.render("To play again press SPACE", True, pygame.Color(config.font_color),
                                           pygame.Color(config.background_color))
        rect_continue = render_continue.get_rect()
        rect_continue.midtop = rect_score.midbottom
        screen.blit(render_continue, rect_continue)

        render_quit = font_keys.render("To quit to main menu press Q or ESC", True, pygame.Color(config.font_color),
                                       pygame.Color(config.background_color))
        rect_quit = render_quit.get_rect()
        rect_quit.midtop = rect_continue.midbottom
        screen.blit(render_quit, rect_quit)

        pygame.display.update()

        # key handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    main_menu_loop()
                if event.key == pygame.K_SPACE:
                    init_game()
                    game_state = "game"
                if event.key == pygame.K_m:
                    toggle_background_music()

        pygame.display.update()
        refresh_controller.tick(config.speed)


def game_over():
    # if snake head out of window
    if snake_position[0] < 0 or snake_position[0] > config.window_width or snake_position[1] < 0 or snake_position[1] > config.window_height:
        game_over_screen()
    # if snake hits own body
    for blob in snake_body[1:]:
        if snake_position[0] == blob[0] and snake_position[1] == blob[1]:
            game_over_screen()


def paint_hud():
    font = pygame.font.Font(config.font, config.font_size_small)

    # paint score section left aligned
    render = font.render(f"Score: {score}", True, pygame.Color(config.font_color))
    rect = render.get_rect()
    screen.blit(render, rect)

    # paint highscore section right aligned
    render_highscore = font.render(f"Highscore: {highscore}", True, pygame.Color(config.font_color))
    rect_highscore = render_highscore.get_rect()
    rect_highscore.right = config.window_width
    screen.blit(render_highscore, rect_highscore)

    pygame.display.update()


def game_loop():
    global movement_direction
    global game_state
    game_state = "game"
    while game_state == "game":
        movement_direction = handle_keys()
        move_snake(movement_direction)
        eat_food()
        repaint()
        paint_hud()
        game_over()
        pygame.display.update()
        refresh_controller.tick(config.speed)


def main_menu_loop():
    init_game()
    global game_state
    game_state = "menu"
    while game_state == "menu":
        screen.fill(pygame.Color(config.background_color))
        paint_checked_pattern()

        font = pygame.font.Font(config.font, config.font_size)
        render_play = font.render("Press space to Play", True, pygame.Color(config.font_color),
                                  pygame.Color(config.background_color))
        rect_play = render_play.get_rect()
        rect_play.center = (config.window_width / 2, config.window_height / 2)
        screen.blit(render_play, rect_play)

        render_quit = font.render("Press Q or ESC to quit", True, pygame.Color(config.font_color),
                                  pygame.Color(config.background_color))
        rect_quit = render_quit.get_rect()
        rect_quit.midtop = rect_play.midbottom
        screen.blit(render_quit, rect_quit)

        render_mute = font.render("Press M to mute/unmute music", True, pygame.Color(config.font_color),
                                  pygame.Color(config.background_color))
        rect_mute = render_mute.get_rect()
        rect_mute.midtop = rect_quit.midbottom
        screen.blit(render_mute, rect_mute)

        handle_keys()
        pygame.display.update()
        refresh_controller.tick(config.speed)


if __name__ == "__main__":
    main_menu_loop()
