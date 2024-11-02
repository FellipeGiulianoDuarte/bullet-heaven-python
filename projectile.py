import pygame


class Projectile(pygame.sprite.Sprite):
    SCREEN_SIZE = (1280, 720)

    def __init__(self, x, y, direction_x, direction_y, speed, orientation, lifespan=100):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 255))
        self.image = pygame.transform.rotate(self.image, orientation)
        self.rect = self.image.get_rect(center=(x, y))

        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = speed
        self.lifespan = lifespan

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()
            return

        if (
            self.rect.right < 0
            or self.rect.left > self.SCREEN_SIZE[0]
            or self.rect.bottom < 0
            or self.rect.top > self.SCREEN_SIZE[1]
        ):
            self.kill()
