import pygame
from pygame.locals import *
import time
import random

size = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*size
        self.y = random.randint(1,19)*size

class snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = "down" 

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length-1 , 0 , -1):
            self.x[i]= self.x[i-1]
            self.y[i]= self.y[i-1]

        if self.direction == "left":
            self.x[0] -=size
        if self.direction == "right":
            self.x[0] +=size
        if self.direction == "up":
            self.y[0] -=size
        if self.direction == "down":
            self.y[0] +=size

        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        pygame.mixer.init()
        self.play_background_music()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1,0)


    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def reset(self):
        self.snake = snake(self.surface,1)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def show_game_over(self):
        self.render_background()
        pygame.mixer.music.pause()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                self.snake.increase_length()
                self.apple.move()
            
            

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"

        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"
                
        
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if not pause:
                     
                        if event.key== K_UP:
                           self.snake.move_up()

                        if event.key== K_DOWN:
                            self.snake.move_down()

                        if event.key== K_RIGHT:
                            self.snake.move_right()

                        if event.key== K_LEFT:
                            self.snake.move_left()  

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

if __name__ == "__main__":
    game= Game()
    game.run()
