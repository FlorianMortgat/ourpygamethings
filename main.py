#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pygame, sys, os, time, random, math
from pygame.locals import *
#sttings before pgame starts up:
pygame.init()

winx = 750
winy = 500
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.Font(None, 20)

win = pygame.display.set_mode((winx, winy))
pygame.display.set_caption("name")

class Platform():
    def __init__(self, xpos, ypos, length, color):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.height = 25
        self.color = color
        self.deltax = 0
        self.deltay = 0
    def show(self):
        if self.xpos < winx and self.ypos < winy:
            pygame.draw.rect(win, pygame.Color(self.color), (self.xpos, self.ypos, self.length, self.height))
            self.showing = True
    def accelerate(self, accx, accy):
        self.deltax += accx
        self.deltay += accy
    def move(self):
        old_xpos, old_ypos = self.xpos, self.ypos
        self.xpos += self.deltax
        self.ypos += self.deltay
        if self.xpos >= winx - self.length or self.xpos <= 0:
            self.deltax = -self.deltax
        if self.ypos >= winy - self.height or self.ypos <= 0:
            self.deltay = -self.deltay

class Player():
    def __init__(self, height, size, jump_impulse, speed, color, movement_type): #movemet type = arrows/wasd/numpad
        self.height = height
        self.size = float(size)
        self.jump_impulse = float(jump_impulse)
        self.speed = float(speed)
        self.color = pygame.Color(str(color))
        self.movement_type = str(movement_type)
        self.actions = ['up', 'down', 'left', 'right', 'shoot']
        self.controls = {
            'up': 0,
            'down': 0,
            'left': 0,
            'right': 0,
            'shoot': 0,
        }


    def attach_to_window(self, win):
        self.win = win
    def attach_to_platform(self, platform):
        if self.body.collidepoint(platform):
            if self.x_speed == 0 and self.y_speed == 0:
                self.x_speed += platform.deltax
                self.y_speed += platform.deltay
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
    def show(self):
        self.body = pygame.draw.circle(self.win, self.color, (self.xpos, self.ypos), self.size)

class Button:
    '''
    A clickable button
    '''
    def __init__(self, text, pos, action):
        self.text = text
        self.rendered_text = font1.render(self.text, 0, pygame.Color('#ffffff'))
        self.rect = self.rendered_text.get_rect()
        self.rect.width = 50
        self.pos = pos
        self.rect = self.rect.move(pos)
        self.action = action
        self.action_arg = text
    def show(self):
        pygame.draw.rect(win, pygame.Color(0,0,0), self.rect)
        win.blit(self.rendered_text, self.rect)
    def checkHovered(self, event):
        if (event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos)):
            self.action(self, self.action_arg)
    def checkClicked(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if self.rect.collidepoint(event.pos):
                self.action(self, self.action_arg)
    def setText(self, new_text):
        self.text = new_text
        self.rendered_text = font1.render(self.text, 0, pygame.Color('#ffffff'))
        self.rect = self.rendered_text.get_rect()
        self.rect.width = 50
        self.rect = self.rect.move(self.pos)


def main():
    players = []
    players.append(Player(6, 10, 1, 1, "#660066", 'arrows'))
    setupControl(players[0])

# this should be a class (would be easier because it needs to have a state)

class ControlSettings:
    def __init__(self):
        pass
    def setupControls(self, player):
        pass

class O: ''

def setupControl(player):
    '''
    Will allow a player to setup a keyboard key for a control
    :param player: A Player instance
    :return:
    '''
    this = O()
    this.action = 'noaction'
    this.button = None
    def setCurrentControl(button, control): # if it were a class, this ugly function would be a beautiful method :D
        print('current control becomes {}'.format(control))
        this.action = control
        this.button = button

    loop1 = True

    k = 0;
    text = {}
    buttons = [
        Button('up',    (182, 220), setCurrentControl),
        Button('down',  (182, 250), setCurrentControl),
        Button('left',  (122, 250), setCurrentControl),
        Button('right', (242, 250), setCurrentControl),
    ]
    while loop1:
        win.fill((0,100,50))
        if this.action in player.controls:
            txt = '{}: {}'.format(this.action, player.controls[this.action])
        else:
            txt = ''
        win.blit(font2.render(txt, 1, (255,0,0)), (0,0))

        for button in buttons:
            button.show()

        # when i test it it just goes right into the game though
        # because no one calls setupControl() in the main thread
        #key_up_input    = pygame.draw.rect(win, ((255,0,0)), (162, 250), (75, 75))
        #key_down_input  = pygame.draw.rect(win, ((255,0,0)), (325, 250), (75, 75))
        #key_left_input  = pygame.draw.rect(win, ((255,0,0)), (487, 250), (75, 75))
        #key_right_input = pygame.draw.rect(win, ((255,0,0)), (650, 250), (75, 75))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop1 = False
            elif event.type == pygame.KEYDOWN:
                k = event.key
                # we map the key to the action for that player
                if (this.action in player.actions):
                    player.controls[this.action] = event.key
                    if this.button is not None:
                        this.button.setText(str(event.key))
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in buttons:
                    button.checkHovered(event)
                #if mouse_pos.collidepoint(key_up_input):
                #    for k in event.key:
                #        'What is this supposed to do?'
                        #text[key_up_input] = font1.render(str(k))
                        #text[key_up_input].blit(win, (162.5, 250))
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.checkClicked(event)


        pygame.display.update()
        time.sleep(0.1)

if __name__ == '__main__':
    main()

'''G
plt = {}  #platforms


loop = True
plt['plt1'] = Platform(400, 100, 150, 'yellow')

plt['plt2'] = Platform(0, 100, 150, 'purple')
win.fill((100, 100, 100))

while loop:

    plt['plt1'].move()
    plt['plt2'].move()

    for platformNumber in plt:
        plt[platformNumber].show()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        plt['plt1'].accelerate(-0.05, 0)
    if keys[pygame.K_RIGHT]:
        plt['plt1'].accelerate( 0.05, 0)
    if keys[pygame.K_UP]:
        plt['plt1'].accelerate(0, -0.05)
    if keys[pygame.K_DOWN]:
        plt['plt1'].accelerate(0,  0.05)

    if keys[pygame.K_a]:
        plt['plt2'].accelerate(-0.05, 0)
    if keys[pygame.K_d]:
        plt['plt2'].accelerate( 0.05, 0)
    if keys[pygame.K_w]:
        plt['plt2'].accelerate(0, -0.05)
    if keys[pygame.K_s]:
        plt['plt2'].accelerate(0,  0.05)
    if keys[pygame.K_ESCAPE]:
        loop = False
    pygame.display.update()
    time.sleep(0.01)
'''