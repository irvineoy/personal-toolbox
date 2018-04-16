
----------------------------------------------------------------------
Schedule :
    * week_07 : I'll check your progress on your GA project (bring your PC!)
    * week_14 : You'll send me all your program (source code + executable + results + report)
    * week_15 : You'll give a presentation (10min / PPT) about your GA project
----------------------------------------------------------------------
    
----------------------------------------------------------------------
Genetic Algorithms Project (Milestones) :
--------------------------

Problems :
    * MAXONE problem (see your slides from week_02 / week_03) (easy)
    * Function Optimization : y=cos(x-1)*cos(2*x) ; x e [-4, 4]
    * Travel Salesman Problem (TSP) : http://www.lalena.com/ai/ts
    * Image Restoration (see Image_Restoration_Project.pdf)

Input Parameters :
    * prob_crossover    <- [0, 1]
    * prob_mutation     <- [0, 1]
    * iterations_limit  <- ex 2000
    * population_size   <- ex 200

Functions :   
    * random_individual(n)          -> generate a random individuals of length 'n'
    * initial_population(N)         -> population of 'N' random individuals
    * fitness(c)                    -> fitness value of 'c' (the closer to the solution the better)
    * selection(fitness_population) -> new population (select best parents)
    * crossover(c1, c2)             -> c12, c21 (combine the chromosomes to yield two new children)
    * mutation(c)                   -> c1 (randomly mutate parts/bits of the chromosome)
    * check_stop(fitness_population)-> stop run if true
      
    # REF: https://gist.github.com/bellbind/741853
    # REF: http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
    def run():
        n = population_size
        population = initial_population(n)
        while True:
            fits_pops = [(fitness(ch),  ch) for ch in population]
            if check_stop(fits_pops): break
            population = breed_population(fits_pops)
        return population
          
    def breed_population(fitness_population):
        parent_pairs = select_parents(fitness_population)
        size = len(parent_pairs)
        next_population = []
        for k in range(size) :
            parents = parent_pairs[k]
            cross = random() < prob_crossover
            children = crossover(parents) if cross else parents
            for ch in children:
                mutate = random() < prob_mutation
                next_population.append(mutation(ch) if mutate else ch)
        return next_population
----------------------------------------------------------------------
