import random

# Import and initialize pygame
import pygame
pygame.init()

# Create the window (640x480)
screen = pygame.display.set_mode([640, 480])

# Create the circle class
class Circle:
    def __init__(self, position):
        # Initialize the values
        # Color will be random for each circle
        # Position will be based off of mouse press
        self.color = ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.position = position
    
    def drawCircle(self):
        # Draw the circle to the screen
        pygame.draw.circle(screen, self.color, self.position, 15)

# Number of circles
onScreenCircles = []

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
            # Create an instance of the currentCircle and append it to the onScreenSircles list to keep track of all circles
            currentCircle = Circle(pygame.mouse.get_pos())
            currentCircle.drawCircle()
            onScreenCircles.append(currentCircle.position)

            # Detect if more than one circle is on screen, if so draw a line to it, and the last one created
            if (len(onScreenCircles) > 1):
                pygame.draw.line(screen, (255, 255, 255), currentCircle.position,
                                onScreenCircles[len(onScreenCircles)-2], width=2)

    pygame.display.update()

'''
TODO:
    Implement Eulerianpath algo
'''