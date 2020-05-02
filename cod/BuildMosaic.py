import os

import matplotlib.pyplot as plt

from cod.AddPiecesMosaic import *
from cod.Parameters import *


def load_pieces(params: Parameters):
    # citeste toate cele N piese folosite la mozaic din directorul corespunzator
    # toate cele N imagini au aceeasi dimensiune H x W x C, unde:
    # H = inaltime, W = latime, C = nr canale (C=1  gri, C=3 color)
    # functia intoarce pieseMozaic = matrice H x W x C x N in params
    # pieseMoziac(:,:,:,i) reprezinta piesa numarul i

    # # Obtinerea denumirilor pieselor pentru mozaic din director si citirea acestora
    # # intr-o lista, transformata apoi intr-o matrice H x W x C x N
    # img_names = [img for img in os.listdir(params.small_images_dir) if img.endswith(params.image_type)]
    # img_list = [cv.imread(params.small_images_dir + '/' + img_names[i]) for i in range(len(img_names))]
    # images = np.stack(img_list, axis=3)

    # AM MODIFICAT MODUL IN CARE SE FACE MEMORAREA IMAGINILOR (din matrice H x W x C x N in
    # matrice N x H x W x C), DEOARECE FUNCTIILE DIN SCRIPTUL 'AddPiecesMosaic.py' PRELUCREAZA
    # PIESELE PENTRU MOZAIC SUB FORMA UNEI MATRICI CU DIMENSIUNEA  N x H x W x C
    # (AM SCRIS SI FUNCTIILE DIN ACEST SCRIPT CONFORM FORMEI MODIFICATE)

    # Obtinerea denumirilor pieselor pentru mozaic din director si citirea acestora
    # intr-o matrice N x H x W x C
    img_names = [img for img in os.listdir(params.small_images_dir)
                 if img.endswith(params.image_type)]
    images = np.array([cv.imread(params.small_images_dir + '/' + img_names[i])
                       for i in range(len(img_names))])

    if params.show_small_images:
        for i in range(10):
            for j in range(10):
                plt.subplot(10, 10, i * 10 + j + 1)
                # OpenCV reads images in BGR format, matplotlib reads images in RBG format
                im = images[i * 10 + j].copy()
                # BGR to RGB, swap the channels
                im = im[:, :, [2, 1, 0]]
                plt.imshow(im)

        plt.savefig('1.png')
        plt.show()

    params.small_images = images


def compute_dimensions(params: Parameters):
    # calculeaza dimensiunile mozaicului
    # obtine si imaginea de referinta redimensionata avand aceleasi dimensiuni
    # ca mozaicul
    # completati codul
    # calculeaza automat numarul de piese pe verticala

    # Obtinerea dimensiunilor pieselor pentru mozaic
    # Obtinerea dimensiunilor originale ale imaginii de referinta
    small_img_h, small_img_w = params.small_images.shape[1:-1]
    ref_img_h, ref_img_w = params.image.shape[:-1]

    # Calcularea latimi(W) mozaicului
    new_w = params.num_pieces_horizontal * small_img_w
    # Calcularea numarului de piese necesare pe verticala pentru pastrarea
    # aspectului imaginii
    # Rotunjirea la intreg a numarului de piese necesare pe verticala obtinut,
    # deoarece compunem mozaicul din piese intregi
    params.num_pieces_vertical = round((new_w * ref_img_h) / (ref_img_w * small_img_h))
    # Calcularea inaltimii(H) mozaicului
    new_h = params.num_pieces_vertical * small_img_h

    # redimensioneaza imaginea
    params.image_resized = cv.resize(params.image, (new_w, new_h))


def set_mosaic_name(params: Parameters):
    """
    Construirea denumirii mozaicului care va contine informatii despre imaginea de referinta
    si despre parametrii layout, num_pieces_horizontal, criterion, constraint si hexagon
    pentru salvarea ca imagine in directorul specificat in parametrul 'output_path'.
    """
    try:
        os.mkdir(params.output_path[:-1])
    except OSError:
        print('Directory already created.')
    else:
        print('Directory created successfully.')

    mosaic_name = params.output_path
    mosaic_name += params.image_path.split('/')[-1].split('.')[0]
    mosaic_name += '_'
    mosaic_name += params.layout
    mosaic_name += str(params.num_pieces_horizontal)
    mosaic_name += '_'
    mosaic_name += params.criterion
    if params.constraint:
        mosaic_name += '_'
        mosaic_name += params.constraint
    if params.hexagon:
        mosaic_name += '_hexagonal'

    print(mosaic_name)
    return mosaic_name


def build_mosaic(params: Parameters):
    # incarcam imaginile din care vom forma mozaicul
    load_pieces(params)
    # calculeaza dimensiunea mozaicului
    compute_dimensions(params)

    img_mosaic = None
    if params.layout == 'caroiaj':
        if params.hexagon is True:
            img_mosaic = add_pieces_hexagon(params)
        else:
            img_mosaic = add_pieces_grid(params)
    elif params.layout == 'aleator':
        img_mosaic = add_pieces_random(params)
    else:
        print('Wrong option!')
        exit(-1)

    return img_mosaic
