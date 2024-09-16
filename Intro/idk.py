import math
from pickletools import read_unicodestring1
from re import T
from winreg import DeleteKeyEx
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
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200
LEFT_SIDE = 248
RIGHT_SIDE = 955 

MAX_CARS = 3
MAX_FLAGS = 2

class MasterSprite(pygame.sprite.Sprite):
  def __init__(self, imageFile, x=0, y=0):
    self.x = x
    self.y = y
    self.image = pygame.image.load(imageFile)
    self.image1=self.image
    self.rect=self.image.get_bounding_rect()
    self.rect.x=x
    self.rect.y=y
    #self.displaySize=pygame.display.get_surface().get_size()
    self.displaySize = (SCREEN_WIDTH-(LEFT_SIDE+RIGHT_SIDE), SCREEN_HEIGHT)
    
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
   
class Button(MasterSprite):
  def __init__(self,imageFile,x,y):
    super().__init__(imageFile,x,y)

  def clicked(self,mousePos):
    if mousePos[0] >= self.rect.left and mousePos[0] <= self.rect.right:
      if mousePos[1] >= self.rect.top and mousePos[1] <= self.rect.bottom:
        return True
    return False

class InstructionsButton(Button):
  def __init__(self,x,y):
    super().__init__("instructionsButton.png",x,y)

class PlayButton(Button):
  def __init__(self,x,y):
    super().__init__("playButton.png",x,y)

class QuitButton(Button):
  def __init__(self,x,y):
    super().__init__("quitButton.png",x,y)

def playGame(screen, largeFont):
  clicked = False
  while not clicked:
    screen.fill(WHITE)

    # render the text
    gameText = largeFont.render("Game Played, click to end",True,BLACK)
    screen.blit(gameText,(100,200))

    # Render the screen as prepared with the blit commands
    pygame.display.flip()

    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONDOWN:
      clicked = True

def showInstructions(screen, largeFont):
  clicked = False
  while not clicked:
    screen.fill(WHITE)

    # render the text
    instructionsText = largeFont.render("The instructions, click for menu",True,BLACK)
    screen.blit(instructionsText,(100,200))
    pygame.display.flip()

    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONDOWN:
      clicked = True

def main():
  #start PyGame
  pygame.init()

  # Set the height and width of the screen
  size = [SCREEN_WIDTH, SCREEN_HEIGHT]
  screen = pygame.display.set_mode(size)

  pygame.display.set_caption("Example Menu")

  # set up the fonts
  largeFont = pygame.font.Font(pygame.font.match_font("thonburi"),60)

  # initialise the menu buttons
  instructionsButton = InstructionsButton(200,200)
  playButton = PlayButton(200,50)
  quitButton = QuitButton(200,350)

  # Loop until the user clicks the close button.
  userQuit = False

  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()

  # -------- Main Program Loop -----------
  while not userQuit:

    # --- Event Processing
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        userQuit = True
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = event.pos
        if playButton.clicked(mousePos):
          playGame(screen, largeFont)
        elif instructionsButton.clicked(mousePos):
          showInstructions(screen, largeFont)
        elif quitButton.clicked(mousePos):
          userQuit = True

    # Set the screen background
    screen.fill(WHITE)

    # display the buttons
    screen.blit(instructionsButton.getSurface(),instructionsButton.getRect())
    screen.blit(playButton.getSurface(),playButton.getRect())
    screen.blit(quitButton.getSurface(),quitButton.getRect())

    # Limit to 60 frames per second
    clock.tick(60)

    # Render the screen as prepared with the blit commands
    pygame.display.flip()

  # Close everything down
  pygame.quit()

if __name__ == "__main__":
  main()