import cv2 as cv
import numpy as np
import tensorflow as tf
import imutils
import os
from PIL import ImageGrab


def screen2cells():
    # Saving screenshot
    try:
        im = ImageGrab.grabclipboard()
        im.save('assets/cells/screenshot.png')
    except AttributeError:
        return False

    # --Image processing--
    image = cv.imread('assets/cells/screenshot.png', cv.IMREAD_GRAYSCALE)  # Reading an image in grayscale
    image = cv.GaussianBlur(image.copy(), (9, 9), 0)  # Blurs image to get rid of noise. K-Size % 2 == 1, Kernel is sqr
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 7, 2)  # Thresh + Inv

    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    image = cv.dilate(image, kernel)

    # --Finding contours--
    cnts = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:2]  # Returns 2 contours with biggest area

    # --PolyDP - Finds corners of a box--
    for curve in cnts:
        perim = cv.arcLength(curve, True)
        approx = cv.approxPolyDP(curve, 0.015 * perim, True)
        if len(approx) == 4:  # Searches for largest 4-side contour
            cnts = approx
            break

    # --Extracting corners--
    corners = [(corner[0][0], corner[0][1]) for corner in cnts]
    top_l, top_r, bot_l, bot_r = corners[0], corners[3], corners[1], corners[2]  # FIXME if bugged do smth

    # --Cropping & Warping image--
    # Getting width/height
    width_a = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width_b = np.sqrt(((bot_r[0] - bot_l[0]) ** 2) + ((bot_r[1] - bot_l[1]) ** 2))
    width = max(int(width_a), int(width_b))

    height_a = np.sqrt(((top_r[0] - bot_r[0]) ** 2) + ((top_r[1] - bot_r[1]) ** 2))
    height_b = np.sqrt(((top_l[0] - bot_l[0]) ** 2) + ((top_l[1] - bot_l[1]) ** 2))
    height = max(int(height_a), int(height_b))

    # Numpy formatting
    dimension = np.array([
        [0, 0],  # Top-left
        [width - 1, 0],  # Top-right
        [width - 1, height - 1],  # Bot-right
        [0, height - 1],  # Bot-left
    ], dtype="float32")

    enum_corners = np.array((top_l, top_r, bot_r, bot_l), dtype="float32")

    # Cropping and warping
    m = cv.getPerspectiveTransform(enum_corners, dimension)
    image = cv.warpPerspective(image, m, (width, height))

    # --Creating a grid--
    edge_h, edge_w = np.shape(image)[0], np.shape(image)[1]
    cell_h, cell_w = edge_h // 9, edge_w // 9

    # Creating temporary grid with images
    temp_grid = []
    for i in range(cell_h, edge_h + 1, cell_h):
        for j in range(cell_w, edge_w + 1, cell_w):
            rows = image[i - cell_h:i]
            temp_grid.append([rows[k][j - cell_w:j] for k in range(len(rows))])

    # Creating the 9X9 grid of images
    grid = []
    for i in range(0, len(temp_grid) - 8, 9):
        grid.append(temp_grid[i:i + 9])

    # Converting to the numpy array
    for i in range(9):
        for j in range(9):
            grid[i][j] = np.array(grid[i][j])

    # Saving cells as images
    try:  # Deleting previous files
        for i in range(9):
            for j in range(9):
                os.remove(f"assets/cells/cell{i}{j}.jpg")
    except FileNotFoundError:
        pass
    for i in range(9):
        for j in range(9):
            grid[i][j] = cv.resize(grid[i][j], (36, 36))
            grid[i][j] = grid[i][j][4:32, 4:32]  # Crops to 28x28
            cv.imwrite(str(f"assets/cells/cell{i}{j}.png"), grid[i][j])
    return True


def cells2board():
    # Loads an AI
    board = [[] for _ in range(9)]
    model = tf.keras.models.load_model('recognition.model')

    for row in range(9):
        for col in range(9):
            # Switching images to grayscale
            image = cv.imread(f'assets/cells/cell{row}{col}.png')
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            image = cv.threshold(image, 128, 255, cv.THRESH_BINARY)[1]

            # # Cropping lines
            # size = 28
            # crop = 3
            # image[:crop, :size] = [0]  # Upper line
            # image[size - crop:, :size] = [0]  # Bottom
            # image[:size, :crop] = [0]  # Left
            # image[:size, size - crop:] = [0]  # Right

            image = image.astype('float32')
            image = image.reshape(1, 28, 28, 1)
            image /= 255

            prediction = model.predict(image)
            board[row].append(np.argmax(prediction) if max(prediction[0]) > 0.8 else 0)
    return board
