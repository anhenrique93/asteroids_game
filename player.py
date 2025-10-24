import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, color="white", points=self.triangle(), width=2)

    def __rotate(self, dt):
        self.rotation -= PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer -= dt

        if keys[pygame.K_a]:
            rev_dt = dt * -1
            self.__rotate(rev_dt)
              
        if keys[pygame.K_d]:
            self.__rotate(dt)

        if keys[pygame.K_w] or keys[pygame.K_s]:
            self.__move(dt)
        
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.__shot()
    
    def __move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def __shot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        vel = pygame.Vector2(0, 1)
        dir = vel.rotate(self.rotation)
        shot.velocity += dir * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN