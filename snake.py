import pygame

pygame.init()

#create dimensions for an empty game window 
screen_width = 600
screen_height = 600

#create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

bg = (255, 200, 150)

def draw_screen():
    screen.fill(bg)

#create game loop
run = True

while run:

    draw_screen()
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update the display
    pygame.display.update()

#end pygame
pygame.quit