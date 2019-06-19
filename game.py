import random, pygame                                                           # imports

screenWidth  = 288                                                              # screen width variable
screenHeight = 512                                                              # screen height variable

screen = pygame.display.set_mode((screenWidth, screenHeight))                   # set screen size

world = {
  "score"            :   0,
  "pipespace"        : 200,
  "pipes"            :  [],
  "background-image" : pygame.image.load("resources/background-day.png")
}

bird = {                                                                        # bird object
  "x"                  : 127.0,
  "y"                  : 240.0,
  "width"              :  34.0,
  "height"             :  24.0,
  "yVelocity"          :   3.0,
  "yVelocityMin"       :  10.0,
  "yVelocityMax"       : -12.0,
  "yAccel"             :  -1.0,
  "jumpSpeed"          :  10.0,
  "image"              : pygame.image.load("resources/yellowbird-midflap.png")
}

def init():
  gameIcon = pygame.image.load("resources/yellowbird-midflap.png")              # game icon
  pygame.display.set_icon(gameIcon)
  pygame.display.set_caption("Flappy Bird")
  world["pipes"] = [{"x": 500, "y" : 300}]
  while len(world["pipes"]) < 8:
    world["pipes"].append({"x" : world["pipes"][-1]["x"]+world["pipespace"], "y" : random.randint(80, 350)})
  pygame.init()                                                                 # initialize pygame

def checkEvents():                                                              # method to check if mouse is clicked or game is closed    
  for event in pygame.event.get():
    if event.type == pygame.QUIT:                                               # close game
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP:                                    # mouse pressed
      bird["yVelocity"] = bird["jumpSpeed"]

def updateSprites():                                                            # method to update images on screen
  baseImg = pygame.image.load("resources/base.png")
  pipeImg = pygame.image.load("resources/pipe-green.png")
  pipeUpsidedownImg = pygame.transform.flip(pygame.image.load("resources/pipe-green.png"), False, True)

  screen.fill((0, 0, 0))

  screen.blit(world["background-image"], (0, 0))                                # draw background image

  for pipe in world["pipes"]:
    screen.blit(pipeImg, (pipe["x"]-bird["x"], pipe["y"]))
    screen.blit(pipeUpsidedownImg, (pipe["x"]-bird["x"], pipe["y"]-100-320))

  screen.blit(baseImg, (0, 400))
  screen.blit(bird["image"], (127.0, bird["y"]  ))                              # draw bird 

  pygame.display.flip()                                                         # update screen

def playerMover():
  bird["yVelocity"] += bird["yAccel"]

  if(bird["yVelocity"] < bird["yVelocityMax"]):
    bird["yVelocity"] = bird["yVelocityMax"]

  if(bird["yVelocity"] > bird["yVelocityMin"]):
    bird["yVelocity"] = bird["yVelocityMin"]

  bird["y"] -= bird["yVelocity"]

  if(bird["y"] > 376):
    bird["velocity"] = 0
    bird["y"] = 376

  if(bird["y"] < 0):
    bird["velocity"] = 0
    bird["y"] = 0

  bird["x"] += 2

def pipeMover():
  if(world["pipes"][0]["x"]-bird["x"] < -30):                                     # remove pipe
    world["pipes"].pop(0)

  if(len(world["pipes"]) < 8):
    world["pipes"].append({"x" : world["pipes"][-1]["x"]+world["pipespace"], "y" : random.randint(80, 360)})

def gameLoop():                                                                  # game loop which contains logic of the game
  checkEvents()
  playerMover()
  pipeMover()
  updateSprites()

def main():
  init()
  while True:
    gameLoop()

if __name__ == "__main__":
    main()