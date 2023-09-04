import pygame

# variables used in sprite class
COLOR = (255, 100, 98)
WIDTH = 500
HEIGHT = 500
# array with maze info
walls = []

# sprite / player class
class Sprite(pygame.sprite.Sprite):

    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.set_colorkey(COLOR)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()

    # moving functions, names indicate direction (what moves, how much it moves)
    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, speed):
        self.rect.y -= speed * speed / 10

    def moveBack(self, speed):
        self.rect.y += speed * speed / 10

# wall class, creates and recognizes maze walls
class Wall(object):
    def __init__(self, pos):
        # adds to walls[] array
        walls.append(self)
        # draws wall blocks onto the screen
        self.rect = pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 50, 50))

# initialize the pygame
pygame.init()

# create window thingy
screen = pygame.display.set_mode((500, 500))
# setting window title & icon
pygame.display.set_caption("avoid green & get to purple")
pygame.display.set_icon(pygame.image.load('rubik_1362043.png'))
# check if it initialized
print(pygame.display.get_init())

# maze array. 0 represents path, 1 represents walls, 3 is the end
building = [[1, 3, 1, 0, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 0, 1]]

# the variable player will reference the sprite, which is an object created through the Sprite class
player_=Sprite((255, 0, 0), 25, 25)
# coordinates where player will spawn in (415, 450)
player_.rect.x=415
player_.rect.y=450

# any sprite created in the program will be added to this list to be constantly updated
all_sprites_list = pygame.sprite.Group()
# add the player_ variable to that list
all_sprites_list.add(player_)

# draws the maze from the array onto the screen
def renderbuilding(build):

   x = 0
   y = 0
   for row in build:
       for block in row:
           if block == 0:
               # draws path blocks
               pygame.draw.rect(screen, (0, 0, 0), (x, y, 50, 50))
           elif block == 1:
               # creates wall blocks with class Wall()
                Wall((x,y))
           # moves block drawings along the x axis
           x = x + 50
       # moves to next row of blocks
       y = y + 50
       x = 0

# creating end square - when touched the player wins and restarts
end_ = pygame.draw.rect(screen, (0,0,255), (50,0,50,50))

# variable that indicates runtime - starts infinite while loop
running = 1
# the clock will be used later to control the speed of running the loop
clock = pygame.time.Clock()
# game loop, what happens when it is running.
while running == 1:
    # background color (will be covered by maze, served as a test for configurations
    screen.fill((255, 0, 255))
    # adding the maze
    renderbuilding(building)
    # the screen needs to be updated for changes to appear
    pygame.display.update()
    # detects user input (events)
    for event in pygame.event.get():
        # closing if the quit button is pressed
        if event.type == pygame.QUIT:
            print("closed")
            running = 0
        # sprite movement
        key = pygame.key.get_pressed()
        # if left arrow is pressed
        if key[pygame.K_LEFT]:
            player_.moveLeft(10)
            # left boundaries
            if player_.rect.x<= 0:
                player_.rect.x=1
        # if right arrow is pressed
        if key[pygame.K_RIGHT]:
            player_.moveRight(10)
            # right boundaries
            if player_.rect.x>= 480:
                player_.rect.x=479
        # if up arrow is pressed
        if key[pygame.K_UP]:
            player_.moveForward(10)
            # top boundaries
            if player_.rect.y<= 0:
                player_.rect.y=1
        # if down arrow is pressed
        if key[pygame.K_DOWN]:
            player_.moveBack(10)
            # bottom boundaries
            if player_.rect.y>= 480:
                player_.rect.y=479
        # references walls array, the player isn't supposed to touch any block that is in it
        for item in walls:
            # recognizes if player touches/collides with wall
             if pygame.sprite.collide_rect(player_, item):
                print("contaminated! try again")
                player_.rect.y=450
                player_.rect.x=415
        # when the sprite touches the end square
        if player_.rect.colliderect(end_):
            print("you win!")
            player_.rect.y = 450
            player_.rect.x = 415

    # making the changes appear on display
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()

    # stabilizing sprite - controls loop speed
    clock.tick(20)
