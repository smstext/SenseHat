#Martin O'Hanlon
#www.stuffaboutcode.com
#Astro Pi Snake
from random import randint
from sense_hat import SenseHat
from time import sleep
import pygame
from pygame.locals import *

class AstroPiSnake():
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

    BACKCOL = [0, 0, 0]
    SNAKECOL = [0, 0, 155]
    APPLECOL = [0, 155, 0]
    
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((640, 480))
        
        self.ap = SenseHat()
        
    def startGame(self):
        self.ap.clear(self.BACKCOL)
        self.direction = self.UP
        self.length = 3
        self.tail = []
        self.tail.insert(0, [4, 4])
        self.createApple()
        self.score = 0
        
        playing = True
        while(playing):
            sleep(0.5)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self._handle_event(event)
            playing = self.move()

        self.ap.clear()

    def _handle_event(self, event):
        if event.key == pygame.K_DOWN:
            self.down()
        elif event.key == pygame.K_UP:
            self.up()
        elif event.key == pygame.K_LEFT:
            self.left()
        elif event.key == pygame.K_RIGHT:
            self.right()
        
    def createApple(self):
        badApple = True
        #try and fnd a location for the apple
        while(badApple):
            x = randint(0, 7)
            y = randint(0, 7)
            badApple = self.checkCollision(x, y)
        self.apple = [x, y]
        self.ap.set_pixel(x, y, self.APPLECOL)

    def checkCollision(self, x, y):
        #is this outside the screen
        if x > 7 or x < 0 or y > 7 or y < 0:
            return True
        else:
            #or in the snakes tail
            for segment in self.tail:
                if segment[0] == x and segment[1] == y:
                    return True
            else:
                return False

    def addSegment(self, x, y):
        #create the new segment of the snake
        self.ap.set_pixel(x, y, self.SNAKECOL)
        self.tail.insert(0, [x, y])
        
        #do I need to clear a segment
        if len(self.tail) > self.length:
            lastSegment = self.tail[-1]
            self.ap.set_pixel(lastSegment[0], lastSegment[1], self.BACKCOL)
            self.tail.pop()
        
    def move(self):
        #work out where the new segment of the snake will be
        newSegment = [self.tail[0][0], self.tail[0][1]]
        if self.direction == self.UP:
            newSegment[1] -= 1
        elif self.direction == self.DOWN:
            newSegment[1] += 1
        elif self.direction == self.LEFT:
            newSegment[0] -= 1
        elif self.direction == self.RIGHT:
            newSegment[0] += 1

        if self.checkCollision(newSegment[0], newSegment[1]):
            #game over
            snakehead = self.tail[0]
            for flashHead in range(0,5):
                self.ap.set_pixel(snakehead[0], snakehead[1], self.SNAKECOL)
                sleep(0.2)
                self.ap.set_pixel(snakehead[0], snakehead[1], self.BACKCOL)
                sleep(0.2)
            self.ap.show_message("Score = {}".format(self.score), text_colour = self.APPLECOL)
            
        else:
            self.addSegment(newSegment[0], newSegment[1])

            #has the snake eaten the apple?
            if newSegment[0] == self.apple[0] and newSegment[1] == self.apple[1]:
                self.length += 1
                self.score += 10
                self.createApple()

            return True
            
    def up(self):
        if self.direction != self.DOWN:
            self.direction = self.UP

    def down(self):
        if self.direction != self.UP:
            self.direction = self.DOWN

    def left(self):
        if self.direction != self.RIGHT:
            self.direction = self.LEFT

    def right(self):
        if self.direction != self.LEFT:
            self.direction = self.RIGHT

if __name__ == "__main__":

    snake = AstroPiSnake()
    print("Press Escape to quit")
    print("Press Joystick to start")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    snake.startGame()

