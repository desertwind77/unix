#!/usr/bin/env python3

import pygame
import random
from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT,
                            K_ESCAPE, KEYDOWN, QUIT, )

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
BACKGROUOND = ( 135, 206, 250 )
DESIRED_FPS = 30

# In programming terms, a sprite is a 2D representation of something on the screen.
# Essentially, it’s a picture. pygame provides a Sprite class, which is designed to
# hold one or several graphical representations of any game object that you want to
# display on the screen. To use it, you create a new class that extends Sprite.
# This allows you to use its built-in methods.
class Player( pygame.sprite.Sprite ):
    def __init__( self ):
        super( Player, self ).__init__()
        # Image to display
        #self.surf = pygame.Surface( ( 75, 25 ) )
        #self.surf.fill( WHITE )
        self.surf = pygame.image.load( "images/jet.png" ).convert()
        self.surf.set_colorkey( WHITE, RLEACCEL )
        self.rect = self.surf.get_rect()
        self.move_up_sound = pygame.mixer.Sound( "sounds/Rising_putter.ogg" )
        self.move_down_sound = pygame.mixer.Sound( "sounds/Falling_putter.ogg" )
        self.collision_sound = pygame.mixer.Sound( "sounds/Collision.ogg" )

    def update( self, pressed_keys ):
        if pressed_keys[ K_UP ]:
            # Move in place
            self.rect.move_ip( 0, -5 )
            self.move_up_sound.play()
        if pressed_keys[ K_DOWN ]:
            self.rect.move_ip( 0, 5 )
            self.move_down_sound.play()
        if pressed_keys[ K_LEFT ]:
            self.rect.move_ip( -5, 0 )
        if pressed_keys[ K_RIGHT ]:
            self.rect.move_ip( 5, 0 )

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy( pygame.sprite.Sprite ):
    def __init__( self ):
        super( Enemy, self ).__init__()
        #self.surf = pygame.Surface( ( 20, 10 ) )
        #self.surf.fill( WHITE )
        self.surf = pygame.image.load( "images/missile.png" ).convert()
        self.surf.set_colorkey( WHITE, RLEACCEL )
        self.rect = self.surf.get_rect(
            center=(
                random.randint( SCREEN_WIDTH + 20, SCREEN_WIDTH + 100 ),
                random.randint( 0, SCREEN_HEIGHT ),
            )
        )
        self.speed = random.randint( 5, 20 )

    def update( self ):
        self.rect.move_ip( -self.speed, 0 )
        if self.rect.right < 0:
            self.kill()

class Cloud( pygame.sprite.Sprite ):
    def __init__( self ):
        super( Cloud, self ).__init__()
        self.surf = pygame.image.load( "images/cloud.png" ).convert()
        self.surf.set_colorkey( BLACK, RLEACCEL )
        self.rect = self.surf.get_rect(
                center=(
                    random.randint( SCREEN_WIDTH + 20, SCREEN_WIDTH + 100 ),
                    random.randint( 0, SCREEN_HEIGHT ),
                )
        )

    def update( self ):
        self.rect.move_ip( -5, 0 )
        if self.rect.right < 0:
            self.kill()

pygame.init()
screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
# Trigger the custom event every 250ms
pygame.time.set_timer( ADDENEMY, 250 )
pygame.time.set_timer( ADDCLOUD, 1000 )

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

player = Player()
# Sprite group used for position updates and collision detection
enemies = pygame.sprite.Group()
# Sprite group used for position updates
clouds = pygame.sprite.Group()
# Sprite group used for image rendering
all_sprites = pygame.sprite.Group()
all_sprites.add( player )

pygame.mixer.music.load( "sounds/Apoxode_-_Electric_1.mp3" )
pygame.mixer.music.play( loops=-1 )

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add( new_enemy )
            all_sprites.add( new_enemy )
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add( new_cloud )
            all_sprites.add( new_cloud )

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    player.update( pressed_keys )
    # Update enemy position
    enemies.update()
    clouds.update()

    # Recall that a Surface is a rectangular object on which you can draw, like a blank
    # sheet of paper. The screen object is a Surface, and you can create your own Surface
    # objects separate from the display screen.
    screen.fill( BACKGROUOND )

    # blit (block transfer) surf on to screen at the center
    # Draw all sprites
    for entity in all_sprites:
        screen.blit( entity.surf, entity.rect ) 

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany( player, enemies ):
        # If so, then remove teh player and stop the loop
        player.move_up_sound.stop()
        player.move_down_sound.stop()
        player.collision_sound.play()
        player.kill()
        running = False

    # Display it
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick( DESIRED_FPS )

pygame.mixer.music.stop()
pygame.mixer.quit()
