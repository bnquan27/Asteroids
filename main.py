import pygame
import sys
import time
from asteroid import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    score = 0
    font = pygame.font.SysFont(None, 50)

    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    me = Player(x, y)
    field = AsteroidField()
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for obj in asteroids:
            if obj.collides_with(me):
                log_event("player_hit")
                if me.lives > 0:
                    me.respawn()
                else:
                    end_display = font.render("YOU DIE", True, "White")
                    screen.blit(end_display, (x, y))
                    pygame.display.update()
                    time.sleep(5)
                    print("Game over!")
                    sys.exit()
        for each_asteroid in asteroids:
            for each_shot in shots:
                if each_shot.collides_with(each_asteroid):
                    log_event("asteroid_shot")
                    each_shot.kill()
                    each_asteroid.split()
                    score += 10
        for obj in drawable:
            obj.draw(screen)

        score_display = font.render(f"Score : {score}", True, "White")
        screen.blit(score_display, (10, 10))

        pygame.display.flip()
        pygame.display.update()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
