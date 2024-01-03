import pygame
from pygame.locals import Rect
import random

pygame.init()

#create dimensions for an empty game window 
screen_width = 600
screen_height = 600

#create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

#define some game vaiables
cell_size = 10
direction = 1 # 1 is up, 2 is right, 3 is down, 4 is left
update_snake = 0
food = [0, 0]
new_food = True
new_piece = [0,0]
score = 0
game_over = False
clicked = False

#create the snake
snake_pos = [[int(screen_width/2), int(screen_height/2)]]
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size])
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 2])
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 3])

#define text font
font = pygame.font.SysFont(None, 40)

#define colors
bg = (192, 192, 192)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
red = (255, 0, 0)
food_col = (200, 50, 50)
blue = (0, 0, 255)

#set up rect for 'Play Again'
again_rect = Rect(screen_width//2 - 80, screen_height//2, 160, 50)

def draw_screen():
    screen.fill(bg)

def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0,0))

def check_game_over(game_over):

    #first check if snake has eaten itself
    head_count = 0
    for segment in snake_pos:
        if snake_pos[0] == segment and head_count > 0:
            game_over = True
        head_count += 1

    #check if snake is out of bounds
    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
        game_over = True

    return game_over

def draw_game_over():
    over_txt = 'Game Over!'
    over_img = font.render(over_txt, True, blue)
    pygame.draw.rect(screen, red, (screen_width//2 -80, screen_height//2 - 60, 160, 50))
    screen.blit(over_img, (screen_width//2 -80, screen_height//2 - 50 ))

    again_txt = 'Play Again?'
    again_img = font.render(again_txt, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width//2 - 80, screen_height//2 + 10))

#create game loop
run = True
while run:

    draw_screen()
    draw_score()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    #create the food
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width // cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)

    #draw the food
    pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))

    #check if food has been eaten
    if snake_pos[0] == food:
        new_food = True
        #create new piece at snake tail
        new_piece = list(snake_pos[-1])
        if direction == 1:
            new_piece[1] += cell_size
        if direction == 3:
            new_piece[1] -= cell_size
        if direction == 2:
            new_piece[0] -= cell_size
        if direction == 4:
            new_piece[0] += cell_size
        
        #attach new piece
        snake_pos.append(new_piece)

        #keep score
        score += 1
    #game over check
    if game_over == False:
        #timer
        if update_snake > 30: #This is the speed of the snake
            update_snake = 0
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            #heading up
            if direction == 1:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
            if direction == 3:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
            if direction == 2:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
            if direction == 4:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size

            game_over = check_game_over(game_over)

    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                #reset variables
                direction = 1 # 1 is up, 2 is right, 3 is down, 4 is left
                update_snake = 0
                food = [0, 0]
                new_food = True
                new_piece = [0,0]
                score = 0
                game_over = False

                #create the snake
                snake_pos = [[int(screen_width/2), int(screen_height/2)]]
                snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size])
                snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 2])
                snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 3])


    #draw snake
    head = 1
    for x in snake_pos:
        if head == 0:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, red, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    #update the display
    pygame.display.update()

    update_snake += 1

#end pygame
pygame.quit