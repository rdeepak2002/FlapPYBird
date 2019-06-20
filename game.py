import random, pygame                                                           # imports

screenWidth  = 288                                                              # screen width variable
screenHeight = 512                                                              # screen height variable

screen = pygame.display.set_mode((screenWidth, screenHeight))                   # set screen size

world = {
  "score"            :   0,
  "pipespace"        : 200,
  "pipes"            :  [],
  "ground"           :  [],
  "minPipeSpawn"     : 100,
  "maxPipeSpawn"     : 350,
  "pipeopening"      : 130,
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
  gameIcon = pygame.image.load("resources/yellowbird-midflap.png")              # game icon

  pygame.display.set_icon(gameIcon)
  pygame.display.set_caption("Flappy Bird")

  world["pipes"] = [{"x": 500, "y" : 300}]
  while len(world["pipes"]) < 8:
    world["pipes"].append({"x" : world["pipes"][-1]["x"]+world["pipespace"], "y" : random.randint(world["minPipeSpawn"], world["maxPipeSpawn"])})

  world["ground"] = [{"x": 0, "y" : 400}]
  while len(world["ground"]) < 8:
    world["ground"].append({"x" : world["ground"][-1]["x"]+288, "y" : 400})

  pygame.init()                                                                 # initialize pygame

def checkEvents():                                                              # method to check if mouse is clicked or game is closed    
  for event in pygame.event.get():
    if event.type == pygame.QUIT:                                               # close game
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP:                                    # mouse pressed
      if (bird["dead"] == False):
        bird["yVelocity"] = bird["jumpSpeed"]

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

  screen.blit(bird["image"], (127.0, bird["y"]))                                # draw bird 

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
  if (bird["dead"] == False): 
    bird["x"] += 2

def pipeMover():
  while(world["pipes"][0]["x"]-bird["x"] < -80):                                  # remove pipe
    world["pipes"].pop(0)

  while(len(world["pipes"]) < 8):
    world["pipes"].append({"x" : world["pipes"][-1]["x"]+world["pipespace"], "y" : random.randint(world["minPipeSpawn"], world["maxPipeSpawn"])})

  while(world["ground"][0]["x"]-bird["x"] < -300):                                # remove ground
    world["ground"].pop(0)

  while(len(world["ground"]) < 8):
    world["ground"].append({"x" : world["pipes"][-1]["x"]+288, "y" : 400})

  for pipe in world["pipes"]:
    if collision(127, bird["y"], bird["width"], bird["height"], pipe["x"]-bird["x"], pipe["y"], 52, 320):
      bird["dead"] = True

def gameLoop():                                                                   # game loop which contains logic of the game
  updateSprites()  
  checkEvents()
  playerMover()
  if (bird["dead"] == False): 
    pipeMover()

def collision(x1, y1, width1, height1, x2, y2, width2, height2):
  rect1 = {"x": x1, "y": y1, "width": width1, "height": height1}
  rect2 = {"x": x2, "y": y2, "width": width2, "height": height2}
  rect3 = {"x": x2, "y": y2-world["pipeopening"]-320, "width": width2, "height": height2}

  if (rect1["x"] <= rect2["x"] + rect2["width"] and rect1["x"] + rect1["width"] >= rect2["x"] and rect1["y"] <= rect2["y"] + rect2["height"] and rect1["y"] + rect1["height"] >= rect2["y"]):
    return True

  if (rect1["x"] <= rect3["x"] + rect3["width"] and rect1["x"] + rect1["width"] >= rect3["x"] and rect1["y"] <= rect3["y"] + rect3["height"] and rect1["y"] + rect1["height"] >= rect3["y"]):
    return True

  return False

def main():
  init()
  while True:
    gameLoop()

if __name__ == "__main__":
    main()