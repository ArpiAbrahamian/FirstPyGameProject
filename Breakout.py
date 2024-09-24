import pygame
import random

from pygame.examples.cursors import color_cursor
from pygame.examples.moveit import WIDTH, HEIGHT

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()


class Player(pygame.Rect):

    def __init__(self, x, y):
        super().__init__(x, y, 100, 25) # arbitrary values TODO tweak
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'tan', self, 0) # fill
        pygame.draw.rect(screen, 'gray', self, 1) # outline

    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball(pygame.Rect):
    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(4, 7) * random.choice([1,-1])
        self.vy = random.randint(4,5) # TODO tweak

    def draw(self):
        pygame.draw.ellipse(screen, 'blue', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 and self.vx < 0:
            self.vx *= -1
        elif self.x + self.width > screen.get_width() and self.vx > 0:
            self.vx *= -1
        elif self.y < 0 and self.vy < 0:
            self.vy *= -1
        elif self.y + self.height > screen.get_height() and self.vy > 0:
            self.y = screen.get_height()//2 + 20
            self.x = screen.get_width()//2 - 10
            self.vx = random.randint(1, 4) * random.choice([1, -1])
            self.vy = random.randint(3, 4)

class Brick(pygame.Rect):
    WIDTH = 112
    HEIGHT = 35
    def __init__(self, x, y):
        super().__init__(x, y, Brick.WIDTH, Brick.HEIGHT)
        self.color = (random.randint(200,255), random.randint(50,255), random.randint(50,255))


    def draw(self):
        pygame.draw.rect(screen, self.color, self, 3)  # fill

player = Player(screen.get_width()/2 - 50, screen.get_height() - 50 ) # arbitrary values TODO tweak
ball = Ball(screen.get_width()/2 - 10, screen.get_height()/ 2 + 20, 20) # arbitrary values TODO tweak

brick_list = []

space = 15

for x in range(space, screen.get_width(), Brick.WIDTH + space):
    for y in range(space, 340, Brick.HEIGHT + space):
        brick_list.append(Brick(x,y))


while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += -10
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += 10

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += 10
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += -10

    # Do logical updates here.
    player.update()
    ball.update()
    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width # perhaps sideways collision would look better?
        diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        ball.vx += diff // 10

    for brick in brick_list:
        if ball.colliderect(brick):
            brick_list.remove(brick)
            ball.vy *= -1


    screen.fill('black')  # Fill the display with a solid color

    # Render the graphics here.

    for b in brick_list:
        b.draw()
    player.draw()
    ball.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
