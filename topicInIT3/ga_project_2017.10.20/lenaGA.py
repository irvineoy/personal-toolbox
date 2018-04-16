from random import random, shuffle, randint, choice
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sys
import time

fig = plt.gcf()
fig.set_size_inches(18, 6)

LENGTH = 24  # DNA's length
N = 600  # population
Mprob = 0.05
Cprob = 1.0
Iterations = 1000


def rand_idx(N): return randint(0, N - 1)


def coin(p=0.5): return 1 if (random() < p) else 0


def random_individual(LENGTH):
    return [coin() for i in range(LENGTH)]


def initial_population(N, LENGTH):
    # individual[-1] is fitness
    # individual[-2] is last updata time
    # individual[-3] is last changed time
    return [random_individual(LENGTH+3) for i in range(N)]


def fitness(c):
    if c[-2] > c[-3]:
        return c[-1]
    else:
        return evaluation(c)
def fitness(c): return evaluation(c)


def updateGlobleElite(population):
    fitnessList = []
    global eliteInd
    fitnessList.append(fitness(population[i]) for i in range(N))
    maxPointer = fitnessList.index(max(fitnessList))
    if fitness(population[maxPointer]) > fitness(eliteInd):
        eliteInd = population[maxPointer]
    return


def selection(population):
    updateGlobleElite(population)
    # print fitness(eliteInd)
    newPopulation = []
    for i in range(N):
        temp = choice(population)
        temp2 = choice(population)
        temp3 = temp if fitness(temp) < fitness(temp2) else temp2
        newPopulation.append(temp3)
    # newPopulation[1] = eliteInd
    # updateGlobleElite(newPopulation)
    return newPopulation


def crossover(population):
    newPopulation = []
    k = rand_idx(LENGTH)
    for i in range(int(N / 2)):
        nc1 = c1 = population[2 * i]
        nc2 = c2 = population[2 * i + 1]
        if random() < Cprob:
            nc1 = c1[:k] + c2[k:]
            nc2 = c2[:k] + c1[k:]
        nc1[-3] = time.time()
        nc2[-3] = time.time()
        newPopulation.append(nc1)
        newPopulation.append(nc2)
    return newPopulation


def mutation(population):
    for i in range(N):
        if coin(Mprob):
            k = rand_idx(LENGTH)
            population[i][k] = 1 - population[i][k]
            population[i][-3] = time.time()
    return population


def check_stop(fitness_population):
    if echo > Iterations:
        return True
    else:
        return False


def sum_population(fitness_population):
    summerOne = 0
    for i in fitness_population:
        summerOne += fitness(i)
    return summerOne


def show(population, graphData):
    print('The echo is: %d' % (echo))
    minFitness = sys.maxsize
    minList = []
    for i in population:
        if minFitness > fitness(i):
            minFitness = fitness(i)
            minList = i
    graphData.append(minFitness)
    print(minList)
    print('The min is: %f' % (minFitness))
    print ('')


def imread(fn):  # img as np array
    return np.array(Image.open(fn).convert('L'))
    return cv2.imread(fn, cv2.IMREAD_GRAYSCALE)


lenaOriginal = imread("lena.png")
lenaNoise = imread("lena.png_noisy_NA_XXX_NFRow_XXX_NFCol_XXX.png")
row, col = np.meshgrid(np.arange(512), np.arange(512), sparse=True)
noise = np.zeros((512, 512), dtype = np.float64)


def evaluation(individual):
    global row, col, noise
    global lenaOriginal, lenaNoise
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
    # print("NoiseAmp is %f" % NoiseAmp)
    # print("NoiseFreqRow is %f" % NoiseFreqRow)
    # print("NoiseFreqCol is %f" % NoiseFreqCol)
    # print (lena.shape, lena.dtype)
    noise = NoiseAmp * np.sin(2 * np.pi * NoiseFreqRow * row + 2 * np.pi * NoiseFreqCol * col)
    differ = (lenaNoise - lenaOriginal) - noise
    differSum = np.sum(np.abs(differ)) / (512*512)
    # noise = Image.fromarray(noise)
    # noise.show()
    individual[-1] = differSum
    individual[-2] = time.time()
    return individual[-1]


def run(graphData):
    population = initial_population(N, LENGTH)
    global echo
    global eliteInd
    eliteInd = population[0]
    echo = 0
    while True:
        population = crossover(population)
        population = mutation(population)
        population = selection(population)
        show(population, graphData)
        echo += 1
        if check_stop(population): break
    print(graphData)


def plotGraph(graphData, label):
    index = []
    for i, j in enumerate(graphData):
        index.append(i)
    print(len(index))
    print(len(graphData))
    return plt.plot(index, graphData, label=label)


if __name__ == '__main__':
    graphData = []
    run(graphData)
    # LENGTH = 192
    # Mprob = 0.05
    # Cprob = 0.95
    # Iterations = 100
    # N = 100
    # graphData_1 = []
    # Mprob = 0.00
    # run(graphData_1)

    # graphData_2 = []
    # Mprob = 0.01
    # run(graphData_2)

    # graphData_3 = []
    # Mprob = 0.05
    # run(graphData_3)

    # graphData_4 = []
    # Mprob = 0.50
    # run(graphData_4)

    # graphData_5 = []
    # Mprob = 1.00
    # run(graphData_5)

    # plot1 = plotGraph(graphData_1, 'Mprob = 0.00')
    # plot2 = plotGraph(graphData_2, 'Mprob = 0.01')
    # plot3 = plotGraph(graphData_3, 'Mprob = 0.05')
    # plot4 = plotGraph(graphData_4, 'Mprob = 0.50')
    # plot4 = plotGraph(graphData_5, 'Mprob = 1.00')
    # plt.xlabel('Para = (LENGTH:192, Iteration:100, N:100, Cprob:0.95)')
    # plt.ylabel('Best fitness')
    # plt.legend(loc = 'upper left')
    # fig.savefig('fig/Mutation.png', dpi=100)
    # plt.show()
