from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random
import pygame


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position,
                           self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20, 50)
            m1 = self.velocity.rotate(random_angle)
            m2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            nf_asteroid = Asteroid(
                self.position.x, self.position.y, new_radius)
            ns_asteroid = Asteroid(
                self.position.x, self.position.y, new_radius)
            nf_asteroid.velocity = m1 * 1.2
            ns_asteroid.velocity = m2 * 1.2
