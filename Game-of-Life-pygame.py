import sys, pygame
import numpy as np
from scipy.signal import fftconvolve

BLACK = 0,0,0
WHITE = 255,255,255
GREEN = 0,255,0
FONT = 'comicsansms'
g_width,g_height,g_margin = 10,10,1
n_rows, n_columns = 50,50
size = width,height = n_rows*g_height + (n_rows+1)*g_margin, n_rows*g_width + (n_rows+1)*g_margin

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game of Life (Press S to go back to Start Screen)")

clock = pygame.time.Clock()


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def print_message_to_screen(message, font_size, colour, x, y):
    largeText = pygame.font.SysFont(FONT,font_size)
    TextSurf, TextRect = text_objects(message, largeText, colour)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)

def start_screen():
    loop = True
    run_ahead = True
    screen.fill(BLACK)
    pygame.display.update()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                run_ahead = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                loop = False
        print_message_to_screen("Game of Life", 40, GREEN, (width/2), (height/6))
        print_message_to_screen("___________", 40, GREEN, (width/2), (height/6))
        print_message_to_screen("Instructions:", 20, WHITE, width/2, height/4)
        print_message_to_screen("Left Mouse: Draw", 20, WHITE, width/2, height/4+25)
        print_message_to_screen("Right Mouse:Erase", 20, WHITE, width/2, height/4+50)
        print_message_to_screen("Enter:Start simulation", 20, WHITE, width/2, height/4+75)
        print_message_to_screen("R:Reload to blank screen", 20, WHITE, width/2, height/4+100)
        print_message_to_screen("S:Go back to start screen", 20, WHITE, width/2, height/4+125)
        pygame.display.update()
    return run_ahead


# Initializing the grid with input
def initialize():
    screen.fill(BLACK)
    pygame.display.flip()
    grid = np.zeros(n_rows*n_columns).reshape(n_rows,n_columns)
    loop = True
    proceed = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                proceed = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (g_width + g_margin)
                row = pos[1] // (g_height + g_margin)
                # Set that location to one
                if event.button == 1:
                    grid[row][column] = 1
                    color = WHITE
                    pygame.draw.rect(screen,
                                            color,
                                            [(g_margin + g_width) * column + g_margin,
                                            (g_margin + g_height) * row + g_margin,
                                            g_width,
                                            g_height])
                    pygame.display.flip()
                elif event.button == 3:
                    grid[row][column] = 0
                    color=BLACK
                    pygame.draw.rect(screen,
                                            color,
                                            [(g_margin + g_width) * column + g_margin,
                                            (g_margin + g_height) * row + g_margin,
                                            g_width,
                                            g_height])
                    pygame.display.flip()
                # print("Click ", pos, "Grid coordinates: ", row, column)
            elif (event.type == pygame.KEYDOWN):
                if event.unicode=='\r':
                    loop = False
                    break
    return grid, proceed

def run_game(grid):
    # Evolution of the grid
    neighbour_kernel = np.ones(9).reshape(3,3)
    neighbour_kernel[1,1] = 0
    running = True
    reload = False
    back_to_start = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode in ['r', 'R']:
                    running = False
                    reload = True
                elif event.unicode in ['s', 'S']:
                    running = False
                    back_to_start = True


        neighbour_count = np.round(fftconvolve(grid,neighbour_kernel,mode='same'))
        R2 = (grid==1) & ((neighbour_count>1) & (neighbour_count<4))
        R4 = (grid==0) & (neighbour_count==3)
        grid = np.zeros(n_rows*n_columns).reshape(n_rows,n_columns)
        grid[R2|R4] = 1

        for row in range(n_rows):
            for column in range(n_columns):
                color = BLACK
                if grid[row][column] == 1:
                    color = WHITE
                pygame.draw.rect(screen,
                                    color,
                                    [(g_margin + g_width) * column + g_margin,
                                    (g_margin + g_height) * row + g_margin,
                                    g_width,
                                    g_height])
    
        # Limit to 5 frames per second
        clock.tick(5)
        
        pygame.display.flip()
    return reload, back_to_start

s = True
while s:
    s = False
    r = start_screen()
    while r:
        r = False
        g1,p = initialize()
        if p:
            r,s = run_game(g1)
pygame.quit()