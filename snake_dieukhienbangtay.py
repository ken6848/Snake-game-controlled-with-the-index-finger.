import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import math
import pygame
import random

WIDTH, HEIGHT = 600, 600
TILE = 20
GRID_W, GRID_H = WIDTH // TILE, HEIGHT // TILE
BACKGROUND = (18, 18, 18)
SNAKE_COLOR = (40, 200, 40)
HEAD_COLOR = (60, 230, 60)
APPLE_COLOR = (220, 60, 60)
GRID_COLOR = (35, 35, 35)
TEXT_COLOR = (230, 230, 230)
SPEED_MS = 120

DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def out_of_bounds(p) -> bool:
    return not (0 <= p[0] < GRID_W and 0 <= p[1] < GRID_H)

def spawn_apple(occupied):
    free = [(x, y) for x in range(GRID_W) for y in range(GRID_H) if (x, y) not in occupied]
    return random.choice(free) if free else (-1, -1)

def draw_grid(surf: pygame.Surface):
    for x in range(0, WIDTH, TILE):
        pygame.draw.line(surf, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(surf, GRID_COLOR, (0, y), (WIDTH, y), 1)

def draw_rect(surf: pygame.Surface, color, cell, pad: int = 2):
    x, y = cell
    pygame.draw.rect(
        surf, color,
        pygame.Rect(x * TILE + pad, y * TILE + pad, TILE - 2 * pad, TILE - 2 * pad),
        border_radius=4
    )

def down(lm):
    gest = None
    if abs(lm[4].y - lm[3].y) < 0.04:
        if lm[4].x > lm[3].x:
            gest = "RIGHT"
        elif lm[3].x > lm[4].x:
            gest = "LEFT"
    elif lm[4].y < lm[3].y:
        gest = "UP"
    elif lm[4].y > lm[3].y:
        gest = "DOWN"
    return gest

def main():
    pygame.init()
    pygame.display.set_caption("SNAKE")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    def reset():
        mid = (2, 29)
        snake = [mid, (mid[0] - 1, mid[1]), (mid[0] - 2, mid[1])]
        direction = (+1, 0)
        apple = spawn_apple(set(snake))
        score = 0
        return snake, direction, apple, score, False

    snake, direction, apple, score, game_over = reset()
    last_step = pygame.time.get_ticks()
    pending_dir = direction

    cap = cv2.VideoCapture(0)
    base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        running_mode=vision.RunningMode.VIDEO
    )
    detector = vision.HandLandmarker.create_from_options(options)
    
    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
        (0, 17),
    ]

    running = True
    while running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp = int(time.time() * 1000)
        result = detector.detect_for_video(mp_image, timestamp)

        if result.hand_landmarks:
            h, w, _ = frame.shape
            lm = result.hand_landmarks[0]

            for ind, landmark in enumerate(lm):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                cv2.putText(frame, str(ind), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (5, 113, 255))

            for start, end in HAND_CONNECTIONS:
                x1, y1 = int(lm[start].x * w), int(lm[start].y * h)
                x2, y2 = int(lm[end].x * w), int(lm[end].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            gesture = down(lm)
            if gesture:
                cv2.putText(frame, gesture, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                nx, ny = DIRS[gesture]
                if (nx, ny) != (-direction[0], -direction[1]):
                    pending_dir = (nx, ny)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                    snake, direction, apple, score, game_over = reset()
                    last_step = pygame.time.get_ticks()
                    pending_dir = direction

        now = pygame.time.get_ticks()
        if not game_over and now - last_step >= SPEED_MS:
            last_step = now
            direction = pending_dir
            head = add(snake[0], direction)

            if out_of_bounds(head) or head in snake:
                game_over = True
            else:
                snake.insert(0, head)
                if head == apple:
                    score += 1
                    apple = spawn_apple(set(snake))
                else:
                    snake.pop()

        cv2.imshow("Camera", frame)
        cv2.waitKey(1)
        
        screen.fill(BACKGROUND)
        draw_grid(screen)

        if apple != (-1, -1):
            draw_rect(screen, APPLE_COLOR, apple, pad=3)

        for i, cell in enumerate(snake):
            draw_rect(screen, HEAD_COLOR if i == 0 else SNAKE_COLOR, cell, pad=2)

        score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surf, (10, 8))

        if game_over:
            big = pygame.font.SysFont("consolas", 48)
            go = big.render("GAME OVER", True, TEXT_COLOR)
            hint = font.render("Press R / Enter to restart — Esc to quit", True, TEXT_COLOR)
            rect = go.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
            rect2 = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 28))
            screen.blit(go, rect)
            screen.blit(hint, rect2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()