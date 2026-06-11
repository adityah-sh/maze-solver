# Professor Lachure's Maze Solver

An automated pipeline built in Python to decrypt a digital vault by processing glitched maze images and calculating shortest paths.

## Features
* **Image Preprocessing:** Uses OpenCV for Grayscale conversion, Median Blur noise reduction, and Binary Thresholding.
* **Downsampling:** Converts 800x800 pixel images into a 40x40 logical grid layout.
* **Pathfinding:** Implements Breadth-First Search (BFS) to guarantee finding the absolute shortest path length.
* **Modular Math:** Multiplies path lengths using a Modulo $10^9 + 7$ safeguard to prevent integer overflow.

## How to Run
1. Place the maze images inside a folder named `maze_images/`.
2. Run `python solver.py`.