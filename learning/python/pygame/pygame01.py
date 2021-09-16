#!/usr/bin/env python3
''' A simple pygame program'''
import pygame

pygame.init()

# Set up the drawing window
# In pygame, everything is viewed on a single user-created display, which can
# be a window or a full screen. The display is created using .set_mode(), which
# returns a Surface representing the visible part of the window. It is this Surface
# that you pass into drawing functions like pygame.draw.circle(), and the contents
# of that Surface are pushed to the display when you call pygame.display.flip().
screen = pygame.display.set_mode( [ 500, 500 ] )

running = True
while running:
    # Wait for the window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill( ( 255, 255, 255 ) )

    # Draw a solid blue circle in the center
    pygame.draw.circle( screen, ( 0, 0, 255 ), ( 250, 250 ), 75 )

    # Flip the display
    pygame.display.flip()

pygame.quit()
