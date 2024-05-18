import pygame, sys, random
from pygame.math import Vector2 as vec2

class SNAKE:

    def __init__(self):
        self.body = [vec2(5, 10), vec2(4,10), vec2(3,10)]
        self.direction = vec2(1,0)
        self.new_block = False
        

    def draw_snake(self):
        col = 125
        for index,block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size )

            if index == 0:
                if self.body[index] - self.body[1] == vec2(1,0):
                    pygame.draw.circle(screen,(0,0,0),(block_rect.midleft), cell_size / 2, 25,True,False,False,True) # right facing
                elif self.body[index] - self.body[1] == vec2(-1,0):
                    pygame.draw.circle(screen,(0,0,0),(block_rect.midright), cell_size / 2, 25,False,True,True,False) # left facing
                elif self.body[index] - self.body[1] == vec2(0,-1):
                    pygame.draw.circle(screen,(0,0,0),(block_rect.midbottom), cell_size / 2, 25,True,True,False,False) # up facing
                elif self.body[index] - self.body[1] == vec2(0,1):
                    pygame.draw.circle(screen,(0,0,0),(block_rect.midtop), cell_size / 2, 25,False,False,True,True) # down facing
            
            elif index == len(self.body) - 1:
                if self.body[-2] - self.body[index] == vec2(1,0):
                    pygame.draw.polygon(screen,(0,0,0), [block_rect.topright,block_rect.midleft,block_rect.bottomright]) # going right
                if self.body[-2] - self.body[index] == vec2(-1,0):
                    pygame.draw.polygon(screen,(0,0,0), [block_rect.topleft,block_rect.midright,block_rect.bottomleft]) # going left
                if self.body[-2] - self.body[index] == vec2(0,-1):
                    pygame.draw.polygon(screen,(0,0,0), [block_rect.topleft,block_rect.midbottom,block_rect.topright]) # going up
                if self.body[-2] - self.body[index] == vec2(0,1):
                    pygame.draw.polygon(screen,(0,0,0), [block_rect.bottomleft,block_rect.midtop,block_rect.bottomright]) # going down
            else:
                pygame.draw.rect(screen, (col, col, col), block_rect)
            

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [vec2(5, 10), vec2(4,10), vec2(3,10)]

class FRUIT:

    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size - 5, self.pos.y * cell_size - 5, cell_size, cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = vec2(self.x , self.y)

class MAIN:

    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake() 
        self.draw_score()

    def keyboard_press(self):
        if event.key == pygame.K_UP:
            if self.snake.direction.y != 1:
                self.snake.direction = vec2(0,-1)
        if event.key == pygame.K_DOWN:
            if self.snake.direction.y != -1:
                self.snake.direction = vec2(0,1)
        if event.key == pygame.K_RIGHT:
            if self.snake.direction.x != -1:
                self.snake.direction = vec2(1,0)
        if event.key == pygame.K_LEFT:
            if self.snake.direction.x != 1:
                self.snake.direction = vec2(-1,0)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            # print("🐍 ate 🍎")
            self.snake.add_block()

        for block in self.snake.body[:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # hitting walls
        if (not 0 <= self.snake.body[0].x  < cell_number) or (not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        # pygame.quit()
        # sys.exit() 
        self.snake.reset()

    def draw_grass(self):
        grass_color = (162, 208, 47)
        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(row * cell_size , col * cell_size, cell_size, cell_size)
                if (row+col) % 2 == 0:
                    pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        score_surface = font.render(score,True,(0,0,0))
        score_rect = score_surface.get_rect(center = (cell_number * cell_size - 60 ,cell_number * cell_size - 40 ))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

pygame.init()

cell_size = 30
cell_number = 20

screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
pygame.display.set_caption('Classic Snake Game')
apple = pygame.image.load('apple.png').convert_alpha()
pygame.display.set_icon(apple)

font = pygame.font.Font(None,30)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

clock = pygame.time.Clock()
main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            main_game.keyboard_press()

    screen.fill((175,215,70)) 

    main_game.draw_elements()

    pygame.display.update()
    clock.tick(30)

