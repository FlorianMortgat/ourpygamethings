#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pygame
import sys
import os
import time
import random
import math
from pygame.locals import *
import re

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
    def __init__(self, name, height, size, jump_impulse, speed, color, movement_type): #movemet type = arrows/wasd/numpad
        self.name = name
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
    A clickable/hoverable button
    '''
    def __init__(self, text, pos, action, action_arg = None):
        self.text = text
        self.rendered_text = font1.render(self.text, 0, pygame.Color('#ffffff'))
        self.rect = self.rendered_text.get_rect()
        self.rect.width = 50
        self.pos = pos
        self.rect = self.rect.move(pos)
        self.action = action
        self.action_arg = action_arg
        if self.action_arg is None:
            self.action_arg = text
    def show(self):
        '''Display the button on the main window'''
        pygame.draw.rect(win, pygame.Color(0,0,0), self.rect)
        win.blit(self.rendered_text, self.rect)
    def checkHovered(self, event):
        '''Will run self.action if the mouse hovers over the button.'''
        if (event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos)):
            self.action(self, self.action_arg)
    def checkClicked(self, event):
        '''Will run self.action if a click has been registered inside the button'''
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if self.rect.collidepoint(event.pos):
                self.action(self, self.action_arg)
    def setText(self, new_text):
        '''Change the displayed text of the button'''
        self.text = new_text
        self.rendered_text = font1.render(self.text, 0, pygame.Color('#ffffff'))
        self.rect = self.rendered_text.get_rect()
        self.rect.width = 50
        self.rect = self.rect.move(self.pos)


def main():
    players = []
    assigned_keys = set()
    players.append(Player('1', 6, 10, 1, 1, "#660066", 'arrows'))
    players.append(Player('2', 6, 10, 1, 1, "#660066", 'arrows'))
    for player in players:
        if not setupControl(player, assigned_keys):
            return
        print 'Controls for Player {}:'

class ControlSettings:
    '''This class will replace the setupControl() function (it will be cleaner as a class)'''
    def __init__(self):
        pass
    def setupControls(self, player):
        pass

class O:
    '''An empty class to create schema-less objects'''

def setupControl(player, blocked_keys):
    '''
    Will allow a player to setup a keyboard key for a control
    :param player: A Player instance
    :return: False if we should exit the game, True if we can continue
    '''
    this = O()
    this.action = 'noaction'
    this.button = None
    this.next_step = False
    setupText = font2.render('Setup controls for player {}'.format(player.name), 1, (255, 0, 0))
    this.timerKeyAlreadyUsed = 0
    maxTimerKeyAlreadyUsed = 10

    def setCurrentControl(button, control): # if it were a class, this ugly function would be a beautiful method :D
        '''This is the function that gets called when one of the hover buttons is hovered'''
        this.action = control
        this.button = button

    def onBtnOK(button, arg):
        '''This is the function that gets called when the OK button is clicked'''
        this.next_step = True # we clicked on the button = we want to go to the next step

        # but… if one of the "controls" buttons has a non-number text on it, it means
        # the player hasn't chosen a key yet, so we can't go to the next step.
        for hover_button in hover_buttons:
            if not re.match('\d+', hover_button.text):
                this.next_step = False
                return

    k = 0;
    text = {}
    hover_buttons = [
        Button('up',    (182, 220), setCurrentControl),
        Button('down',  (182, 250), setCurrentControl),
        Button('left',  (122, 250), setCurrentControl),
        Button('right', (242, 250), setCurrentControl),
    ]
    click_buttons = [
        Button('OK',    (500, 460), onBtnOK),
    ]
    all_buttons = hover_buttons + click_buttons

    while not this.next_step:
        win.fill((0, 100, 50))
        if this.action in player.controls:
            currentControlText = 'Setup player {}... {} = {}'.format(player.name, this.action, player.controls[this.action])
        else:
            currentControlText = ''
        win.blit(setupText, (0, 0))
        win.blit(font2.render(currentControlText, 1, (255, 0, 0)), (0, 30))
        if this.timerKeyAlreadyUsed:
            keyAlreadyUsed = font1.render('KEY ALREADY IN USE', 1, (int(this.timerKeyAlreadyUsed * 255 / maxTimerKeyAlreadyUsed), 0, 0))
            win.blit(keyAlreadyUsed, (0, 60))

        for button in all_buttons:
            button.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # we map the key to the action for that player
                if (this.action in player.actions):
                    if event.key in blocked_keys:
                        this.timerKeyAlreadyUsed = maxTimerKeyAlreadyUsed
                        continue
                    if player.controls[this.action]:
                        # the old key is now free, we unblock it
                        blocked_keys.remove(player.controls[this.action])
                    player.controls[this.action] = event.key
                    # the new key is now blocked
                    blocked_keys.add(event.key)
                    if this.button is not None:
                        this.button.setText(str(event.key))
            elif event.type == pygame.MOUSEMOTION:
                for button in hover_buttons:
                    button.checkHovered(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in click_buttons:
                    button.checkClicked(event)

        this.timerKeyAlreadyUsed = max(0, this.timerKeyAlreadyUsed - 1)

        pygame.display.update()
        time.sleep(0.1)
    return True

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