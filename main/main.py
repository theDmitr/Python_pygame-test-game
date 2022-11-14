import pygame as pg
from random import randint
from app import *

class Scene:
    def setScene(scene):
        Scene.currentScene = scene
        scene.init()
    def playScene():
        Scene.currentScene.run()

class Menu:
    def init():
        Button.items = list()
        Menu.buttonQuit = Button(400 - 200 - 75, 400 - 170, 150, 50, (250, 80, 30), (100, 100, 100), "Quit")
        Menu.buttonSettings = Button(400 - 200 - 75, Menu.buttonQuit.aabb.top - 60, 150, 50, (200, 120, 40), (100, 100, 100), "Settings")
        Menu.buttonPlay = Button(400 - 200 - 75, Menu.buttonSettings.aabb.top - 60, 150, 50, (180, 150, 50), (100, 100, 100), "Play")
    def run():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if Menu.buttonPlay.aabb.collidepoint(event.pos):
                    Scene.setScene(Play)
                    return
                elif Menu.buttonSettings.aabb.collidepoint(event.pos):
                    Scene.setScene(Settings)
                    return
                elif Menu.buttonQuit.aabb.collidepoint(event.pos):
                    quit()
            elif event.type == pg.MOUSEMOTION:
                for item in Button.items:
                    if item.aabb.collidepoint(event.pos): 
                        item.animation = True
                    else: item.animation = False
        clock.tick(60)
        screen.fill((200, 200, 200))
        for item in Button.items: item.draw()
        pg.display.update()

class Play:
    player = None
    enemy = None
    enemies = None
    loose = False
    def init():
        Play.player = Player(0, 0, 50, 50, 3, 20)
        Play.player.aabb.move_ip(175, 325)
        enemies = list()
        enemy = Enemy(0, 0, 50, 50, 1, 20)
        enemy.aabb.x = randint(50, 350)
        enemy.aabb.y = 50
        enemies.append(Play.enemy)
        enemy.moveRight = True
        Play.loose = False
    def run():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    Play.player.moveTop = True
                if event.key == pg.K_s:
                    Play.player.moveDown = True
                if event.key == pg.K_d:
                    Play.player.moveRight = True
                if event.key == pg.K_a:
                    Play.player.moveLeft = True
                if event.key == pg.K_SPACE:
                    if Play.player.tempValue == 1:
                        Shell(Play.player.aabb.centerx, Play.player.aabb.y, Play.player, 5, 0, -3)
                        Play.player.tempTime = pg.time.get_ticks()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    Play.player.moveTop = False
                if event.key == pg.K_s:
                    Play.player.moveDown = False
                if event.key == pg.K_d:
                    Play.player.moveRight = False
                if event.key == pg.K_a:
                    Play.player.moveLeft = False
        # // Player`s shot cooldown
        Play.player.tempValue = ((pg.time.get_ticks() - Play.player.tempTime) / 600) # 0.6 seconds
        if Play.player.tempValue > 1: Play.player.tempValue = 1
        # //
        for index, item in enumerate(Creature.items):
            if item.health <= 0:
                if item == Play.player: Play.loose = True
                Creature.items.clear()
                Shell.shells.clear()
                Scene.setScene(Prompt)
                return
            # // Move control
            if item.moveLeft:
                item.aabb.x -= item.speed
                if item.aabb.x < 0: item.aabb.x = 0
            if item.moveRight:
                item.aabb.x += item.speed
                if item.aabb.right > 400: item.aabb.right = 400
            # //
            # // Shells control
            for index, shell in enumerate(Shell.shells):
                if shell.aabb.colliderect(item.aabb) and shell.sender != item:
                    item.makeDamage(shell.damage)
                    Shell.shells.pop(index)
                    continue
                if shell.aabb.y < 0 or shell.aabb.y > 400 or shell.aabb.x < 0 or shell.aabb.x > 400: 
                    Shell.shells.pop(index)
                shell.aabb.x += shell.speed[0]
                shell.aabb.y += shell.speed[1]
            #//
            if item == Play.player: continue
            # // Enemy controls
            # // Swap speed
            if item.aabb.right + 3 > 400:
                item.moveRight = False
                item.moveLeft = True
            elif item.aabb.left - 3 < 0:
                item.moveRight = True
                item.moveLeft = False
            #item.aabb.move_ip(item.speed, 0)
            # //
            # Shot control

            # //
            # //
        clock.tick(60)
        screen.fill((255, 200, 230))
        for shell in Shell.shells:
            shell.draw()
        for item in Creature.items:
            item.draw()
        pg.draw.rect(screen, (30, 0, 0), frameRect, 4)
        pg.display.flip()

class Settings:
    def init():
        Button.items = list()
        Settings.buttonMenu = Button(400 - 200 - 75, 400 - 170, 150, 50, (200, 120, 40), (100, 100, 100), "Menu")
        Settings.label = myFont.render("В разработке...", True, (150, 150, 220))
        Settings.labelRect = Settings.label.get_rect(center = (400 / 2, Settings.buttonMenu.aabb.top - 50))
    def run():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if Settings.buttonMenu.aabb.collidepoint(event.pos):
                    Scene.setScene(Menu)
                    return
            elif event.type == pg.MOUSEMOTION:
                for item in Button.items:
                    if item.aabb.collidepoint(event.pos): 
                        item.animation = True
                    else: item.animation = False
        clock.tick(60)
        screen.fill((200, 200, 200))
        for item in Button.items: item.draw()
        screen.blit(Settings.label, Settings.labelRect)
        pg.display.update()

class Prompt:
    def init():
        Button.items = list()
        if Play.loose == False:
            text = "Победа!"
            color = (0, 200, 0)
        else:
            text = "Поражение!"
            color = (200, 0, 0)
        Prompt.buttonMenu = Button(400 - 200 - 75, 400 - 170, 150, 50, (200, 120, 40), (100, 100, 100), "Menu")
        Prompt.buttonPlay = Button(400 - 200 - 75, Prompt.buttonMenu.aabb.top - 60, 150, 50, (180, 150, 50), (100, 100, 100), "Play")
        Prompt.label = myFont.render(text, True, color)
        Prompt.labelRect = Prompt.label.get_rect(center = (400 / 2, Prompt.buttonPlay.aabb.top - 50))
    def run():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if Prompt.buttonMenu.aabb.collidepoint(event.pos):
                    Scene.setScene(Menu)
                    return
                elif Prompt.buttonPlay.aabb.collidepoint(event.pos):
                    Scene.setScene(Play)
                    return
            elif event.type == pg.MOUSEMOTION:
                for item in Button.items:
                    if item.aabb.collidepoint(event.pos): 
                        item.animation = True
                    else: item.animation = False
        clock.tick(60)
        screen.fill((200, 200, 200))
        for item in Button.items: item.draw()
        screen.blit(Prompt.label, Prompt.labelRect)
        pg.display.update()

Scene.setScene(Menu)
while True:
    Scene.playScene()