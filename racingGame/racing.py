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
   
class Player(MasterSprite):
  def __init__(self, x, y):
    super().__init__("red_car.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0
    self.moveSize = 10

  def move(self, x, y):
    self.changeX = x*self.moveSize
    self.changeY = y*self.moveSize
  
  def rot(self, angle):
    self.image=pygame.transform.rotate(self.image, angle)
    
  def setXY(self, x, y):
    super().setXY(x,y)
    if self.x < LEFT_SIDE:
      self.setX(LEFT_SIDE)
    elif self.x+self.width > RIGHT_SIDE: 
      self.setX(RIGHT_SIDE-self.width)
    if self.y < 0:
      self.setY(0)
    elif self.y+self.height > self.displaySize[1]:
      self.setY(self.displaySize[1]-self.height)

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)

class Car(MasterSprite):
    def __init__(self, x):
      super().__init__("enemy_car.png")
      self.originalImage = self.image
      self.setXY(x, 0)
      #self.setXY(self.displaySize[0],random.randint(0,self.displaySize[1]-self.height))
      self.changeY= 10
      self.ready = False

    
    def isReady(self):
        return self.ready

    def update(self):
        self.setY(self.y+self.changeY)
        if self.rect.top > 0:
            self.ready = True
        if self.rect.top > self.displaySize[1]:
            return True
        return False

class Flag(MasterSprite):
    def __init__(self):
      super().__init__("health_power_up.png")
      self.originalImage = self.image
      self.setXY(random.randrange(LEFT_SIDE, RIGHT_SIDE), 0)
      self.changeY= 5
      self.ready = False
    
    def isReady(self):
        return self.ready

    def update(self):
        self.setY(self.y+self.changeY)
        if self.rect.bottom < 0:
            self.ready = True
        if self.rect.top > self.displaySize[1]:
            return True
        return False

  
class Health(MasterSprite):
    def __init__(self, x, y):
      super().__init__("health_sprite.png",x,y)
      self.originalImage = self.image
      self.size = 150
    
    def damage(self, amount):
      self.size-=amount
      if self.size < 0:
        self.size = 0

    def recover(self, amount):
      self.size+=amount
      if self.size > 150:
        self.size = 150

    def update(self):
      self.image = pygame.transform.scale(self.originalImage, (150*self.size/100, 17))
  
def main():
  pygame.mixer.pre_init(44100, -16, 2, 2048)
  #start PyGame
  pygame.init()
  playsound = True
  # Set the height and width of the screen
  size = [SCREEN_WIDTH, SCREEN_HEIGHT]
  screen = pygame.display.set_mode(size)

  pygame.display.set_caption("Retro Racer")

  scoreFont = pygame.font.Font(pygame.font.match_font("Times New Roman"), 30)
  gameOverFont = pygame.font.Font(pygame.font.match_font("Times New Roman"), 60)

  pygame.mixer.init()
  pygame.mixer.music.load("music.wav")
  pygame.mixer.music.set_volume(0.1)
  pygame.mixer.music.play(-1)   # keep looping the music
  crashSound = pygame.mixer.Sound("crash_sound.wav")
  crashSound.set_volume(0.2)
  lifeSound = pygame.mixer.Sound("recover_sound.wav")
  lifeSound.set_volume(6.0)
  gameOverSound = pygame.mixer.Sound("game_over.wav")
  gameOverSound.set_volume(6.0)
  # Loop until the user clicks the close button.
  userQuit = False

  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()

  # Cretate the initial sprites
  player = Player(595,600)
  health = Health(20,10)
  
  score = 0
  gameOver = False

  cars = []
  lastCar = Car(random.randrange(LEFT_SIDE, RIGHT_SIDE - player.width))
  cars.append(lastCar)
  car_counter = 15

  flags = []
  lastFlag = Flag()
  flags.append(lastFlag) 

  bg = pygame.image.load("racing_map_new.png")
  """if score < 30:
    health.image = pygame.image.load("health_low_sprite.png")"""

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
        if event.key == pygame.K_SPACE:
          player.move(0,-50)
        if event.key == pygame.K_RCTRL:
          player.moveSize+=5
        if event.key == pygame.K_LSHIFT:
          player.moveSize-=5
        if event.key == pygame.K_RSHIFT:
          player.moveSize-=5
        if event.key == pygame.K_w:
          player.move(0,-1)
          player.moveSize+=5
        if event.key == pygame.K_s:
          player.move(0,1)
        if event.key == pygame.K_a:
          player.move(-1,0)
        elif event.key == pygame.K_d:
          player.move(1,0)
      elif event.type == pygame.KEYUP:
        player.moveSize=5
        if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LSHIFT, pygame.K_RSHIFT]:
          player.move(0,0)

    # Set the screen background
    screen.fill(BLACK)
    screen.blit(bg, (0,0))

    if score < 30:
      health.image = pygame.image.load("health_low_sprite.png")
    
    if not gameOver:
      if lastCar.isReady() and car_counter <= 0:
          car_hit = True
          while car_hit:
            carPos = random.randrange(LEFT_SIDE, RIGHT_SIDE- player.width)
            car_hit = False
            for car in cars:
              if carPos > car.x-player.width and carPos < car.x+player.width and car.y < player.height:
                car_hit = True
                break
          lastCar = Car(carPos)
          cars.append(lastCar)
          car_counter = random.randint(0, 30)
      else:
          car_counter-=1

      if len(flags) < MAX_FLAGS and lastFlag.isReady:
          lastFlag = Flag()
          flags.append(lastFlag)

      # move the sprites
    
      player.update()
      for car in cars:
          removeCar = car.update()
          if removeCar:
              cars.remove(car)
              del car

      for flag in flags:
          removeFlag = flag.update()
          if removeFlag:
              flags.remove(flag)
              del flag

      hits = player.getRect().collidelist(cars)
      if hits >= 0:
          for car in cars:
              if player.getRect().colliderect(car):
                crashSound.play(0)
                cars.remove(car)
                health.damage(30)
                del car
      
      hits = player.getRect().collidelist(flags)
      if hits >= 0:
          for flag in flags:
              if player.getRect().colliderect(flag):
                  lifeSound.play(0)
                  flags.remove(flag)
                  health.recover(20)
                  del flag                

    # blit the sprites
    scoreText = scoreFont.render("Score: "+str(score), True, BLACK)
    screen.blit(scoreText, (SCREEN_WIDTH-150,0))
    health.update()

    if health.size <= 0:
      if playsound:
        gameOverSound.play(0)
        playsound = False
      gameOver = True
      pygame.mixer.music.stop()
      gameOverText = gameOverFont.render("GAME OVER", True, WHITE)
      displayScore = scoreFont.render("Your Score: "+str(score), True, WHITE)
      screen.fill(BLACK)
      screen.blit(gameOverText, ((SCREEN_WIDTH//4)+120, (SCREEN_HEIGHT//2)-60))
      screen.blit(displayScore, ((SCREEN_WIDTH//4)+200, (SCREEN_HEIGHT//2)-1))
    else:
      screen.blit(player.getSurface(), player.getRect())
      screen.blit(health.getSurface(), health.getRect())
      for car in cars:
          screen.blit(car.getSurface(), car.getRect())
      
      for flag in flags:
          screen.blit(flag.getSurface(), flag.getRect())  

      score+=1
    
    # Limit to 60 frames per second
    clock.tick(60)

    # Render the screen as prepared with the blit commands
    pygame.display.flip()

  # Close everything down
  pygame.quit()

if __name__ == "__main__":
  main()