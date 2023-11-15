import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")


#define player action variables
moving_left = False
moving_right = False


#colors

RED = (255,0,0)

def draw_bgg():
  pygame.draw.line(screen, RED, (0, 370), (SCREEN_WIDTH, 370))

class Player(pygame.sprite.Sprite):
  def __init__(self, char_type, name_char, x, y,scale,speed):
    pygame.sprite.Sprite.__init__(self)
    self.speed = speed
    self.alive = True
    self.char_type = char_type
    self.name_char = name_char
    self.direction = 1
    self.vel_y = 0
    self.jump = False
    self.in_air = True
    self.flip = False
    self.update_time  = pygame.time.get_ticks()
    self.anition_list = []
    self.frame_index = 0
    self.action = 0

    temp_list = []
    for i in range(2):
      img = pygame.image.load(f'img/{self.char_type}/character_{self.name_char}_idle{i}.png')
      img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
      temp_list.append(img)
    self.anition_list.append(temp_list)

    temp_list = []
    for i in range(3):
      img = pygame.image.load(f'img/{self.char_type}/character_{self.name_char}_run{i}.png')
      img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
      temp_list.append(img)
    self.anition_list.append(temp_list)

    temp_list = []
    for i in range(1):
      img = pygame.image.load(f'img/{self.char_type}/character_{self.name_char}_jump{i}.png')
      img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
      temp_list.append(img)
    self.anition_list.append(temp_list)


    self.image = self.anition_list[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

  def move(self,moving_left,moving_right):
    #reset movement variables
    dx = 0
    dy = 0

    #assign movement variables
    if moving_left:
      dx = -self.speed
      self.flip = True
      self.direction = -1

    if moving_right:
      dx = self.speed
      self.flip = False
      self.direction = 1
    
    #jump
    if self.jump == True and self.in_air == False:
      self.vel_y = -11
      self.jump = False
      self.in_air = True
    
    #apply gravity
    self.vel_y += GRAVITY
    if self.vel_y > 10:
      self.vel_y
    dy += self.vel_y

    #check for collision with floor
    if self.rect.bottom + dy > 370:
      dy = 370 - self.rect.bottom
      self.in_air = False
      #self.jump = False


    #update rectangle position
    self.rect.x += dx
    self.rect.y += dy


  def update_animation(self):

    if self.action == 0 or self.action == 2:#idle animation
      ANIMATION_COOLDOWN = 320
    else:
      ANIMATION_COOLDOWN = 60 
    #update image depending on current frame
    self.image = self.anition_list[self.action][self.frame_index]

    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - self.speed:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1
    #if the animation has run out reset back to the start
    if self.frame_index >= len(self.anition_list[self.action]):
      self.frame_index = 0


  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks() 

  def draw(self):
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Player('character','maleAdventurer',100, 344, .2, 2)
player2 = Player('enemy','zombie',500, 344, .2, 0)

x = 400
y = 343
scale = .2
#define game variables
scroll = 0

ground_image = pygame.image.load("img/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
  bg_image = pygame.image.load(f"img/plx-{i}.png").convert_alpha()
  bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
  for x in range(5):
    speed = 0
    for i in bg_images:
      screen.blit(i, ((x * bg_width) - scroll * speed+2, 0))
      speed += 0.1

def draw_ground():
 
  
  for x in range(15):
    screen.blit(ground_image, ((x * ground_width) - scroll * .2, SCREEN_HEIGHT - ground_height))

#game loop
run = True
while run:
  clock.tick(FPS)
  #draw world
  draw_bg()
  draw_ground()
  draw_bgg()

  player.update_animation()
  player.draw()
  player2.draw()

  #update player actions
  if player.alive:
    if player.in_air:
      player.update_action(2) #2 means jump
    elif moving_left or moving_right:
      player.update_action(1)#1 means walk
    else:
      player.update_action(0)#0 means idle

  player.move(moving_left,moving_right)
  #get keypresses
  key = pygame.key.get_pressed()
  if key[pygame.K_a] and scroll > 0:
    scroll -= 2
  if key[pygame.K_d] and scroll < 1000:
    scroll += 2

  #event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    #Keyboard presses 
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_right = True
      if event.key == pygame.K_w and player.alive and player.in_air == False:
        player.jump = True  
      if event.key == pygame.K_ESCAPE:
        run = False
    #Keyboard button released
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_right = False

  pygame.display.update()


pygame.quit()