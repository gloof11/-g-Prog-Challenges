# Import and initialize pygame
import pygame
pygame.init()

# Create the window (640x480)
screen = pygame.display.set_mode([640, 480])

# The Main Loop
while (1):
    # Check the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.circle(screen, (0, 0, 255), pygame.mouse.get_pos(), 15)

    pygame.display.update()

'''
TODO:
    Draw lines to each circle
    Implement Eulerianpath algo
'''