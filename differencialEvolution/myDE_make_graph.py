# python3
import numpy as np
import matplotlib.pyplot as plt
fig = plt.gcf()
fig.set_size_inches(18, 6)

size = 80
dimension = 10
lowerBound = -5.12
upperBound = 5.12
iteration = 500
F = 0.5
crProb = 0.8


def evaluation_sphere(individual):
    y = 0.0
    for x in individual:
        y = y + (x ** 2)
    return y


def evaluation_rastrigin(individual):
    y = dimension * 10
    for ｘ in individual:
        y = y + x ** 2 - 10 * np.cos(2 * np.pi * x)
    return y


def initial(population, newPopulation):
    for i in range(size):
        for j in range(dimension):
            population[i][j] = lowerBound + np.random.random() * (upperBound - lowerBound)
    newPopulation = population.copy()
    return population, newPopulation


def mutationAndCrossover(population, newPopulation):
    for i in range(size):
        ind0, ind1, ind2 = 0, 0, 0
        while ind0 == ind1 or ind1 == ind2 or ind2 == ind0 or ind0 == i or ind1 == i or ind2 ==i:
            ind0 = np.random.randint(size)
            ind1 = np.random.randint(size)
            ind2 = np.random.randint(size)
        tempInd0, tempInd1, tempInd2 = population[ind0], population[ind1], population[ind2]
        tempInd4 = tempInd0 + F * (tempInd1 - tempInd2)
        for j in range(dimension):
            if tempInd4[j] > upperBound:
                tempInd4[j] = upperBound - np.random.random() * (tempInd4[j] - upperBound)
            if tempInd4[j] < lowerBound:
                tempInd4[j] = lowerBound + np.random.random() * (lowerBound - tempInd4[j])
        newPopulation[i] = [tempInd4[k] if np.random.random() < crProb else population[i][k] for k in range(dimension)]
        if evaluation_rastrigin(population[i]) < evaluation_rastrigin(newPopulation[i]):
            newPopulation[i] = population[i]
    population = newPopulation.copy()
    return population, newPopulation


def whichTheBest(population):
    evaluateResult = [evaluation_rastrigin(population[i]) for i in range(size)]
    bestResult = population[np.argmin(evaluateResult)]
    return bestResult


def plotGraph(graphData, label):
    index = []
    for i,j in enumerate(graphData):
        index.append(i)
    return plt.plot(index, graphData, label = label)


def run(allBestResult):
    population = np.zeros((size, dimension))
    newPopulation = np.zeros((size, dimension))
    population, newPopulation = initial(population, newPopulation)
    for i in range(iteration):
        print('The iteration is %d' % i)
        population, newPopulation = mutationAndCrossover(population, newPopulation)
        bestResult = whichTheBest(population)
        print('The best is:')
        print(bestResult)
        thisResult = evaluation_rastrigin(bestResult)
        allBestResult[i] += (thisResult)
        print('The result is: %f' % thisResult)
        print()
    return allBestResult

def crossoverPlot():
    global crProb
    graphData_1 = np.zeros((iteration))
    crProb = 0.2
    for i in range(10):
        graphData_1 = run(graphData_1)
    graphData_1 = graphData_1 / 10.0

    graphData_2 = np.zeros((iteration))
    crProb = 0.5
    for i in range(10):
        graphData_2 = run(graphData_2)
    graphData_2 = graphData_2 / 10.0

    graphData_3 = np.zeros((iteration))
    crProb = 0.8
    for i in range(10):
        graphData_3 = run(graphData_3)
    graphData_3 = graphData_3 / 10.0

    graphData_4 = np.zeros((iteration))
    crProb = 1.0
    for i in range(10):
        graphData_4 = run(graphData_4)
    graphData_4 = graphData_4 / 10.0

    plot1 = plotGraph(graphData_1, 'crProb = 0.2')
    plot2 = plotGraph(graphData_2, 'crProb = 0.5')
    plot3 = plotGraph(graphData_3, 'crProb = 0.8')
    plot4 = plotGraph(graphData_4, 'crProb = 1.0')
    plt.xlabel('Para = (Dimension:10, Iteration:500, size:80, F:0.5)')
    plt.ylabel('Best fitness')
    plt.legend(loc = 'upper right')
    fig.savefig('fig/crossover_rastrigin.png', dpi=100)

def FPlot():
    global F
    graphData_1 = np.zeros((iteration))
    F = 0.3
    for i in range(10):
        graphData_1 = run(graphData_1)
    graphData_1 = graphData_1 / 10.0

    graphData_2 = np.zeros((iteration))
    F = 0.5
    for i in range(10):
        graphData_2 = run(graphData_2)
    graphData_2 = graphData_2 / 10.0

    graphData_3 = np.zeros((iteration))
    F = 0.8
    for i in range(10):
        graphData_3 = run(graphData_3)
    graphData_3 = graphData_3 / 10.0

    graphData_4 = np.zeros((iteration))
    F = 1.5
    for i in range(10):
        graphData_4 = run(graphData_4)
    graphData_4 = graphData_4 / 10.0

    plot1 = plotGraph(graphData_1, 'F = 0.3')
    plot2 = plotGraph(graphData_2, 'F = 0.5')
    plot3 = plotGraph(graphData_3, 'F = 0.8')
    plot4 = plotGraph(graphData_4, 'F = 1.5')
    plt.xlabel('Para = (Dimension:10, Iteration:500, size:80, crProb:0.8)')
    plt.ylabel('Best fitness')
    plt.legend(loc = 'upper right')
    fig.savefig('fig/F_rastrigin.png', dpi=100)


def sizePlot():
    global size
    graphData_1 = np.zeros((iteration))
    size = 20
    for i in range(10):
        graphData_1 = run(graphData_1)
    graphData_1 = graphData_1 / 10.0

    graphData_2 = np.zeros((iteration))
    size = 80
    for i in range(10):
        graphData_2 = run(graphData_2)
    graphData_2 = graphData_2 / 10.0

    graphData_3 = np.zeros((iteration))
    size = 200
    for i in range(10):
        graphData_3 = run(graphData_3)
    graphData_3 = graphData_3 / 10.0

    graphData_4 = np.zeros((iteration))
    size = 500
    for i in range(10):
        graphData_4 = run(graphData_4)
    graphData_4 = graphData_4 / 10.0

    plot1 = plotGraph(graphData_1, 'size = 20')
    plot2 = plotGraph(graphData_2, 'size = 80')
    plot3 = plotGraph(graphData_3, 'size = 200')
    plot4 = plotGraph(graphData_4, 'size = 500')
    plt.xlabel('Para = (Dimension:10, Iteration:500, F:0.5, crProb:0.8)')
    plt.ylabel('Best fitness')
    plt.legend(loc = 'upper right')
    fig.savefig('fig/size_rastrigin2.png', dpi=100)


if __name__ == '__main__':
	# crossoverPlot()
    # FPlot()
    sizePlot()

