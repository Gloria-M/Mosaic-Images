from cod.Parameters import *

import numpy as np
import math as m


def compute_average_color_small_img(params: Parameters):
    """
    Calcularea culorilor medii pe cele 3 canale pentru imaginile piese de mozaic.
    """

    params.small_images_avg_color = np.empty(len(params.small_images), dtype=object)
    for i in range(len(params.small_images)):
        blue_ch = np.mean(params.small_images[i, :, :, 0])
        green_ch = np.mean(params.small_images[i, :, :, 1])
        red_ch = np.mean(params.small_images[i, :, :, 2])

        params.small_images_avg_color[i] = [blue_ch, green_ch, red_ch]


def compute_average_color_ref_image(params: Parameters, top_left_x, top_left_y):
    """
    Calcularea culorilor medii pe cele 3 canale pentru o sectiune de dimensiune HxW din
    imaginea de referinta, avand coltul stanga-sus de coordonate (top_left_x, top_left_y).
    """

    H, W = params.small_images.shape[1:-1]
    blue_ch = np.mean(params.image_resized[top_left_x:top_left_x+H, top_left_y:top_left_y+W, 0])
    green_ch = np.mean(params.image_resized[top_left_x:top_left_x+H, top_left_y:top_left_y+W, 1])
    red_ch = np.mean(params.image_resized[top_left_x:top_left_x+H, top_left_y:top_left_y+W, 2])

    return [blue_ch, green_ch, red_ch]


def compute_euclidean_distance(img_avg_color, small_img_avg_color):
    """
    Calcularea distantei euclidiene intre doua imagini, functie de culorile lor medii.
    """
    return m.sqrt((img_avg_color[0] - small_img_avg_color[0])**2 +
                  (img_avg_color[1] - small_img_avg_color[1])**2 +
                  (img_avg_color[2] - small_img_avg_color[2])**2)


def get_neighbours_grid(grid, row, column):
    """
    Gasirea valorilor vecinilor unei piese in grid, avand pozitia (row, column).
    Se tine cont de modul de completare a gridului: de sus in jos si
    de la stanga la dreapta.
    """

    # gasirea randului si a coloanei maxime, pentru verificarea pozitiei vecinilor
    max_row, max_col = grid.shape

    neighbours = []
    neighbours_pos = [[row - 1, column], [row, column - 1], [row, column + 1]]

    # daca pozitia unui vecin este in afara gridului, o ignoram
    for pos in neighbours_pos:
        if -1 < pos[0] < max_row:
            if -1 < pos[1] < max_col:
                neighbours.append(grid[pos[0], pos[1]])

    return list(set(neighbours))


def get_neighbours_hexa(hexa_grid, row, column):
    """
    Gasirea valorilor vecinilor unei piese in grid, avand pozitia (row, column).
    Se tine cont de modul de completare a gridului: de sus in jos si
    de la stanga la dreapta.
    """

    # gasirea randului si a coloanei maxime, pentru verificarea pozitiei vecinilor
    # gasirea randului minim, tratata diferit functie de paritatea coloanei
    max_row, max_col = hexa_grid.shape
    if column % 2:
        max_row -= 1
        min_row = 1
    else:
        min_row = 0

    neighbours = []
    neighbours_pos = [[row - 1, column], [row, column - 1], [row, column + 1]]

    # daca pozitia unui vecin este in afara gridului, o ignoram
    for pos in neighbours_pos:
        if min_row <= pos[0] < max_row:
            if -1 < pos[1] < max_col:
                neighbours.append(hexa_grid[pos[0], pos[1]])

    return list(set(neighbours))


def num_filled_pixels(params: Parameters, filled_pixels, top_left_x, top_left_y):
    """
    Calcularea numarului de pixeli nou-acoperiti de o piesa, in sectiunea din grid avand
    coltul stanga-sus de coordonate (top_left_x, top_left_y) si actualizarea matricei
    'filled_pixels' corespunzator.
    """

    h, w = params.small_images.shape[1:-1]
    # pixelii acoperiti sunt reprezentati cu 1, iar cei neacoperiti cu 0
    # asadar, numarul celor deja acoperiti reprezinta suma valorilor intregii sectiuni
    num_filled = w * h - np.sum(filled_pixels[top_left_x:top_left_x+h, top_left_y:top_left_y+w])

    filled_pixels[top_left_x:top_left_x+h, top_left_y:top_left_y+w] = np.ones((h, w))

    return num_filled


def create_mask(src_img_size):
    """
    Construirea unei masti hexagonale de dimensiunile imaginilor piese candidat.
    """

    h, w, c = src_img_size
    mask = np.zeros(src_img_size, np.uint8)

    # definirea coordonatelor hexagonului inscris in piesa candidat
    hexa_coord = np.array([[w / 4, 0], [3 * w / 4, 0], [w, h / 2], [3 * w / 4, h], [w / 4, h], [0, h / 2]], np.int32)
    cv.fillPoly(mask, [hexa_coord], (255, 255, 255))

    return mask
