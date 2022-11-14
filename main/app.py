import pygame as pg
from random import randint

pg.init()
pg.display.set_caption("Game")
screen = pg.display.set_mode((400, 400))
clock = pg.time.Clock()
frameRect = pg.Rect(0, 0, 400, 400)
myFont = pg.font.Font(None, 36)

class AABB:
    def __init__(self, x, y, w, h):
        self.aabb = pg.Rect(x, y, w, h)

class Button(AABB):
    items = list()
    animation = False
    tempTime = 0
    def __init__(self, x, y, w, h, color1, color2, text):
        super().__init__(x, y, w, h)
        self.aabbBack = self.aabb.copy()
        self.aabbBack.x -= 5
        self.aabbBack.y += 5
        self.color1 = color1
        self.color2 = color2
        self.text = myFont.render(text, True, self.color2)
        self.textRect = self.text.get_rect(center=(self.aabb.centerx, self.aabb.centery))
        Button.items.append(self)
    def draw(self):
        if self.animation and pg.time.get_ticks() - self.tempTime > 30 and self.aabbBack.right < self.aabb.right + 5:
            self.aabbBack.right += 3
            self.color2 = self.color2[0] - 5, self.color2[1] - 5, self.color2[2] - 5
            self.tempTime = pg.time.get_ticks()
        elif not self.animation and pg.time.get_ticks() - self.tempTime > 30 and self.aabbBack.left > self.aabb.left - 5:
            self.color2 = self.color2[0] + 5, self.color2[1] + 5, self.color2[2] + 5
            self.aabbBack.left -= 3
            self.tempTime = pg.time.get_ticks()
        pg.draw.rect(screen, self.color1, self.aabbBack, 3)
        pg.draw.rect(screen, self.color1, self.aabb)
        screen.blit(self.text, self.textRect)

class Entity(AABB):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color

class Creature(Entity):
    items = list()
    moveDown = False
    moveTop = False
    moveLeft = False
    moveRight = False
    def __init__(self, x, y, w, h, color, speed, health):
        super().__init__(x, y, w, h, color)
        self.speed = speed
        self.health = health
        self.startHealth = health
        Creature.items.append(self)
    def makeDamage(self, value):
        self.health -= value
    def draw(self):
        pg.draw.rect(screen, self.color, self.aabb)
        pg.draw.rect(screen, (50, 50, 50), pg.Rect(self.aabb.x, self.aabb.y - 7, self.aabb.w, 4))
        pg.draw.rect(screen, (50, 200, 50), pg.Rect(self.aabb.x, self.aabb.y - 7, self.aabb.w * (self.health / self.startHealth), 4))

class Player(Creature):
    tempTime = 0
    tempValue = 0
    def __init__(self, x, y, w, h, speed, health):
        super().__init__(x, y, w, h, (0, 255, 0), speed, health)
    def draw(self):
        super().draw()
        pg.draw.rect(screen, (200, 100, 50), pg.Rect(self.aabb.x, self.aabb.y - 12, self.aabb.w * self.tempValue, 4))

class Enemy(Creature):
    def __init__(self, x, y, w, h, speed, health):
        super().__init__(x, y, w, h, (255, 0, 0), speed, health)

class Shell(Entity):
    shells = list()
    def __init__(self, x, y, sender, damage, s1, s2):
        super().__init__(0, 0, 5, 5, (100, 100, 100))
        self.sender = sender
        self.damage = damage
        self.aabb = pg.Rect(x, y, 5, 5)
        self.speed = (s1, s2)
        Shell.shells.append(self)
    def draw(self):
        pg.draw.rect(screen, self.color, self.aabb)