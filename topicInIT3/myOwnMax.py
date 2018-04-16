from random import random, shuffle, randint, choice
import matplotlib.pyplot as plt
fig = plt.gcf()
fig.set_size_inches(18, 6)

LENGTH = 192  # DNA's length
N = 100 # population
Mprob = 0.05
Cprob = 0.95
Iterations = 100

def rand_idx(N) : return randint(0, N-1)


def coin(p=0.5) : return 1 if (random() < p) else 0
def random_individual(LENGTH):
    return [coin() for i in range(LENGTH)]
def initial_population(N, LENGTH):
    return [random_individual(LENGTH) for i in range(N)]


def fitness(c):return sum(c)


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
        temp3 = temp if fitness(temp) > fitness(temp2) else temp2
        newPopulation.append(temp3)
    newPopulation[1] = eliteInd
    updateGlobleElite(newPopulation)
    return newPopulation

# def crossover(population):
#     newPopulation = []
#     for i in range(N / 2):
#         c1 = sampleOne = population[2*i]
#         c2 = sampleTwo = population[2*i+1]
#         if random() < Cprob:
#             for j in range(LENGTH):
#                 if random() < 0.8:
#                     c1[j], c2[j] = c2[j], c1[j]
#         newPopulation.append(c1)
#         newPopulation.append(c2)
#     return newPopulation
def crossover(population):
    newPopulation = []
    k = rand_idx(LENGTH)
    for i in range(N / 2):
        nc1 = c1 = population[2*i]
        nc2 = c2 = population[2*i+1]
        if random() < Cprob:
            nc1 = c1[:k] + c2[k:]
            nc2 = c2[:k] + c1[k:]
        newPopulation.append(nc1)
        newPopulation.append(nc2)
    return newPopulation


def mutation(population):
    for i in range(N):
        if coin(Mprob) :
            k = rand_idx(LENGTH)
            population[i][k] = 1 - population[i][k]
    return population


def check_stop(fitness_population):
    # summer = 0
    # for i in fitness_population:
    #     summer += fitness(i)
    # if (summer / (LENGTH * N) > 0.95) or (echo > Iterations):
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
    # print 'The echo is: %d' % (echo)
    maxFitness = 0
    for i in population:
        if maxFitness < fitness(i):
            maxFitness = fitness(i)
    graphData.append(maxFitness)
    # print 'The max is: %f' % (maxFitness)
    # print ''


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
    print graphData

def plotGraph(graphData, label):
    index = []
    for i,j in enumerate(graphData):
        index.append(i)
    print len(index)
    print len(graphData)
    return plt.plot(index, graphData, label = label)

if __name__ == '__main__':
    # LENGTH = 192
    # Mprob = 0.05
    # Cprob = 0.95
    # Iterations = 100
    # N = 100
    graphData_1 = []
    Mprob = 0.00
    run(graphData_1)

    graphData_2 = []
    Mprob = 0.01
    run(graphData_2)

    graphData_3 = []
    Mprob = 0.05
    run(graphData_3)

    graphData_4 = []
    Mprob = 0.50
    run(graphData_4)

    graphData_5 = []
    Mprob = 1.00
    run(graphData_5)

    plot1 = plotGraph(graphData_1, 'Mprob = 0.00')
    plot2 = plotGraph(graphData_2, 'Mprob = 0.01')
    plot3 = plotGraph(graphData_3, 'Mprob = 0.05')
    plot4 = plotGraph(graphData_4, 'Mprob = 0.50')
    plot4 = plotGraph(graphData_5, 'Mprob = 1.00')
    plt.xlabel('Para = (LENGTH:192, Iteration:100, N:100, Cprob:0.95)')
    plt.ylabel('Best fitness')
    plt.legend(loc = 'upper left')
    fig.savefig('fig/Mutation.png', dpi=100)
    # plt.show()





