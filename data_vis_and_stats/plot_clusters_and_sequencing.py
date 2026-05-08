# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 23:26:08 2026

@author: cesar

Plota os clusters e o sequenciamento do socorro às vítimas. As vítimas de um
mesmo clusters são identificadas por um quadrado de mesma cor. O caminho é
plotado por linhas entre as vítimas.

CONFIGURAÇÕES
1) PATHS para os arquivos de configuração, map e clusters.
- path_maps: arquivo resultante da exploração do ambiente
- clusters: arquivos resultantes do agrupamento das vítimas. Também,
          a ordem pode representar o sequenciamento do socorro. Para clusters
          basta configurar a pasta. Todos os arquivos da pasta que iniciam
          por cluster são considerados.
          
2) PLOTAR_SEQUENCIAMENTO
  - True: plota a ordem de socorro às vítimas de acordo com a ordem em que elas
          aparecem nos arquivos dos clusters
  - False: não plota
"""

import pygame
import csv
import os
import numpy as np

# =========================
# CONFIGURAÇÕES DE PATH
# =========================
path_config = "./datasets/env/20x20_42v"
path_vict   = "./datasets/vict/42v"
path_maps   = "./map"
path_clusters = "./clusters"

PLOTAR_SEQUENCIAMENTO = True

# =========================
# CORES
# =========================
WHITE = (255,255,255)
BLACK = (0,0,0)
DARK_GRAY = (80,80,80)
CYAN = (0,255,255)

GREEN = (0,200,0)
YELLOW = (255,255,0)
RED = (255,0,0)

# cores vivas para clusters
CLUSTER_COLORS = [
    (255,0,255),(0,255,255),(255,128,0),
    (128,0,255),(0,255,128),(255,0,128),
    (0,128,255),(128,255,0)
]

# =========================
# LEITURA CONFIG
# =========================
import re

def parse_base(line):
    match = re.search(r'BASE\s+(\d+)\s*,\s*(\d+)', line)
    if not match:
        raise ValueError(f"env_config.txt: BASE inválida: {line}")
    x = int(match.group(1))
    y = int(match.group(2))
    return (x, y)

def read_config():

    config = {}
    with open(os.path.join(path_config,"env_config.txt")) as f:
        for line in f:
            if "BASE" in line:
                config["BASE"] = parse_base(line)
            else:
                k,v = line.split()
                if "DELAY" in line:
                    config[k]=float(v)
                else:                
                    config[k] = int(v)
    return config

# =========================
# LEITURA DATA (GROUND TRUTH)
# =========================
def read_data():
    data = {}
    with open(os.path.join(path_vict,"data.csv")) as f:
        reader = csv.DictReader(f)
        for i,row in enumerate(reader):
            data[i] = {
                "tri": int(row["tri"]),
                "sobr": float(row["sobr"])
            }
    return data

# =========================
# LEITURA MAP
# =========================
def read_map(config):
    BASE = config["BASE"]
    cells = {}

    with open(os.path.join(path_maps,"map.csv")) as f:
        reader = csv.reader(f)
        header_map = next(reader)
        for row in reader:
            x_rel = int(row[0])
            y_rel = int(row[1])
            obst  = float(row[2])
            vid   = int(row[3])

            x = BASE[0] + x_rel
            y = BASE[1] + y_rel

            cell = {
                "obst": obst,
                "id": vid,
                "vitals": None
            }

            if vid != -1:
                cell["vitals"] = {
                    "tri": int(row[-2]),
                    "sobr": float(row[-1]),
                    "all": row[4:]
                }

            cells[(x,y)] = cell

    return cells

# =========================
# LEITURA CLUSTERS
# =========================
def read_clusters():
    clusters = []
    files = sorted(os.listdir(path_clusters))

    for file in files:
        if file.startswith("cluster"):
            ids = []
            with open(os.path.join(path_clusters,file)) as f:
                reader = csv.reader(f)
                for row in reader:

                    try:
                        id_temp = int(row[0])
                        ids.append(int(id_temp))
                    except (ValueError, TypeError, IndexError):
                        print(f"Id de vítima errado: {row} no {file}")

            clusters.append(ids)

    return clusters

# =========================
# MÉTRICAS
# =========================
def compute_metrics(cells, data_gt):
    y_true = []
    y_pred = []
    sobr_true = []
    sobr_pred = []

    for cell in cells.values():
        if cell["id"] != -1:
            vid = cell["id"]

            y_true.append(data_gt[vid]["tri"])
            y_pred.append(cell["vitals"]["tri"])

            sobr_true.append(data_gt[vid]["sobr"])
            sobr_pred.append(cell["vitals"]["sobr"])

    # matriz de confusão 4x4
    conf = np.zeros((4,4), dtype=int)
    for t,p in zip(y_true,y_pred):
        conf[t][p] += 1

    acc = np.mean(np.array(y_true) == np.array(y_pred))
    mse = np.mean((np.array(sobr_true) - np.array(sobr_pred))**2)

    print("\n=== MATRIZ DE CONFUSÃO (tri) ===")
    print(conf)
    print()
    print(f"\nAcurácia: {acc:.3f}")
    print()
    print(f"\nMSE (sobr): {mse:.3f}")

# =========================
# COR DO TERRENO
# =========================
def get_color(obst):
    if obst == 1.0:
        color = (255, 255, 255)
    elif obst == 100.0:
        color = (0, 0, 0) ## black
    else:
        gray = int(255 - (obst / 6) * 255)
        color = (200, gray, gray)
        
    return color

# =========================
# MAIN PYGAME
# =========================
def run():
    config = read_config()
    data_gt = read_data()
    cells = read_map(config)
    clusters = read_clusters()

    compute_metrics(cells, data_gt)

    pygame.init()
    screen = pygame.display.set_mode(
        (config["WINDOW_WIDTH"], config["WINDOW_HEIGHT"])
    )

    clock = pygame.time.Clock()

    cell_w = config["WINDOW_WIDTH"] // config["GRID_WIDTH"]
    cell_h = config["WINDOW_HEIGHT"] // config["GRID_HEIGHT"]

    # mapear id -> posição
    id_to_pos = {}
    for pos,cell in cells.items():
        if cell["id"] != -1:
            id_to_pos[cell["id"]] = pos

    running = True
    while running:
        screen.fill(WHITE)

        # =========================
        # DESENHAR GRID
        # =========================
        for x in range(config["GRID_WIDTH"]):
            for y in range(config["GRID_HEIGHT"]):
        
                rect = pygame.Rect(x*cell_w, y*cell_h, cell_w, cell_h)
        
                if (x,y) in cells:
                    cell = cells[(x,y)]
        
                    pygame.draw.rect(screen, get_color(cell["obst"]), rect)
        
                    # vítima
                    if cell["id"] != -1:
                        tri = cell["vitals"]["tri"]
                        color = [GREEN,YELLOW,RED,BLACK][tri]
        
                        cx = x*cell_w + cell_w//2
                        cy = y*cell_h + cell_h//2
        
                        pygame.draw.circle(screen, color, (cx,cy), min(cell_w,cell_h)//3)
        
                        # erro de tri
                        if tri != data_gt[cell["id"]]["tri"]:
                            font = pygame.font.SysFont(None, 18)
                            text = font.render("X", True, WHITE)
                            screen.blit(text, (cx-5, cy-8))
        
                else:
                    # CÉLULA NÃO EXPLORADA
                    pygame.draw.rect(screen, (220,220,220), rect)
        
                    font = pygame.font.SysFont(None, 18)
                    text = font.render("?", True, BLACK)
        
                    cx = x*cell_w + cell_w//2 - 5
                    cy = y*cell_h + cell_h//2 - 8
        
                    screen.blit(text, (cx,cy))
        
                # grid sempre por cima
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)
        
                # BASE (por último para garantir visibilidade)
                if (x,y) == config["BASE"]:
                    pygame.draw.rect(screen, CYAN, rect)

        # =========================
        # DESENHAR CLUSTERS
        # =========================
        font = pygame.font.SysFont(None, 18)

        for i,cluster in enumerate(clusters):
            color = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]

            pts = []
            for vid in cluster:
                if vid in id_to_pos:
                    x,y = id_to_pos[vid]
                    pts.append((x,y))

                    rect = pygame.Rect(x*cell_w, y*cell_h, cell_w, cell_h)
                    pygame.draw.rect(screen, color, rect, 3)

            if PLOTAR_SEQUENCIAMENTO:
                for j in range(len(pts)-1):
                    x1,y1 = pts[j]
                    x2,y2 = pts[j+1]

                    p1 = (x1*cell_w + cell_w*0.05, y1*cell_h + cell_h*0.1)
                    p2 = (x2*cell_w + cell_w*0.05, y2*cell_h + cell_h*0.1)

                    pygame.draw.line(screen, color, p1, p2, 2)

                    label = font.render(str(j+1), True, color)
                    screen.blit(label, p1)

        # =========================
        # EVENTOS
        # =========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                x = mx // cell_w
                y = my // cell_h

                if (x,y) in cells:
                    cell = cells[(x,y)]
                    print("\n=== CLICK ===")
                    print("Coord\t:", (x,y))
                    print("Obst\t:", cell["obst"])

                    if cell["id"] != -1:
                        vid = cell["id"]
                        print("ID\t:", vid)
                        print("Sinais vitais:", cell["vitals"]["all"])
                        print("TRI (map)\t:", cell["vitals"]["tri"])
                        print("SOBR (map)\t:", cell["vitals"]["sobr"])
                        print("TRI (GT)\t:", data_gt[vid]["tri"])
                        print("SOBR (GT)\t:", data_gt[vid]["sobr"])

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    run()