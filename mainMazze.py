import pygame
import sys
from collections import deque
import time
import math

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 400, 400
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
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
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
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Validasi ukuran maze
assert len(maze) == ROWS, f"Jumlah baris maze ({len(maze)}) tidak sesuai dengan ROWS ({ROWS})"
assert all(len(row) == COLS for row in maze), f"Jumlah kolom maze tidak konsisten atau tidak sesuai dengan COLS ({COLS})"

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
            bx, by = x + dx, y + dy
            if 0 <= bx < ROWS and 0 <= by < COLS and maze[bx][by] == 0 and (bx, by) not in visited:
                visited.add((bx, by))
                queue.appendleft((bx, by, path + [(x, y)]))
    
    return []  # Jika tidak ditemukan jalur

# Fungsi DFS untuk Patroli 
def dfs(maze, start, end):
    stack = [(start[0], start[1], [])]
    visited = set()
    
    while stack:
        x, y, path = stack.pop()
        if (x, y) == (end[0], end[1]):
            return path + [(x, y)]
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                ndx, ndy = x + dx, y + dy
                #print(f"nx: {ndx}, ny: {ndy}, maze shape: {len(maze)}x{len(maze[0])}")
                if 0 <= ndx < len(maze) and 0 <= ndy < len(maze[0]) and maze[ndx][ndy] == 0:
                    stack.append((ndx, ndy, path + [(x, y)]))
    return []

def is_visible(maze, enemy_pos, player_pos):
    # Cek apakah player terlihat oleh musuh (tanpa halangan dinding)
    x1, y1 = enemy_pos
    x2, y2 = player_pos
    
    # Bresenham's line algorithm untuk mengecek LOS
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            if maze[x][y] == 1:  # Terhalang dinding
                return False
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            if maze[x][y] == 1:  # Terhalang dinding
                return False
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    
    return True

def hybrid_ai(maze, enemy_pos, player_pos, vision_range=5):
    # AI Hybrid: DFS saat jauh, BFS saat dekat/lihat player
    distance = math.sqrt((enemy_pos[0] - player_pos[0])**2 + (enemy_pos[1] - player_pos[1])**2)
    
    # Jika player dalam jangkauan penglihatan dan terlihat
    if distance < vision_range and is_visible(maze, enemy_pos, player_pos):
        path = bfs(maze, enemy_pos, player_pos)  # Mode agresif (BFS)
    else:
        path = dfs(maze, enemy_pos, player_pos)  # Mode patroli (DFS)
    
    if path and len(path) > 1:
        return path[1]  # Langkah berikutnya
    else:
        return enemy_pos  # Diam jika tidak ada jalan

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
    
    # Gerakan musuh setiap 0.5 detik
    if current_time - last_enemy_move > 0.5:
        enemy_path = hybrid_ai(maze, (enemy_pos[0], enemy_pos[1]), (player_pos[0], player_pos[1]))
        if enemy_path:
            enemy_pos = enemy_path
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