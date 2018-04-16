from random import random, shuffle, randint, choice

LENGTH = 192  # DNA's length
N = 300 # population
if 0 :
    LENGTH = 10  # DNA's length
    N = 6 # population
Mprob = 0.05
Cprob = 1.0
GENERATION = 350
eliteInd = []

def rand_idx(N) : return randint(0, N-1)

def random_individual(LENGTH):
    child = []
    for i in range(LENGTH):
        if random() < 0.5:
            child.append(1)
        else:
            child.append(0)
    return child
def coin(p=0.5) : return 1 if (random() < p) else 0
def random_individual(LENGTH): return [coin() for i in range(LENGTH)]

def initial_population(N, LENGTH):
    population = []
    for i in range(N):
        temp = random_individual(LENGTH)
        population.append(temp)
    return population
def initial_population(N, LENGTH): return [random_individual(LENGTH) for i in range(N)]


def fitness(c):
    count = 0
    for i in c:
        if i:
            count = count + 1
    return count
def fitness(c): return sum(c)

def updateGlobleElite(population):
    fitnessList = []
    global eliteInd
    for i in range(N):
        fitnessList.append(fitness(population[i]))
    maxPointer = fitnessList.index(max(fitnessList))
    # if fitness(population[maxPointer]) > fitness(eliteInd):
    eliteInd = population[maxPointer][:]
    return

def selectionIrvine(population):
    # updateGlobleElite(population)
    shuffle(population)
    newPopulation = []
    fitnessList = []
    for i in range(N):
        temp = population[rand_idx(2*N)]
        temp2 = population[rand_idx(2*N)]
        if fitness(temp) > fitness(temp2):
            newPopulation.append(temp)
            fitnessList.append(fitness(temp))
        else:
            newPopulation.append(temp2)
            fitnessList.append(fitness(temp2))
    minPointer = fitnessList.index(min(fitnessList))
    newPopulation[minPointer] = eliteInd
    updateGlobleElite(newPopulation)
    return newPopulation

def selection(population):
    newPopulation = []
    for k in range(N) :
        c1 = choice(population)
        c2 = choice(population)
        c12 = c1
        if fitness(c1) < fitness(c2) : c12 = c2
        newPopulation.append(c12)
    return newPopulation

def rouletteSelection(population):
    shuffle(population)
    compress = []
    summer = 0
    newPopulation = []
    fitnessList = []
    for i in population:
        compress.append(fitness(i))
        summer += fitness(i)
    for i in range(2*N):
        compress[i] = float(compress[i]) / summer
    for i in range(N):
        pointer = random()
        summer_temp = 0
        selectNum = -1
        while (pointer > summer_temp):
            selectNum += 1
            summer_temp += compress[selectNum]
        newPopulation.append(population[selectNum])
        fitnessList.append(fitness(population[selectNum]))
    minPointer = fitnessList.index(min(fitnessList))
    newPopulation[minPointer] = eliteInd
    updateGlobleElite(newPopulation)
    return newPopulation


def crossoverIrvine(population):
    shuffle(population)
    newPopulation = []
    for i in range(N / 2):
        c1 = sampleOne = population[2*i]
        c2 = sampleTwo = population[2*i+1]
        if random() < Cprob:
            k = rand_idx(LENGTH)
            c1 = sampleOne[:k] + sampleTwo[k:]
            c2 = sampleTwo[:k] + sampleOne[k:]
        newPopulation.append(c1)
        newPopulation.append(c2)
    return newPopulation
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

def mutationIrvine(population):
    for i in range(N):
        for j in range(LENGTH):
            if random() < Mprob:
                population[i][j] = 1 - population[i][j]
    return population
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
    # if (summer / (LENGTH * N) > 0.95) or (echo > GENERATION):
    if echo > GENERATION:
        return True
    else:
        return False


def sum_population(fitness_population):
    summerOne = 0
    for i in fitness_population:
        summerOne += fitness(i)
    return summerOne
def sum_population(fitness_population): return sum(map(fitness, fitness_population))


def show(population):
    print 'The echo is: %d' % (echo)
    # for i in population:
    #     print i
    print 'The percentage of sum is: %f' %(sum_population(population) / float(N) / LENGTH)
    maxFitness = 0
    for i in population:
        if maxFitness < fitness(i):
            maxFitness = fitness(i)
    print 'The max is: %f' % (maxFitness)
    print ''
def best_fit(population) :
    fitness_values = map(fitness, population)
    bf = max(fitness_values)
    bf_idx = fitness_values.index(bf)
    return bf, population[bf_idx]
def show(population): print "[G %03d]" % echo, best_fit(population)

def run():
    population = initial_population(N, LENGTH)
    global echo
    global eliteInd
    eliteInd = population[0]
    echo = 0
    while True:
        population = selection(population)
        population = crossoverIrvine(population)
        population = mutation(population)
        show(population)
        echo += 1
        if check_stop(population): break


if __name__ == '__main__':
    run()
