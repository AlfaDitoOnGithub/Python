import pygame
import sys
from collections import deque
import time

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirin dengan BFS")
clock = pygame.time.Clock()

# Labirin (1 = dinding, 0 = jalan)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Posisi awal player dan musuh
player_pos = [1, 1]
enemy_pos = [ROWS-2, COLS-2]

# Fungsi BFS untuk mencari jalur terpendek
def bfs(maze, start, end):
    queue = deque()
    queue.appendleft((start[0], start[1], []))
    visited = set()
    visited.add((start[0], start[1]))
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Atas, bawah, kiri, kanan
    
    while queue:
        x, y, path = queue.pop()
        
        if (x, y) == (end[0], end[1]):
            return path + [(x, y)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.appendleft((nx, ny, path + [(x, y)]))
    
    return []  # Jika tidak ditemukan jalur

# Fungsi untuk menggambar labirin
def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Fungsi untuk menggambar player dan musuh
def draw_characters():
    pygame.draw.rect(screen, GREEN, (player_pos[1] * GRID_SIZE, player_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (enemy_pos[1] * GRID_SIZE, enemy_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Game loop
running = True
last_enemy_move = 0

while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Kontrol player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_pos[0] > 0 and maze[player_pos[0]-1][player_pos[1]] == 0:
                player_pos[0] -= 1
            if event.key == pygame.K_DOWN and player_pos[0] < ROWS-1 and maze[player_pos[0]+1][player_pos[1]] == 0:
                player_pos[0] += 1
            if event.key == pygame.K_LEFT and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1]-1] == 0:
                player_pos[1] -= 1
            if event.key == pygame.K_RIGHT and player_pos[1] < COLS-1 and maze[player_pos[0]][player_pos[1]+1] == 0:
                player_pos[1] += 1
    
    # Gerakan musuh menggunakan BFS setiap 0.5 detik
    if current_time - last_enemy_move > 0.5:
        path = bfs(maze, (enemy_pos[0], enemy_pos[1]), (player_pos[0], player_pos[1]))
        if len(path) > 1:  # Jika ada jalur
            next_pos = path[1]  # Langkah berikutnya
            enemy_pos[0], enemy_pos[1] = next_pos[0], next_pos[1]
        last_enemy_move = current_time
    
    # Cek jika musuh menangkap player
    if enemy_pos[0] == player_pos[0] and enemy_pos[1] == player_pos[1]:
        print("Game Over! Musuh menangkap Anda!")
        running = False
    
    # Render
    screen.fill(WHITE)
    draw_maze()
    draw_characters()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()