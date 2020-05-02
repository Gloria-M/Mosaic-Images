"""
    PROIECT MOZAIC
"""

# Parametrii algoritmului sunt definiti in clasa Parameters.
from cod.BuildMosaic import *
from cod.ProcessCifar10 import *

images, labels, filenames = load_cifar10_test_batch('./../data/cifar10')
create_cifar10_collections(images, labels, filenames)

image_path = './../data/cifarTest/ship.jpg'
params = Parameters(image_path)

# directorul cu imagini folosite pentru realizarea mozaicului
params.small_images_dir = './../data/cifarImg/ship/'
# tipul imaginilor din director
params.image_type = 'png'
# numarul de piese ale mozaicului pe orizontala
# # pe verticala vor fi calcultate dinamic a.i sa se pastreze raportul
params.num_pieces_horizontal = 100
# afiseaza piesele de mozaic dupa citirea lor
params.show_small_images = False
# modul de aranjarea a pieselor mozaicului
# optiuni: 'aleator', 'caroiaj'
params.layout = 'caroiaj'
# criteriul dupa care se realizeaza mozaicul
# optiuni: 'aleator', 'distantaCuloareMedie'
params.criterion = 'distantaCuloareMedie'
# proprietatea ca nu exista doua piese adiacente (stanga, dreapta, jos, sus) identice
# optiuni: None, 'diferite'
params.constraint = None
# daca params.layout == 'caroiaj', sa se foloseasca piese hexagonale
params.hexagon = False
# schimbarea directorului in care vor fi salvate imaginile mozaic
params.output_path = './../data/outputCifar/'

img_mosaic = build_mosaic(params)

img_name = set_mosaic_name(params)
cv.imwrite(img_name + '.png', img_mosaic, [cv.IMWRITE_PNG_COMPRESSION, 7])
