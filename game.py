import random, pygame                                                           # imports

screenWidth  = 288                                                              # screen width variable
screenHeight = 512                                                              # screen height variable

screen = pygame.display.set_mode((screenWidth, screenHeight))                   # set screen size

world = {
  "score"            :     0,
  "pipespace"        :   200,
  "pipes"            :    [],
  "ground"           :    [],
  "minPipeSpawn"     :   140,
  "maxPipeSpawn"     :   350,
  "pipeopening"      :   150,
  "gameover"         : False,
  "startgame"        : False,
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
  "dead"               : False,
  "image"              : pygame.image.load("resources/yellowbird-midflap.png")
}

def init():
  gameIcon = pygame.image.load("resources/icon.png")              # game icon

  pygame.display.set_icon(gameIcon)
  pygame.display.set_caption("Flappy Bird")
  
  createGround()

  pygame.init()                                                                 # initialize pygame

def checkEvents():                                                              # method to check if mouse is clicked or game is closed    
  for event in pygame.event.get():
    if event.type == pygame.QUIT:                                               # close game
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP:                                    # mouse pressed
      if(world["startgame"] == False):
        world["startgame"] = True
        createPipes()
      if (bird["dead"] == False):
        bird["yVelocity"] = bird["jumpSpeed"]
      elif (bird["dead"] == True and world["gameover"] == True):
        world["startgame"] = False
        reset()

def updateSprites():                                                            # method to update images on screen
  baseImg = pygame.image.load("resources/base.png")
  pipeImg = pygame.image.load("resources/pipe-green.png")
  pipeUpsidedownImg = pygame.transform.flip(pygame.image.load("resources/pipe-green.png"), False, True)

  screen.fill((0, 0, 0))

  screen.blit(world["background-image"], (0, 0))                                # draw background image

  for pipe in world["pipes"]:
    screen.blit(pipeImg, (pipe["x"]-bird["x"], pipe["y"]))
    screen.blit(pipeUpsidedownImg, (pipe["x"]-bird["x"], pipe["y"]-world["pipeopening"]-320))

  for ground in world["ground"]:
    screen.blit(baseImg, (ground["x"]-bird["x"], ground["y"]))

  if(world["startgame"]== True):
    drawScore()
  else:
    screen.blit(pygame.image.load("resources/message.png"), (52, 70))

  screen.blit(bird["image"], (127.0, bird["y"]))                                # draw bird 

  if(world["gameover"]==True):
    screen.blit(pygame.image.load("resources/gameover.png"), (48, 200))

  pygame.display.flip()                                                         # update screen

def drawScore():
  numbers = [pygame.image.load("resources/0.png"), pygame.image.load("resources/1.png"), pygame.image.load("resources/2.png"), pygame.image.load("resources/3.png"), pygame.image.load("resources/4.png"), 
             pygame.image.load("resources/5.png"), pygame.image.load("resources/6.png"), pygame.image.load("resources/7.png"), pygame.image.load("resources/8.png"), pygame.image.load("resources/9.png")]
  
  number_string = str(world["score"])

  length = len(number_string)

  if(length == 1):
    screen.blit(numbers[world["score"]], (131.5, 10))
  elif(length == 2):
    screen.blit(numbers[int(number_string[0])], (131.5, 10))
    screen.blit(numbers[int(number_string[1])], (156.5, 10))
  elif(length == 3):
    screen.blit(numbers[int(number_string[0])], (119, 10))
    screen.blit(numbers[int(number_string[1])], (131.5, 10))
    screen.blit(numbers[int(number_string[2])], (156.5, 10))

def playerMover():
  if(world["startgame"]== True):
    bird["yVelocity"] += bird["yAccel"]

    if(bird["yVelocity"] < bird["yVelocityMax"]):
      bird["yVelocity"] = bird["yVelocityMax"]

    if(bird["yVelocity"] > bird["yVelocityMin"]):
      bird["yVelocity"] = bird["yVelocityMin"]

    bird["y"] -= bird["yVelocity"]

  if(bird["y"] > 376):
    bird["velocity"] = 0
    bird["y"] = 376
    bird["dead"] = True
    world["gameover"] = True

  if(bird["y"] < 0):
    bird["velocity"] = 0
    bird["y"] = 0

  if (bird["dead"] == False): 
    bird["x"] += 2

def pipeMover():
  if(len(world["pipes"]) != 0):
    while(world["pipes"][0]["x"]-bird["x"] < -80 and (world["startgame"]== True)):                                  # remove pipe
      world["pipes"].pop(0)
      createPipes()

  while(world["ground"][0]["x"]-bird["x"] < -300):                                # remove ground
    if(len(world["ground"]) != 0):
      world["ground"].pop(0)
    createGround()

  for pipe in world["pipes"]:
    if collision(127, bird["y"], bird["width"], bird["height"], pipe["x"]-bird["x"], pipe["y"], 52, 320, pipe):
      bird["dead"] = True

def gameLoop():                                                                   # game loop which contains logic of the game
  updateSprites()  
  checkEvents()
  playerMover()
  if (bird["dead"] == False): 
    pipeMover()

def collision(x1, y1, width1, height1, x2, y2, width2, height2, pipe):
  rect1 = {"x": x1, "y": y1, "width": width1, "height": height1}
  rect2 = {"x": x2, "y": y2, "width": width2, "height": height2}
  rect3 = {"x": x2, "y": y2-world["pipeopening"]-320, "width": width2, "height": height2}

  if(world["score"] > 999):
    world["score"] = 999

  if (rect1["x"] <= rect2["x"] + rect2["width"] and rect1["x"] + rect1["width"] >= rect2["x"] and rect1["y"] <= rect2["y"] + rect2["height"] and rect1["y"] + rect1["height"] >= rect2["y"]):
    return True
  elif (rect1["x"] <= rect3["x"] + rect3["width"] and rect1["x"] + rect1["width"] >= rect3["x"] and rect1["y"] <= rect3["y"] + rect3["height"] and rect1["y"] + rect1["height"] >= rect3["y"]):
    return True
  elif(rect1["y"] > rect3["y"]+rect3["height"] and rect1["y"] < rect2["y"] and rect1["x"] > rect2["x"] and rect1["x"] < rect2["x"] + rect2["width"]):
    if(pipe["passed"] == False):
      world["score"] += 1
      pipe["passed"] = True
  return False

def createPipes():
  if(len(world["pipes"]) == 0):
    world["pipes"] = [{"x": bird["x"]+400, "y" : 300, "passed" : False}]

  while len(world["pipes"]) < 8:
    world["pipes"].append({"x" : world["pipes"][-1]["x"]+world["pipespace"], "y" : random.randint(world["minPipeSpawn"], world["maxPipeSpawn"]), "passed" : False})

def createGround():
  if(len(world["ground"]) == 0):
      world["ground"] = [{"x": 0, "y" : 400}]

  while len(world["ground"]) < 8:
      world["ground"].append({"x" : world["ground"][-1]["x"]+288, "y" : 400})

def reset():
  bird["x"] = 127
  bird["y"] = 240
  world["pipes"] = []
  world["ground"] = []
  world["gameover"] = False
  world["score"] = 0
  bird["dead"] = False
  bird["yVelocity"] = 3
  createPipes()
  createGround()

def main():
  init()
  clock = pygame.time.Clock()
  while True:
    gameLoop()
    clock.tick(1000)

if __name__ == "__main__":
    main()