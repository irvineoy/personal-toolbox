import numpy as np
from PIL import Image

individual = [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1515499035.057473, 1515499057.3824456, 16.068477655080642]
LENGTH = 24

def imread(fn):  # img as array
    return np.array(Image.open(fn).convert('L'))

def evaluation(individual):
    lenaOriginal = imread("lena.png")
    lenaNoise = imread("lena.png_noisy_NA_XXX_NFRow_XXX_NFCol_XXX.png")
    NoiseAmpBinary = individual[0:int(LENGTH / 3)]
    NoiseFreqRowBinary = individual[int(LENGTH / 3):int(LENGTH * 2 / 3)]
    NoiseFreqColBinary = individual[int(LENGTH * 2 / 3):LENGTH]
    NoiseAmp = 0
    NoiseFreqRow = 0
    NoiseFreqCol = 0
    for i, j in enumerate(NoiseAmpBinary):
        NoiseAmp += (j * 2) ** i
    for i, j in enumerate(NoiseFreqRowBinary):
        NoiseFreqRow += (j * 2) ** i
    for i, j in enumerate(NoiseFreqColBinary):
        NoiseFreqCol += (j * 2) ** i
    NoiseAmp = 30 * NoiseAmp / 2 ** (LENGTH / 3)
    NoiseFreqCol = 0.01 * NoiseFreqCol / 2 ** (LENGTH / 3)
    NoiseFreqRow = 0.01 * NoiseFreqRow / 2 ** (LENGTH / 3)
    noise = [[1.0 for i in range(512)] for j in range(512)]
    print("NoiseAmp is %f" % NoiseAmp)
    print("NoiseFreqRow is %f" % NoiseFreqRow)
    print("NoiseFreqCol is %f" % NoiseFreqCol)
    # print (lena.shape, lena.dtype)
    for row in range(lenaOriginal.shape[0]):
        for col in range(lenaOriginal.shape[1]):
            a = NoiseAmp * np.sin(2 * np.pi * NoiseFreqRow * row + 2 * np.pi * NoiseFreqCol * col)
            noise[row][col] = a
    noise = np.asarray(noise)
    lenaOriginal = np.asarray(lenaOriginal)
    lenaNoise = np.asarray(lenaNoise)
    differ = lenaNoise - noise
    noise = Image.fromarray(noise)
    noise.show()
    differ = Image.fromarray(differ)
    differ.show()
    individual[-1] = np.absolute(differSum)
    individual[-2] = time.time()
    return individual[-1]

evaluation(individual)
