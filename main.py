import pygame
import noise
import numpy as np
import random
import math
# Importer les fonctions du personnage
import character

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre et s'assurer qu'elles sont divisibles par le nombre de colonnes
COLS = 100
TILE_SIZE = 10  # Taille de chaque tuile
WIDTH = COLS * TILE_SIZE
HEIGHT = WIDTH // 16 * 9  # Maintenir un ratio 16:9 pour la hauteur
ROWS = HEIGHT // TILE_SIZE

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map")

# Définir les couleurs
WHITE = (255, 255, 255)  # Couleur de fond
GREEN = (34, 139, 34)  # Terre
BROWN = (238, 214, 175)  # Plage
BLUE = (0, 0, 255)  # Eau
DARK_BLUE = (0, 0, 139)  # Océan
DARK_GREEN = (0, 100, 0)  # Forêt dense
GRAY = (169, 169, 169)  # Montagnes
RED = (255, 0, 0)  # Ville 

# Définir les dimensions de la grille
ROWS, COLS = 300,300
TILE_SIZE = WIDTH // COLS

# Fonction pour générer une carte de bruit de Perlin
def generate_perlin_noise_map(rows, cols, scale=10, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    if seed is None:
        seed = random.randint(0, 100)
    noise_map = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            nx = j / cols * scale
            ny = i / rows * scale
            noise_map[i][j] = noise.pnoise2(nx, ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=cols, repeaty=rows, base=seed)
    return noise_map

# Fonction pour classifier les différents types de terrain
def classify_terrain(noise_map, ocean_level=-0.2, water_level=0.0, beach_level=0.1, forest_level=0.3, mountain_level=0.6):
    rows, cols = noise_map.shape
    terrain_map = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if noise_map[i][j] < ocean_level:
                terrain_map[i][j] = 3  # Océan
            elif noise_map[i][j] < water_level:
                terrain_map[i][j] = 2  # Eau
            elif noise_map[i][j] < beach_level:
                terrain_map[i][j] = 1  # Plage
            elif noise_map[i][j] < forest_level:
                terrain_map[i][j] = 0  # Terre
            elif noise_map[i][j] < mountain_level:
                terrain_map[i][j] = 5  # Forêt dense
            else:
                terrain_map[i][j] = 4  # Montagne
    return terrain_map

# Fonction pour dessiner la carte
def draw_map(win, terrain_map, city_locations):
    for i in range(ROWS):
        for j in range(COLS):
            if (i, j) in city_locations:
                # Dessiner la case de la ville avec une bordure rouge
                pygame.draw.circle(win, RED, (j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 + 5)
            else:
                terrain_type = terrain_map[i][j]
                if terrain_type == 0:
                    color = GREEN  # Terre
                elif terrain_type == 1:
                    color = BROWN  # Plage
                elif terrain_type == 2:
                    color = BLUE  # Eau
                elif terrain_type == 3:
                    color = DARK_BLUE  # Océan
                elif terrain_type == 4:
                    color = DARK_GREEN  # Forêt dense
                elif terrain_type == 5:
                    color = GRAY  # Montagne
                else:
                    continue
                
                pygame.draw.rect(win, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))


# Fonction pour générer des emplacements de villes
def generate_city_locations(terrain_map):
    city_locations = []
    cities_generated = 0
    
    for i in range(1, ROWS - 1):
        for j in range(1, COLS - 1):
            if terrain_map[i][j] == 0 and all(terrain_map[i+x][j+y] == 0 for x in range(-1,2) for y in range(-1,2)):
                if cities_generated >= 20:
                    return city_locations
                
                # Check distance with existing city locations
                valid_location = True
                for city in city_locations:
                    distance = math.sqrt((i - city[0])**2 + (j - city[1])**2)
                    if distance < 100:
                        valid_location = False
                        break
                
                if valid_location:
                    city_locations.append((i, j))
                    cities_generated += 1
    
    return city_locations

# Fonction principale
def main():
    clock = pygame.time.Clock()
    run = True

    # Génération de la carte et des emplacements des villes
    noise_map = generate_perlin_noise_map(ROWS, COLS, scale=5, octaves=6, persistence=0.5, lacunarity=2.0)
    terrain_map = classify_terrain(noise_map)
    city_locations = generate_city_locations(terrain_map)

    # Position initiale du personnage
    character_pos = (ROWS // 2, COLS // 2)

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Mise à jour de la position du personnage en fonction des touches pressées
        keys_pressed = pygame.key.get_pressed()
        character_pos = character.update_character(keys_pressed, character_pos, terrain_map, TILE_SIZE)

        # Dessin de la carte et du personnage
        WIN.fill(WHITE)
        draw_map(WIN, terrain_map, city_locations)
        character.draw_character(WIN, character_pos, TILE_SIZE)
        pygame.display.update()

    pygame.quit()

# Exécution de la fonction principale si ce fichier est exécuté directement
if __name__ == "__main__":
    main()

