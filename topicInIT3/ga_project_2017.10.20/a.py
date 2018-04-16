# import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as pyplot  

NoiseAmp = 60
NoiseFreqRow = 0.01
NoiseFreqCol = 0.01

def imread(fn) : # img as array
	return np.array(Image.open(fn).convert('L'))
	return cv2.imread(fn, cv2.IMREAD_GRAYSCALE)

def evaluation():
	lena = imread("lena.png")
	lenaNoise = imread("lena.png_noisy_NA_XXX_NFRow_XXX_NFCol_XXX.png")
	noise = [[1.0 for i in range(512)] for j in range(512)]
	print (lena.shape, lena.dtype)
	for row in range(lena.shape[0]):
		for col in range(lena.shape[1]):
			a = NoiseAmp * np.sin(float(2 * np.pi * NoiseFreqRow * row + 2 * np.pi * NoiseFreqCol * col))
			noise[row][col] = a
	noise = np.array(lenaNoise - lena)
	noise = Image.fromarray(noise)
	noise.show()
	# print (noise.shape, noise.dtype)
	# pyplot.imshow(noise)
	# pyplot.show()
evaluation()
# if "__name__" == "__main__":
# 	evaluation()