# STEP 1: Basics------------------------------------------------------
from typing import NewType
import pygame
import os

# -------------------------------------------------------------------

# Step 1: Setting up the basics
# Step 2: Setting the background and display it
# Step 3: Setting the font for the text and display the text
# Step 4: Create an abstract class, Rocket, that will help to build Player and Enemy class
# Step 5: Create movement styles for the hero rocket, like registering the keyboard inputs
# Step 6: Create the player class, our hero and its features
# Step 7: Create the enemy class and its features
# Step 8: Create lasers and its functions
# Step 9: Enemy firing bullets
# Step 10: Implement collision between player and enemy
# Step 11: Create main menu


# STEP 3: Set font for display------------------------------------------------------

pygame.font.init()

# -------------------------------------------------------------------

# STEP 1 Basics------------------------------------------------------
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War Game")

# Load images of enemy
ENEMY_ROCKET_1 = pygame.image.load(
    os.path.join("images", "enemy_rocket_red.png"))
ENEMY_ROCKET_2 = pygame.image.load(
    os.path.join("images", "enemy_rocket_grey.png"))

# Player
HERO_ROCKET = pygame.image.load(
    os.path.join("images", "hero_rocket1.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("images", "red_laser.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("images", "green_laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("images", "blue_laser.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("images", "yellow_laser.png"))

# -------------------------------------------------------------------

# STEP 2: Set bg and labels------------------------------------------------------
# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("images", "background-black3.png")), (WIDTH, HEIGHT))

# ------------------------------------------------------


# STEP 8: Create Laser------------------------------------------------------


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


# ------------------------------------------------------


# STEP 4- Create an abstract class ------------------------------------------------------


class Rocket:

    # Step 8 ------------
    COOLDOWN = 30
    # ------------------

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.rocket_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.rocket_img, (self.x, self.y))
    # Step 8 -------------------------
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 20
                self.lasers.remove(laser)

    # -----------------------------
# -------------------------------------------------------------------

    # Step 8 -----------------------------------------------
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # -------------------------------------------------

    def get_width(self):
        return self.rocket_img.get_width()

    def get_height(self):
        return self.rocket_img.get_height()


# STEP 6- Create our hero ------------------------------------------------------

class Player(Rocket):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.rocket_img = HERO_ROCKET
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.rocket_img)
        self.max_health = health

    # Step 8 ----------------------------------

    def move_lasers(self, vel, objs):
        score = 0
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # ----------------------------------------


# -------------------------------------------------------------------

# STEP 7- Create enemy ------------------------------------------------------


class Enemy(Rocket):
    COLOR_MAP = {
        "red": (ENEMY_ROCKET_1, RED_LASER),
        "grey": (ENEMY_ROCKET_2, GREEN_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.rocket_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.rocket_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# -------------------------------------------------------------------

# step 8 ------------------------------------------------


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# --------------------------------------------------------------
