import math
import numpy
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set the size of the screen
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

class MasterSprite(pygame.sprite.Sprite):
  def __init__(self, imageFile, x=0, y=0):
    self.x = x
    self.y = y
    self.image = pygame.image.load(imageFile)
    self.rect=self.image.get_bounding_rect()
    self.rect.x=x
    self.rect.y=y
    self.displaySize=pygame.display.get_surface().get_size()
    self.width = self.rect.right - self.x
    self.height = self.rect.bottom - self.y

  def getRect(self):
    return self.rect

  def getSurface(self):
    return self.image

  def move(self):
    pass

  def setX(self, x):
    self.x = x
    self.rect.x = x

  def setXY(self,x,y):
    self.setX(x)
    self.setY(y)

  def setY(self, y):
    self.y = y
    self.rect.y = y

class Player(MasterSprite):
  def __init__(self,x,y):
    super().__init__("boy.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0

  def move(self, x, y):
    moveSize = 10
    self.changeX = x*moveSize
    self.changeY = y*moveSize

  def setXY(self, x, y):
    super().setXY(x,y)
    if self.x < 0:
      self.setX(0)
    elif self.x+self.width > self.displaySize[0]:
      self.setX(self.displaySize[0]-self.width)
    if self.y < 0:
      self.setY(0)
    elif self.y+self.height > self.displaySize[1]:
      self.setY(self.displaySize[1]-self.height)

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)

def main():
  #start PyGame
  pygame.init()

  # Set the height and width of the screen
  size = [SCREEN_WIDTH, SCREEN_HEIGHT]
  screen = pygame.display.set_mode(size)

  pygame.display.set_caption("Platform Chase")

  # Loop until the user clicks the close button.
  userQuit = False

  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()

  # Create the initial sprites
  player = Player(100,100)

  # Create a main group for all the sprites to be rendered
  #renderSprites = pygame.sprite.Group()
  #player.add(renderSprites)

  # -------- Main Program Loop -----------
  while not userQuit:

    # --- Event Processing
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        userQuit = True
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          player.move(0,-1)
        elif event.key == pygame.K_s:
          player.move(0,1)
        elif event.key == pygame.K_a:
          player.move(-1,0)
        elif event.key == pygame.K_d:
          player.move(1,0)
      elif event.type == pygame.KEYUP:
        if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
          player.move(0,0)

    # Set the screen background
    screen.fill(WHITE)

    # move the sprites
    player.update()

    # blit the sprites
    screen.blit(player.getSurface(), player.getRect())

    # Limit to 60 frames per second
    clock.tick(60)

    # Render the screen as prepared with the blit commands
    pygame.display.flip()

  # Close everything down
  pygame.quit()

if __name__ == "__main__":
  main()
