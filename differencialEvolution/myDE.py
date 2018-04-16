# python3
import numpy as np

size = 80
dimension = 10
lowerBound = -5.12
upperBound = 5.12
iteration = 1000
F = 0.3
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


def mutation_crossover_selection(population, newPopulation):
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
    # print(evaluateResult)
    bestResult = population[np.argmin(evaluateResult)]
    return bestResult


if __name__ == '__main__':
    population = np.zeros((size, dimension))
    newPopulation = np.zeros((size, dimension))
    population, newPopulation = initial(population, newPopulation)
    allBestResult = []
    for i in range(iteration):
        print('The iteration is %d' % i)
        population, newPopulation = mutation_crossover_selection(population, newPopulation)
        bestResult = whichTheBest(population)
        print('The best is:')
        print(bestResult)
        allBestResult.append(int(evaluation_rastrigin(bestResult)*100)/100.0)
        print('The result is: %f' % allBestResult[-1])
        print()
    print("From the beginning to the end, all the best results are:")
    print(allBestResult)

