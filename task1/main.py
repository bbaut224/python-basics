"""
pygame_oop_template.py — Учебный шаблон для Pygame + ООП

Содержит TODO-задания с максимально прямыми инструкциями:
- Вставить список
- Добавить параметр
- Создать переменную
- Добавить класс-наследник
и т.п.

Сохраните как pygame_oop_template.py
Запуск: python pygame_oop_template.py
"""

import pygame
import sys
import random
import math
from typing import List, Tuple

# ---------- Конфигурация ----------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# ---------- Базовый объект ----------
class GameObject:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(int(x), int(y), width, height)

    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)

    def update(self, dt: float):
        self.update_rect()


# ---------- Игрок ----------
class Player(GameObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 40, 50)
        self.color = (50, 120, 230)
        self.speed = 300.0
        self.shoot_cooldown = 0.25
        self._shoot_timer = 0.0
        self.lives = 3
        self.invincible_timer = 0.0

        # TODO Задание 1:
        # Создайте атрибуты для анимации:
        # self.frames = []
        # self.current_frame = 0
        # self.frame_timer = 0.0
        #
        # После этого загрузите изображение из файла (sprite.png) и разрежьте его на кадры 40x50.
        # Пример: sheet = pygame.image.load("player.png").convert_alpha()
        # (Файла нет — студент должен добавить)
        #
        # Подсказка: используйте subsurface или Surface.blit.

    def handle_input(self, pressed_keys, dt):
        dx = dy = 0
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            dx -= 1
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            dx += 1
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            dy -= 1
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            dy += 1

        # Нормализация
        if dx != 0 and dy != 0:
            diag = 0.7071
        else:
            diag = 1.0

        # TODO Задание 2:
        # Сделать ускорение: если Shift нажат —
        # speed = self.speed * 1.5
        # Иначе speed = self.speed
        speed = self.speed
        if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]:
            speed *= 1.5

        self.x += dx * speed * diag * dt
        self.y += dy * speed * diag * dt

        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

        self.update_rect()

    def can_shoot(self):
        return self._shoot_timer <= 0.0

    def shoot(self):
        self._shoot_timer = self.shoot_cooldown
        bx = self.x + self.width / 2 - 5
        by = self.y - 10
        return Bullet(bx, by, 0, -600)

    def hit(self):
        if self.invincible_timer > 0:
            return
        self.lives -= 1
        self.invincible_timer = 1.5

    def update(self, dt):
        if self._shoot_timer > 0:
            self._shoot_timer -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        # TODO Задание 3:
        # Реализовать переключение кадров анимации.
        # Каждые 0.1 секунды (или меньше) менять self.current_frame.
        #
        # self.frame_timer += dt
        # if self.frame_timer >= 0.1:
        #     self.frame_timer = 0.0
        #     self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.update_rect()

    def draw(self, surf):
        # TODO Задание 4:
        # Если кадры загружены — рисовать self.frames[self.current_frame]
        #
        # Если нет — оставить прямоугольник.
        pygame.draw.rect(surf, self.color, self.rect)


# ---------- Враги ----------
class Enemy(GameObject):
    def __init__(self, x, y, behavior="horizontal"):
        super().__init__(x, y, 36, 36)
        self.color = (220, 50, 50)
        self.speed = 120
        self.behavior = behavior
        self.dir = 1
        self.phase = random.uniform(0, math.pi * 2)

    def update(self, dt):
        if self.behavior == "horizontal":
            self.x += self.dir * self.speed * dt
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.dir *= -1

        elif self.behavior == "vertical":
            self.y += self.dir * self.speed * dt
            if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.height:
                self.dir *= -1

        elif self.behavior == "sine":
            # TODO Задание 5:
            # Сделать синусоиду по Y:
            # self.x += self.speed * dt
            # self.y = 100 + math.sin(time) * 40
            time = pygame.time.get_ticks() / 400
            self.x += self.speed * dt
            self.y = 150 + math.sin(time + self.phase) * 80

        self.update_rect()

    def draw(self, s):
        pygame.draw.rect(s, self.color, self.rect)


