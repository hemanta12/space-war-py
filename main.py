# STEP 1: Basics------------------------------------------------------
import pygame
import time
import random
import features as fe
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

# STEP 1  Basics------------------------------------------------------


def main():
    pygame.init()
    run = True
    main.FPS = 60
    main.score = 0
    # main.highest_score = 0

    def update_score():
        current_time = time.time()
        while current_time > 0:
            main.score += 1
            # main.highest_score = main.score
            current_time = 0

    clock = pygame.time.Clock()
# -------------------------------------------------------------------

# STEP 3: Set font for display------------------------------------------------------

    main_font = pygame.font.SysFont("comicsans", 20)

    # Step 7---------------------
    enemies = []
    wave_length = 4
    enemy_vel = 2

    lost = False
    lost_count = 0

    # ------------------

    # Step 6-----------------
    player_vel = 5
    # ------------------

    # step 8 --------
    laser_vel = 8
    # ---------------

    player = fe.Player(300, 605)


# -------------------------------------------------------------------

    # score function

    # def score_counter(score):


    def display_score():
        score_label = main_font.render(
            f"Score: {main.score}", 1, (255, 255, 255))
        fe.WIN.blit(score_label, (fe.WIDTH - score_label.get_width()-10, 10))

        # highest_score_label = main_font.render(
        #     f"Highest Score: {(main.highest_score)}", 1, (255, 255, 255))
        # fe.WIN.blit(highest_score_label,
        #             (fe.WIDTH - highest_score_label.get_width()-10, 35))


# STEP 2: Set bg and labels------------------------------------------------------

    def redraw_window():
        fe.WIN.blit(fe.BG, (0, 0))

        # draw text
        health_label = main_font.render(
            f"Health: {player.health}", 1, (255, 255, 255))

        fe.WIN.blit(health_label, (10, 10))

        # Step 7---------------------
        for enemy in enemies:
            enemy.draw(fe.WIN)

        if lost:
            lost_label = main_font.render("Game Over!!", 1, (255, 255, 255))
            fe.WIN.blit(lost_label, (fe.WIDTH/2 -
                        lost_label.get_width()/2, 350))
        # -----------------

        # Step: 6-----------
        player.draw(fe.WIN)
        # ------------------
        display_score()

        pygame.display.update()
# ------------------------------------------------------

# STEP 1  Basics------------------------------------------------------

    while run:
        clock.tick(main.FPS)
        redraw_window()

        # Step 7--------------
        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > main.FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            wave_length += 4
            for i in range(wave_length):
                enemy = fe.Enemy(random.randrange(
                    50, fe.WIDTH-100), random.randrange(-2500, -100), random.choice(["red", "grey"]))
                enemies.append(enemy)
        # -----------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
# -------------------------------------------------------------------


# STEP 5: Movements-----------------------------------------------------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < fe.WIDTH:  # right
            player.x += player_vel

        # step 8 ------------------------
        if keys[pygame.K_SPACE]:
            player.shoot()
        # ----------------------
# -------------------------------------------------------------------

        # step 7--------------
        for enemy in enemies:
            enemy.move(enemy_vel)

            # step 8 ------------
            enemy.move_lasers(laser_vel, player)
            # -----------------

            # Step 9 enemy firing bullet
            if random.randrange(0, 2*120) == 1:
                enemy.shoot()

            # -----------------------------

            # step 10, check enemy and player colliding
            if fe.collide(enemy, player):
                player.health -= 10
                if main.score > 50:
                    main.score -= 50
                enemies.remove(enemy)
            # --------------------

            elif enemy.y + enemy.get_height() > fe.HEIGHT:
                enemies.remove(enemy)

        # ---------------

        # step 8
        player.move_lasers(-laser_vel, enemies)
        # --------------------

        update_score()


def main_menu():
    menu_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        fe.WIN.blit(fe.BG, (0, 0))
        menu_label = menu_font.render(
            "Click anywhere to start...", 1, (255, 255, 255))
        fe.WIN.blit(menu_label, (fe.WIDTH/2 - menu_label.get_width()/2, 350))
        # main.highest_score

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                main()

    pygame.quit()


main_menu()
