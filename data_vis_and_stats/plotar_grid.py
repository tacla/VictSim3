## Plot grid with walls, obstacles and victims' positions.
## Author: Cesar Tacla, 01 July 2025
##
## Read the obstacles file and the victims' coordinates file and plot the 2D
## grid. Victims are plotted sequentially and represented by their sequential
## numbers starting from zero, according to the order in the env_victims.txt 
## file. You can click on any cell to print its (x, y) coordinates in the 
## console.
##
## The 2D grid's origin is at the top left corner. Indexation is (column, row).
##
## This program prints the metrics per quadrant (victims and walls per quadrant)
##    upper left | upper right
##    -----------+------------
##    lower left | lower right
##
## To run this program you have to:
## - set the variables in the main method. Default values below:
##    data_folder = "./datasets/20x20_42v"
##    env_config = "env_config.txt"
##    env_obst = "env_obst.txt"                                            
##    env_victims = "env_victims.txt" 

import pygame
import math
import csv
from pathlib import Path

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def load_env_config(env_config):
    config = {}
    with open(env_config, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split(maxsplit=1)
            config[key] = value

    R = int(config["GRID_HEIGHT"])
    C = int(config["GRID_WIDTH"])

    base_x, base_y = config["BASE"].split(",")
    base_c = int(base_x)
    base_r = int(base_y)

    W = int(config["WINDOW_WIDTH"])
    H = int(config["WINDOW_HEIGHT"])

    return R, C, base_c, base_r, W, H


def plot_env(env_config, env_obst, env_victims):

    # --- LOAD CONFIG ---
    R, C, base_c, base_r, WIDTH, HEIGHT = load_env_config(env_config)

    CELLW = WIDTH / C
    CELLH = HEIGHT / R
    base_coords = (base_c, base_r)

    # --- COLORS ---
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YEL = (255, 255, 0)
    CYAN = (0, 255, 255)
    OBST_COLOR = (200, 255, 255)

    # --- COUNTERS ---
    victs_quad = [0] * 4
    walls_quad = [0] * 4

    # --- PYGAME INIT ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Grid')
    screen.fill(WHITE)

    # --- DRAW GRID ---
    for r in range(R):
        for c in range(C):
            pygame.draw.rect(screen, (230, 230, 230),
                             (c * CELLW, r * CELLH, CELLW, CELLH), 1)

    print("\n----------------------------------------")
    print(f"Total of rows......: {R}")
    print(f"Total of cols......: {C}")
    print(f"Total of cells.....: {R*C}")
    print(f"Base position......: {base_coords}")

    # --- LOAD WALLS ---
    wall_coords = []
    with open(env_obst, 'r') as f:
        for line in f:
            col1, col2, col3 = line.strip().split(',')
            col1, col2, col3 = int(col1), int(col2), float(col3)

            if col3 == 100.0:
                wall_coords.append((col1, col2, BLACK))
            elif col3 > 0:
                obst_color = tuple(min(int(x / col3), 240) for x in OBST_COLOR)
                wall_coords.append((col1, col2, obst_color))

    tot_walls = len(wall_coords)

    # --- LOAD VICTIMS ---
    vict_coords = []
    with open(env_victims, 'r') as csvfile:
        for row in csv.reader(csvfile):
            x = int(row[0])
            y = int(row[1])
            if (x < C/2):
                if (y < R/2):
                    victs_quad[0] += 1
                else:
                    victs_quad[2] += 1
            else:
                if (y < R/2):
                   victs_quad[1] += 1
                else:
                   victs_quad[3] += 1
                    
            vict_coords.append((x,y))

    tot_vics = len(vict_coords)

    # --- DRAW BASE ---
    pygame.draw.rect(screen, CYAN,
                     (base_c * CELLW, base_r * CELLH, CELLW, CELLH))

    # --- DRAW WALLS ---
    for c, r, color in wall_coords:
        pygame.draw.rect(screen, color,
                         (c * CELLW, r * CELLH, CELLW, CELLH))

        if r < R / 2:
            walls_quad[0 if c < C / 2 else 1] += 1
        else:
            walls_quad[2 if c < C / 2 else 3] += 1

    print("\n----------------------------------------")
    print(f"Total of obstacles.....: {tot_walls} ({100*tot_walls/(R*C):.1f}%)")
    print(f"  upper left  quad.: {walls_quad[0]}")
    print(f"  upper right quad.: {walls_quad[1]}")
    print(f"  lower left  quad.: {walls_quad[2]}")
    print(f"  lower right quad.: {walls_quad[3]}")

  

    print("\n------------------------------------------")
    print(f"Total of victims...: {tot_vics}")
    print(f"  upper left  quad.: {victs_quad[0]}")
    print(f"  upper right quad.: {victs_quad[1]}")
    print(f"  lower left  quad.: {victs_quad[2]}")
    print(f"  lower right quad.: {victs_quad[3]}")

    pygame.display.update()

    # --- PREPARE FONT ---
    font = pygame.font.SysFont('Arial', int(0.4 * min(CELLW, CELLH)))

    # --- MAIN LOOP (RENDERIZAÇÃO COMPLETA A CADA FRAME) ---
    running = True
    while running:
    
        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                r = int(y / CELLH)
                c = int(x / CELLW)
                print(f'({c},{r})')
    
        # --- REDESENHA TUDO ---
        screen.fill(WHITE)
    
        # GRID
        for r in range(R):
            for c in range(C):
                pygame.draw.rect(screen, (230, 230, 230),
                                 (c * CELLW, r * CELLH, CELLW, CELLH), 1)
    
        # BASE
        pygame.draw.rect(screen, CYAN,
                         (base_c * CELLW, base_r * CELLH, CELLW, CELLH))
    
        # WALLS
        for c, r, color in wall_coords:
            pygame.draw.rect(screen, color,
                             (c * CELLW, r * CELLH, CELLW, CELLH))
    
        # --- VICTIMS (NUMERADAS) ---
        for i, (c, r) in enumerate(vict_coords, start=0):
    
            text = font.render(str(i), True, RED)
            text_rect = text.get_rect(
                center=(c * CELLW + CELLW / 2, r * CELLH + CELLH / 2)
            )
            screen.blit(text, text_rect)
    
        # --- UPDATE ---
        pygame.display.flip()
        
    pygame.quit()
    return


def main():
    data_folder = Path('./datasets/env/94x94_408v')
    env_config = data_folder / "env_config.txt"
    env_obst = data_folder / "env_obst.txt"
    env_victims = data_folder / "env_victims.txt"
    plot_env(env_config, env_obst, env_victims)


if __name__ == "__main__":
    main()