# ---------- Задание 6 — создать новые классы врагов ----------
# Например ChaserEnemy — идёт к игроку
# Например ZigZagEnemy — меняет направление каждые N секунд
#
# class ChaserEnemy(Enemy):
#     def update(self, dt):
#         # Добавить движение к игроку
#         pass


# ---------- Пуля ----------
class Bullet(GameObject):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, 10, 14)
        self.vx = vx
        self.vy = vy
        self.color = (20, 200, 80)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.update_rect()

    def draw(self, s):
        pygame.draw.rect(s, self.color, self.rect)


# ---------- Столкновения ----------
def check_collision(a, b):
    return a.rect.colliderect(b.rect)


# ---------- Игра ----------
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pygame OOP Template — TODO tasks")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        self.player = Player(SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 1.2

        self.score = 0
        self.state = "MENU"

        # TODO Задание 7:
        # Создать двумерный список волн:
        # waves = [
        #    [("horizontal", 5), ("vertical", 3)],
        #    [("sine", 4), ("horizontal", 4)],
        # ]
        #
        # Каждая волна — список из пар (тип_поведения, количество)
        #
        # Пример:
        # self.waves = [
        #    [("horizontal", 3)],
        #    [("sine", 2), ("vertical", 2)],
        #    [("random", 5)],
        # ]
        #
        # Также создайте переменную self.current_wave = 0

        self.waves = [
            [("horizontal", 3)],
            [("sine", 2), ("vertical", 1)],
            [("horizontal", 4), ("vertical", 4)],
        ]
        self.current_wave = 0

    def reset(self):
        self.player = Player(SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemies = []
        self.spawn_timer = 0
        self.score = 0
        self.current_wave = 0
        self.state = "PLAY"

    def spawn_wave(self):
        """Спавн текущей волны."""
        if self.current_wave >= len(self.waves):
            return

        for behavior, count in self.waves[self.current_wave]:
            for _ in range(count):
                x = random.randint(20, SCREEN_WIDTH - 50)
                y = random.randint(20, SCREEN_HEIGHT // 3)
                self.enemies.append(Enemy(x, y, behavior))

        self.current_wave += 1

    def handle_events(self, dt):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if self.state == "MENU" and e.key == pygame.K_RETURN:
                    self.reset()

                if self.state == "GAME_OVER" and e.key == pygame.K_r:
                    self.reset()

        if self.state == "PLAY":
            pressed = pygame.key.get_pressed()
            self.player.handle_input(pressed, dt)

            if (pressed[pygame.K_SPACE] or pressed[pygame.K_z]) and self.player.can_shoot():
                self.bullets.append(self.player.shoot())

    def update(self, dt):
        if self.state != "PLAY":
            return

        if not self.enemies:
            self.spawn_wave()

        self.player.update(dt)

        for b in list(self.bullets):
            b.update(dt)
            if b.y < -20:
                self.bullets.remove(b)

        for e in list(self.enemies):
            e.update(dt)

        for b in list(self.bullets):
            for e in list(self.enemies):
                if check_collision(b, e):
                    self.score += 1
                    try: self.bullets.remove(b)
                    except: pass
                    try: self.enemies.remove(e)
                    except: pass
                    break

        for e in list(self.enemies):
            if check_collision(e, self.player):
                self.player.hit()
                self.enemies.remove(e)
                if self.player.lives <= 0:
                    self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill((18, 24, 38))

        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "PLAY":
            self.player.draw(self.screen)
            for b in self.bullets:
                b.draw(self.screen)
            for e in self.enemies:
                e.draw(self.screen)

            self.draw_ui()
        elif self.state == "GAME_OVER":
            self.draw_game_over()

        pygame.display.flip()

    def draw_ui(self):
        score = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives = self.font.render(f"Lives: {self.player.lives}", True, (255, 100, 100))
        self.screen.blit(score, (10, 10))
        self.screen.blit(lives, (10, 35))

    def draw_menu(self):
        t = self.font.render("Pygame OOP Template (Enter to Start)", True, (255, 255, 255))
        self.screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT // 2))

    def draw_game_over(self):
        t = self.font.render("GAME OVER — R to Restart", True, (255, 100, 100))
        s = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(s, (SCREEN_WIDTH // 2 - s.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events(dt)
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    Game().run()
