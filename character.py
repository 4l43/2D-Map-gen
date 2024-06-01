import pygame

# Fonction pour dessiner le personnage
def draw_character(win, pos, TILE_SIZE):
    pygame.draw.rect(win, (255, 0, 0), (pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Fonction pour mettre à jour la position du personnage
def update_character(keys_pressed, character_pos, terrain_map, TILE_SIZE):
    if keys_pressed[pygame.K_UP] and character_pos[0] > 0 and terrain_map[character_pos[0] - 1][character_pos[1]] != 4:
        character_pos = (character_pos[0] - 1, character_pos[1])
    if keys_pressed[pygame.K_DOWN] and character_pos[0] < len(terrain_map) - 1 and terrain_map[character_pos[0] + 1][character_pos[1]] != 4:
        character_pos = (character_pos[0] + 1, character_pos[1])
    if keys_pressed[pygame.K_LEFT] and character_pos[1] > 0 and terrain_map[character_pos[0]][character_pos[1] - 1] != 4:
        character_pos = (character_pos[0], character_pos[1] - 1)
    if keys_pressed[pygame.K_RIGHT] and character_pos[1] < len(terrain_map[0]) - 1 and terrain_map[character_pos[0]][character_pos[1] + 1] != 4:
        character_pos = (character_pos[0], character_pos[1] + 1)
    
    return character_pos
