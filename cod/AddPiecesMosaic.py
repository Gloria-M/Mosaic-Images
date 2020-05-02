from cod.ProcessMosaic import *
import numpy as np
import timeit


def add_pieces_grid(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal

    if params.criterion == 'aleator':
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                index = np.random.randint(low=0, high=N, size=1)
                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    elif params.criterion == 'distantaCuloareMedie':

        # calcularea culorilor medii a imaginilor din colectie
        compute_average_color_small_img(params)

        # verificam existenta vreunei constrangeri asupra modului de alegere a pieselor
        if params.constraint:
            # pentru a verifica valorile vecinilor fiecarei pozitii in grid, construim
            # matricea 'grid' in care vom memora pentru fiecare piesa asezata, indicele acesteia
            # in matricea 'params.small_images'
            # initializam cu valoarea -1, deoarece nu exista pozitia cu aceasta valoare
            grid = np.full((params.num_pieces_vertical, params.num_pieces_horizontal), -1)

            for r in range(params.num_pieces_vertical):
                for c in range(params.num_pieces_horizontal):
                    # calcularea culorii medii a sectiunii de imagine determinata de 'r' si 'c'
                    img_avg_color = compute_average_color_ref_image(params, r * H, c * W)
                    # definim distanta minima intre culorile medii a doua imagini ca fiind mai mare
                    # decat maximul posibil
                    min_dist = 450

                    # pentru fiecare pozitie pe grid, aflam valorile vecinilor
                    neighbours = get_neighbours_grid(grid, r, c)
                    for i in range(N):
                        if i not in neighbours:
                            # calcularea distantei euclidiene intre culorile medii ale piesei condidat
                            # si ale sectiunii corespunzatoare din imaginea de referinta
                            euclidean_dist = compute_euclidean_distance(img_avg_color,
                                                                        params.small_images_avg_color[i])
                            # daca este cazul, actualizam valoarea 'min_dist' si adaugam piesa gasita
                            # in matricea 'img_mosaic' si indicele acesteia in matricea 'grid'
                            if min_dist > euclidean_dist:
                                min_dist = euclidean_dist
                                grid[r, c] = i
                                img_mosaic[r * H:(r + 1) * H, c * W:(c + 1) * W, :] = params.small_images[i]

                    print('Building mosaic %.2f%%' % (100 * (r * params.num_pieces_horizontal + c + 1) / num_pieces))

        else:
            # pentru fiecare portiune din imaginea de referinta si fiecare imagine-candidat,
            # calculam distanta euclidiana si comparam cu valoarea 'min_dist'
            for r in range(params.num_pieces_vertical):
                for c in range(params.num_pieces_horizontal):
                    # calcularea culorii medii a sectiunii de imagine determinata de 'r' si 'c'
                    img_avg_color = compute_average_color_ref_image(params, r * H, c * W)
                    # definim distanta minima intre culorile medii a doua imagini ca fiind mai mare
                    # decat maximul posibil
                    min_dist = 450

                    for i in range(N):
                        # calcularea distantei euclidiene intre culorile medii ale piesei condidat
                        # si ale sectiunii corespunzatoare din imaginea de referinta
                        euclidean_dist = compute_euclidean_distance(img_avg_color,
                                                                    params.small_images_avg_color[i])
                        # daca este cazul, actualizam valoarea 'min_dist' si adaugam piesa gasita
                        # in matricea 'img_mosaic'
                        if min_dist > euclidean_dist:
                            min_dist = euclidean_dist
                            img_mosaic[r * H:(r + 1) * H, c * W:(c + 1) * W, :] = params.small_images[i]

                    print('Building mosaic %.2f%%' % (100 * (r * params.num_pieces_horizontal + c + 1) / num_pieces))

    else:
        print('Error! unknown option %s' % params.criterion)
        exit(-1)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic


def add_pieces_random(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)

    mosaic_h, mosaic_w = params.image_resized.shape[:-1]
    N, H, W = params.small_images.shape[:-1]
    h, w, c = params.image_resized.shape

    # in matricea 'filled_pixels' de dimensiuni inaltimea si latimea mozaicului
    # vor fi marcati cu 0 pixelii neacoperiti si cu 1 cei acoperiti
    # in variabila 'empty_pixels' se va tine evidenta pixelilor ramasi neacoperiti
    filled_pixels = np.zeros((mosaic_h, mosaic_w))
    empty_pixels = mosaic_h * mosaic_w

    # calcularea culorilor medii a imaginilor din colectie
    compute_average_color_small_img(params)

    # criteriul de oprire este acoperirea tuturor pixelilor din grid cu pixeli
    # din piesele candidat
    # din cauza timpului foarte mare necesar acoperii intregului grid, criteriul de 
    # oprire este acoperirea in proportie de 99%
    while empty_pixels > h * w / 100:
        # alegerea unei pozitii in grid
        r = np.random.randint(low=0, high=mosaic_h - H, size=1)[0]
        c = np.random.randint(low=0, high=mosaic_w - W, size=1)[0]

        # calcularea culorii medii a sectiunii de imagine determinata de 'r' si 'c'
        img_avg_color = compute_average_color_ref_image(params, r, c)
        # definim distanta minima intre culorile medii a doua imagini ca fiind mai mare
        # decat maximul posibil
        min_dist = 450
        for i in range(N):
            # calcularea distantei euclidiene intre culorile medii ale piesei condidat
            # si ale sectiunii corespunzatoare din imaginea de referinta
            euclidean_dist = compute_euclidean_distance(img_avg_color,
                                                        params.small_images_avg_color[i])
            # daca este cazul, actualizam valoarea 'min_dist' si adaugam piesa gasita
            # in matricea 'img_mosaic'
            if min_dist > euclidean_dist:
                min_dist = euclidean_dist
                img_mosaic[r:r + H, c:c + W, :] = params.small_images[i]

        # actualizarea numarului de pixeli ramasi neacoperiti
        empty_pixels -= num_filled_pixels(params, filled_pixels, r, c)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic


def add_pieces_hexagon(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape

    # calcularea culorilor medii a imaginilor din colectie
    compute_average_color_small_img(params)

    # construirea mastii hexagon de dimensiunile pieselor candidat
    mask = create_mask((H, W, C))

    # calcularea numarului de hexagoane pe verticala si orizontala, functie de numarul de piese
    # pe orizontala si pe verticala
    r_hexa = int(2 * params.num_pieces_vertical)
    c_hexa = int(4 * params.num_pieces_horizontal / 3)
    num_pieces = params.num_pieces_vertical * c_hexa
    # constuirea matricei in care se vor salva piesele alese pentru fiecare hexagon din grid
    hexa_grid = np.full((r_hexa, c_hexa), -1)

    if params.constraint:
        for r in range(r_hexa + 1):
            # tratarea diferita a cazurilor in care pozitia in grid este pe rand par si impar
            # calcularea pixelului din coltul stanga-sus al sectiunii in mozaic
            if r % 2:
                r_left = int((int(r / 2) + 1) * H - H / 2)
                c_start = 1
            else:
                r_left = int(r / 2 * H)
                c_start = 0
            for c in range(c_start, c_hexa + 1, 2):
                c_left = int(c * W - W / 4 * c)

                if c_left + W <= w and r_left + H <= h:
                    # calcularea culorii medii a sectiunii de imagine determinata de 'r' si 'c'
                    img_avg_color = compute_average_color_ref_image(params, r_left, c_left)
                    # definim distanta minima intre culorile medii a doua imagini ca fiind mai mare
                    # decat maximul posibil
                    min_dist = 450

                    # pentru fiecare pozitie pe grid, aflam valorile vecinilor
                    neighbours = get_neighbours_hexa(hexa_grid, r, c)

                    for i in range(N):
                        if i not in neighbours:
                            # calcularea distantei euclidiene intre culorile medii ale piesei condidat
                            # si ale sectiunii corespunzatoare din imaginea de referinta
                            euclidean_dist = compute_euclidean_distance(img_avg_color,
                                                                        params.small_images_avg_color[i])
                            # daca este cazul, actualizam valoarea 'min_dist' si adaugam indicele piesei gasite
                            # in matricea 'hexa_grid'
                            if min_dist > euclidean_dist:
                                min_dist = euclidean_dist
                                hexa_grid[r, c] = i
                                hexa_grid[r + 1, c] = i

                    # actualizam imaginea mozaic cu noua piesa gasita
                    best_piece = hexa_grid[r, c]
                    masked_piece = cv.bitwise_and(params.small_images[best_piece], mask, (255, 255, 255))
                    img_mosaic[r_left:r_left + H, c_left:c_left + W, :] += masked_piece

            if r % 2:
                print('Building mosaic %.2f%%' % (100 * (int((r+1)/2) * c_hexa) / num_pieces))

    else:
        # tratarea diferita a cazurilor in care pozitia in grid este pe rand par si impar
        # calcularea pixelului din coltul stanga-sus al sectiunii in mozaic
        for r in range(r_hexa + 1):
            if r % 2:
                r_left = int((int(r / 2) + 1) * H - H / 2)
                c_start = 1
            else:
                r_left = int(r / 2 * H)
                c_start = 0
            for c in range(c_start, c_hexa + 1, 2):
                c_left = int(c * W - W / 4 * c)

                if c_left + W <= w and r_left + H <= h:
                    # calcularea culorii medii a sectiunii de imagine determinata de 'r' si 'c'
                    img_avg_color = compute_average_color_ref_image(params, r_left, c_left)
                    # definim distanta minima intre culorile medii a doua imagini ca fiind mai mare
                    # decat maximul posibil
                    min_dist = 450

                    for i in range(N):
                        # calcularea distantei euclidiene intre culorile medii ale piesei condidat
                        # si ale sectiunii corespunzatoare din imaginea de referinta
                        euclidean_dist = compute_euclidean_distance(img_avg_color,
                                                                    params.small_images_avg_color[i])
                        # daca este cazul, actualizam valoarea 'min_dist' si adaugam indicele piesei gasite
                        # in matricea 'hexa_grid'
                        if min_dist > euclidean_dist:
                            min_dist = euclidean_dist
                            hexa_grid[r, c] = i
                            hexa_grid[r + 1, c] = i

                    # actualizam imaginea mozaic cu noua piesa gasita
                    best_piece = hexa_grid[r, c]
                    masked_piece = cv.bitwise_and(params.small_images[best_piece], mask, (255, 255, 255))
                    img_mosaic[r_left:r_left + H, c_left:c_left + W, :] += masked_piece

            if r % 2:
                print('Building mosaic %.2f%%' % (100 * (int((r+1)/2) * c_hexa) / num_pieces))

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic
