# Written by Stephan T. Lavavej.
# SPDX-License-Identifier: CC0-1.0

# Derived from:
# https://github.com/takluyver/pygame/blob/master/examples/moveit.py
# https://github.com/takluyver/pygame/blob/master/examples/stars.py
# https://github.com/takluyver/pygame/tree/master/examples#readme
# "The source code for these examples is in the public domain.
# Feel free to use for your own projects."

# Resources:
# https://pixelfrog-assets.itch.io/pixel-adventure-1
# https://pixelfrog-assets.itch.io/pixel-adventure-2
# Animation speed: 20 FPS, 50 ms
# "These assets are released under a Creative Commons Zero (CC0) license.
# You can distribute, remix, adapt, and build upon the material in any medium
# or format, even for commercial purposes. Attribution is not required."

import pygame


def load_image(filename):
    return pygame.image.load(filename).convert_alpha()


def zoom_image(img, zoom):
    width = img.get_width()
    height = img.get_height()
    return pygame.transform.scale(img, (width * zoom, height * zoom))


class GameObject:
    def __init__(self, img):
        self.image = img
        self.position = img.get_rect()

    def move_by(self, x, y):
        self.position.move_ip(x, y)


class AnimatedGameObject:
    def __init__(self, anim, frame_ms):
        self.animation = anim
        self.total_milliseconds = frame_ms * len(anim)
        self.frame_milliseconds = frame_ms
        self.position = anim[0].get_rect()

    def get_image(self, ticks):
        ticks_modulo_total = ticks % self.total_milliseconds
        frame_number = ticks_modulo_total // self.frame_milliseconds
        return self.animation[frame_number]

    def move_by(self, x, y):
        self.position.move_ip(x, y)


def main():
    # *** Initialize pygame ***
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT),
                                     flags=pygame.FULLSCREEN | pygame.SCALED)
    clock = pygame.time.Clock()

    # *** Load images and construct game objects ***
    background_img = load_image(
        'resources/Pixel Adventure 1/Free/Background/Blue.png')
    draw_background = True

    virtual_guy_img_1x = load_image(
        'resources/Pixel Adventure 1/Free/Main Characters/Virtual Guy/Jump (32x32).png'
    )
    virtual_guy_img_2x = zoom_image(virtual_guy_img_1x, 2)
    virtual_guy = GameObject(virtual_guy_img_2x)
    virtual_guy.move_by(350, 300)

    duck_img_1x = load_image(
        'resources/Pixel Adventure 2/Enemies/Duck/Jump (36x36).png')
    duck_img_2x = zoom_image(duck_img_1x, 2)
    duck = GameObject(duck_img_2x)
    duck.move_by(450, 300)

    slime_sheet = load_image(
        'resources/Pixel Adventure 2/Enemies/Slime/Idle-Run (44x30).png')
    slime_animation = []
    for i in range(0, 10):
        animation_frame_1x = slime_sheet.subsurface((i * 44, 0), (44, 30))
        animation_frame_2x = zoom_image(animation_frame_1x, 2)
        slime_animation.append(animation_frame_2x)
    slime = AnimatedGameObject(anim=slime_animation, frame_ms=50)
    slime.move_by(400, 400)

    # *** Game loop ***
    while True:
        ticks = pygame.time.get_ticks()  # current time, used for animations

        # *** Handle events (like keyboard input and mouse input) ***
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_SPACE:
                    draw_background = not draw_background
                elif event.key == pygame.K_LEFT:
                    virtual_guy.move_by(-10, 0)
                elif event.key == pygame.K_RIGHT:
                    virtual_guy.move_by(10, 0)
                elif event.key == pygame.K_UP:
                    virtual_guy.move_by(0, -10)
                elif event.key == pygame.K_DOWN:
                    virtual_guy.move_by(0, 10)
                elif event.key == pygame.K_a:
                    duck.move_by(-40, 0)
                elif event.key == pygame.K_d:
                    duck.move_by(40, 0)
                elif event.key == pygame.K_w:
                    duck.move_by(0, -40)
                elif event.key == pygame.K_s:
                    duck.move_by(0, 40)
                elif event.key == pygame.K_j:
                    slime.move_by(-20, 0)
                elif event.key == pygame.K_l:
                    slime.move_by(20, 0)
                elif event.key == pygame.K_i:
                    slime.move_by(0, -20)
                elif event.key == pygame.K_k:
                    slime.move_by(0, 20)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left button
                    virtual_guy.position.center = event.pos
                elif event.button == 2:  # middle button
                    duck.position.center = event.pos
                elif event.button == 3:  # right button
                    slime.position.center = event.pos

        # *** Clear the screen ***
        if draw_background:
            for x in range(0, SCREEN_WIDTH, background_img.get_width()):
                for y in range(0, SCREEN_HEIGHT, background_img.get_height()):
                    screen.blit(background_img, (x, y))
        else:
            screen.fill('black')

        # *** Draw game objects ***
        screen.blit(virtual_guy.image, virtual_guy.position)
        screen.blit(duck.image, duck.position)
        screen.blit(slime.get_image(ticks), slime.position)

        # *** Display this completed frame to the user ***
        pygame.display.flip()
        clock.tick(60)  # limit of frames per second


# *** Call the main() function to play the game ***
if __name__ == '__main__':
    main()
