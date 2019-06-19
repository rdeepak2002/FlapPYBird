import sys, pygame                                                      # imports
pygame.init()                                                           # initialize pygame

screenWidth  = 288                                                      # screen width variable
screenHeight = 512                                                      # screen height variable

screen = pygame.display.set_mode((screenWidth, screenHeight))           # set screen size
bg_image = pygame.image.load("background-day.png")                      # background image

world = {
    "score" : 0,
    "time_elapsed_since_last_action" : 0
}

bird = {                                                                # bird object
  "x"            :  127.0,
  "y"            :  240.0,
  "width"        :   34.0,
  "height"       :   24.0,
  "yVelocity"    :    3.0,
  "yVelocityMin" :    8.0,
  "yVelocityMax" :   -9.0,
  "yAccel"       :   -1.0,
  "jumpSpeed"    :    8.0,
  "image"        : pygame.image.load("yellowbird-midflap.png")
}

def checkEvents():                                                      # method to check if mouse is clicked or game is closed    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:                                     # close game
          sys.exit()
      elif event.type == pygame.MOUSEBUTTONUP:                          # mouse pressed
          bird["yVelocity"] = bird["jumpSpeed"]

def updateSprites():                                                    # method to update images on screen
    screen.blit(bg_image, (0, 0))                                       # draw background image
    birdPos = bird["x"], bird["y"]                                      # get position of bird
    screen.blit(bird["image"], birdPos)                                 # draw bird 
    pygame.display.flip()                                               # update screen

def mover():
    bird["yVelocity"] += bird["yAccel"]

    if(bird["yVelocity"] < bird["yVelocityMax"]):
        bird["yVelocity"] = bird["yVelocityMax"]

    if(bird["yVelocity"] > bird["yVelocityMin"]):
        bird["yVelocity"] = bird["yVelocityMin"]

    bird["y"] -= bird["yVelocity"]          

    if(bird["y"] > 488):
        bird["y"] = 488


def gameLoop():                                                         # game loop which contains logic of the game
    checkEvents()
    mover()
    updateSprites()

while True:                                                             # infinite loop
    gameLoop()