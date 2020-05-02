import cv2 as cv


# In aceasta clasa vom stoca detalii legate de algoritm si de imaginea pe care este aplicat.
class Parameters:

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv.imread(image_path)
        if self.image is None:
            print('%s is not valid' % image_path)
            exit(-1)
        self.image_resized = None

        self.small_images_dir = './../data/colectie/'
        self.image_type = 'png'
        self.num_pieces_horizontal = 100
        self.num_pieces_vertical = None
        self.show_small_images = False

        self.layout = 'caroiaj'
        self.criterion = 'aleator'
        self.hexagon = False
        # parametru in care se specifica daca in construirea mozaicului, piesele adiacente
        # trebuie sa fie diferite
        self.constraint = None

        self.small_images = None

        # parametru folosit pentru memorarea valorilor culorilor medii a imaginilor
        # candidat, pentru evitarea calculelor repetate
        self.small_images_avg_color = None

        # parametru care precizeaza adresa la care se vor salva imaginile rezultate
        self.output_path = './../data/output/'
