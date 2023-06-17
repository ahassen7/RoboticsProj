import pygame
import random
import networkx as nx

# Constants
WIDTH = 800  # Width of the grid
HEIGHT = 600  # Height of the grid
GRID_SIZE = 20  # Size of each grid cell
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Rover:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


def generate_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randint(0, NUM_COLS - 1)
        y = random.randint(0, NUM_ROWS - 1)
        obstacles.append(Obstacle(x, y))
    return obstacles


def is_collision(rover, obstacles):
    for obstacle in obstacles:
        if rover.x == obstacle.x and rover.y == obstacle.y:
            return True
    return False


def main():
    rover = Rover(0, 0)
    obstacles = generate_obstacles(100)  # Increase the number of obstacles here

    # Create the grid graph using networkx
    graph = nx.grid_2d_graph(NUM_COLS, NUM_ROWS)

    # Remove nodes corresponding to obstacles
    for obstacle in obstacles:
        node = (obstacle.x, obstacle.y)
        if graph.has_node(node):
            graph.remove_node(node)

    # Run A* algorithm to find the path to the goal
    start = (rover.x, rover.y)
    goal = (NUM_COLS - 1, NUM_ROWS - 1)
    path = nx.astar_path(graph, start, goal)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if len(path) > 1:
            next_node = path[1]
            dx = next_node[0] - rover.x
            dy = next_node[1] - rover.y
            if not is_collision(Rover(rover.x + dx, rover.y + dy), obstacles):
                rover.move(dx, dy)
                path.pop(0)  # Move to the next node in the path

        screen.fill(WHITE)
        draw_grid()
        for obstacle in obstacles:
            obstacle.draw()
        for node_x, node_y in path:
            pygame.draw.rect(screen, GREEN, (node_x * GRID_SIZE, node_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        rover.draw()
        pygame.display.flip()
        clock.tick(2)  # Adjust the speed of the movement here


if __name__ == '__main__':
    main()

