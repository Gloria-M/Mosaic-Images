import pickle
import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt


def load_cifar10_test_batch(cifar10_dir_path):
    """
    Citirea colectiilor de imagini din 'test_batch' si a informatiilor despre denumirea
    si etichetele lor.
    """

    with open(cifar10_dir_path + '/test_batch', mode='rb') as file:
        batch = pickle.load(file, encoding='latin1')

    # Redimensionarea matricilor imaginilor din colectie si interschimbarea dimensiunilor
    # conform modului de lucru
    images = batch['data'].reshape((len(batch['data']), 3, 32, 32)).transpose(0, 2, 3, 1)
    labels = np.array(batch['labels'])
    filenames = np.array(batch['filenames'])

    return images, labels, filenames


def create_cifar10_collections(images, labels, filenames):
    """
    Salvarea imaginilor din setul CIFAR-10 in directoare corespunzatoare etichetelor lor.
    """

    collections_path = './../data/cifarImg'
    try:
        os.mkdir(collections_path)
    except OSError:
        print('Directory already created.')
    else:
        print('Directory created successfully.')

    label_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                   'dog', 'frog', 'horse', 'ship', 'truck']
    for l in label_names:
        try:
            os.mkdir(collections_path + '/' + l)
        except OSError:
            print('Directory already created.')
        else:
            print('Directory created successfully.')

    for idx in range(len(labels)):

        img_path = collections_path + '/' + label_names[labels[idx]] + '/' + filenames[idx]
        cv.imwrite(img_path, images[idx])


def plot_cifar(collection_path):

    img_names = [img for img in os.listdir(collection_path)
                 if img.endswith('png')]
    images = [cv.cvtColor(cv.imread(collection_path + '/' + img_names[i]), cv.COLOR_BGR2RGB) for i in range(20)]

    fig, axes = plt.subplots(2, 10, figsize=[20.9, 4.1])
    plt.subplots_adjust(wspace=.1, hspace=.1)

    for i in range(2):
        for j in range(10):

            axes[i][j].imshow(images[i*10+j])
            axes[i][j].set_xticks([])
            axes[i][j].set_yticks([])

    try:
        os.mkdir('./../data/cifarPlot')
    except OSError:
        print('Directory already created.')
    else:
        print('Directory created successfully.')

    plt.savefig('./../data/cifarPlot/' + collection_path.split('/')[-1] + '.png', dpi=300)
    # plt.show()


plot_cifar('./../data/cifarImg/automobile')
