import os
import cv2
import numpy as np
from collections import deque

GRID_SIZE = 40
CELL_PIXELS = 20
MOD = 10 ** 9 + 7


def image_to_grid(image_path, threshold_val=127, path_ratio=0.5):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    blurred = cv2.medianBlur(img, 3)

    _, threshed = cv2.threshold(blurred, threshold_val, 255, cv2.THRESH_BINARY)

    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    total_pixels = CELL_PIXELS * CELL_PIXELS

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            y_start, y_end = r * CELL_PIXELS, (r + 1) * CELL_PIXELS
            x_start, x_end = c * CELL_PIXELS, (c + 1) * CELL_PIXELS

            cell_pixels = threshed[y_start:y_end, x_start:x_end]
            white_count = np.sum(cell_pixels == 255)

            if white_count > (total_pixels * path_ratio):
                grid[r][c] = 0  # Path
            else:
                grid[r][c] = 1  # Wall

    return grid


def bfs_shortest_path(grid):

    if grid[0][0] == 1 or grid[GRID_SIZE - 1][GRID_SIZE - 1] == 1:
        return None

    start = (0, 0)
    target = (GRID_SIZE - 1, GRID_SIZE - 1)

    queue = deque([(0, 0, 1)])
    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c, dist = queue.popleft()

        if (r, c) == target:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))

    return None


def execute_vault_decryption(folder_name):

    if not os.path.exists(folder_name):
        print(f"Error: The directory '{folder_name}' does not exist.")
        print("Please check your PyCharm folder structure and try again.")
        return

    all_files = os.listdir(folder_name)
    image_names = sorted([f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if not image_names:
        print(f"Error: No image files found inside the '{folder_name}' folder.")
        return

    print(f"Found {len(image_names)} images. Starting decryption sequence...")
    print("-" * 50)

    total_product = 1
    solvable_mazes = 0
    trap_mazes = 0

    for idx, img_name in enumerate(image_names, 1):
        img_path = os.path.join(folder_name, img_name)

        grid = image_to_grid(img_path)

        if grid is None:
            print(f"[{idx}/100] {img_name}: Failed to read image file.")
            continue

        path_length = bfs_shortest_path(grid)

        if path_length is not None:
            solvable_mazes += 1
            total_product = (total_product * path_length) % MOD
            print(f"[{idx}/100] {img_name}: Solvable! Length = {path_length} cells.")
        else:
            trap_mazes += 1
            print(f"[{idx}/100] {img_name}: **TRAP MAZE DETECTED** (Ignored).")

    print("=" * 50)
    print("DECRYPTION COMPLETE")
    print(f"Solvable Mazes Processed: {solvable_mazes}")
    print(f"Trap Mazes Ignored: {trap_mazes}")
    print(f"FINAL NUMERICAL PASSWORD (Modulo 10^9 + 7): {total_product}")
    print("=" * 50)


if __name__ == "__main__":

    TARGET_FOLDER = "maze_images"
    execute_vault_decryption(TARGET_FOLDER)