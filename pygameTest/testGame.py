import math
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.changeX = random.randint(-self.speed,self.speed)
        self.changeY = random.randint(-self.speed,self.speed)
        while self.changeX == 0:
          self.changeX = random.randint(-self.speed,self.speed)
        while self.changeY == 0:
          self.changeY = random.randint(-self.speed,self.speed)

        self.image = pygame.image.load("asteroid4.png")
        self.rect=self.image.get_bounding_rect()
        self.rect.x=x
        self.rect.y=y

        self.displaySize=pygame.display.get_surface().get_size()

    def move(self):
        self.x += self.changeX
        self.y += self.changeY

        if self.x+self.changeX < 1 or self.rect.right+self.changeX > self.displaySize[0]-self.speed:
          self.changeX *= -1
        if self.y+self.changeY < 1 or self.rect.bottom+self.changeY > self.displaySize[1]-self.speed:
          self.changeY *= -1

        self.rect.x = self.x
        self.rect.y = self.y

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self.image

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        self.displaySize=pygame.display.get_surface().get_size()
        self.image = pygame.image.load("asteroidShip.png")
        self.rect=self.image.get_bounding_rect()
        self.originalImage = self.image

        self.x = (self.displaySize[0]//2)-self.image.get_width()//2
        self.y = (self.displaySize[1]//2)-self.image.get_height()//2
        self.rect.x=self.x
        self.rect.y=self.y

    def rotate(self):
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]
        objectX = self.rect.centerx
        objectY = self.rect.centery
        degrees = math.degrees(math.atan2(objectY-mouseY, objectX-mouseX))-90
        self.image = pygame.transform.rotate(self.originalImage, -degrees)
        self.rect = self.image.get_bounding_rect()
        self.rect.x = (self.displaySize[0]//2)-self.image.get_width()//2
        self.rect.y = (self.displaySize[1]//2)-self.image.get_height()//2

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self.image

def main():

    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("SFO test game")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    asteroid = Asteroid(200,200)
    player = Ship()

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # move the sprites
        asteroid.move()
        player.rotate()

        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)

        screen.blit(player.get_surface(), player.get_rect())
        screen.blit(asteroid.get_surface(), asteroid.get_rect())

        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Close everything down
    pygame.quit()

if __name__ == "__main__":
    main()
