import pygame                                                                   # imports

screenWidth  = 288                                                              # screen width variable
screenHeight = 512                                                              # screen height variable

screen = pygame.display.set_mode((screenWidth, screenHeight))                   # set screen size

world = {
  "score"            : 0,
  "background-image" : pygame.image.load("resources/background-day.png")
}

bird = {                                                                        # bird object
  "x"                  : 127.0,
  "y"                  : 240.0,
  "width"              :  34.0,
  "height"             :  24.0,
  "yVelocity"          :   3.0,
  "yVelocityMin"       :  10.0,
  "yVelocityMax"       :  -12.0,
  "yAccel"             :  -1.0,
  "jumpSpeed"          :  10.0,
  "image"              : pygame.image.load("resources/yellowbird-midflap.png")
}

def init():
  gameIcon = pygame.image.load("resources/yellowbird-midflap.png")              # game icon
  pygame.display.set_icon(gameIcon)
  pygame.display.set_caption("Flappy Bird")

  pygame.init()                                                                 # initialize pygame

def checkEvents():                                                              # method to check if mouse is clicked or game is closed    
  for event in pygame.event.get():
    if event.type == pygame.QUIT:                                               # close game
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP:                                    # mouse pressed
      bird["yVelocity"] = bird["jumpSpeed"]

def updateSprites():                                                            # method to update images on screen
  screen.blit(world["background-image"], (0, 0))                                # draw background image
  screen.blit(bird["image"], (bird["x"], bird["y"]  ))                          # draw bird 
  pygame.display.flip()                                                         # update screen

def mover():
  bird["yVelocity"] += bird["yAccel"]

  if(bird["yVelocity"] < bird["yVelocityMax"]):
    bird["yVelocity"] = bird["yVelocityMax"]

  if(bird["yVelocity"] > bird["yVelocityMin"]):
    bird["yVelocity"] = bird["yVelocityMin"]

  bird["y"] -= bird["yVelocity"]          

  if(bird["y"] > 488):
    bird["velocity"] = 0
    bird["y"] = 488
  if(bird["y"] < 0):
    bird["velocity"] = 0
    bird["y"] = 0

def gameLoop():                                                                  # game loop which contains logic of the game
  checkEvents()
  mover()
  updateSprites()

def main():
  init()
  while True:
    gameLoop()

if __name__ == "__main__":
    main()