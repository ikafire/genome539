import csv
import itertools
import numpy as np
import random

ngram_count = {}

SCORING = { 2: 1, 3: 6, 4: 20 }
RANGE = np.arange(39) + 1
GROUP_SIZE = 4
POPULATION = 100
ELITE_COUNT = 5
GENERATIONS = 1000
MUTATION_RATE = 0.1

def main():
    with open('history.csv') as csvfile:
        history = np.genfromtxt(csvfile, delimiter='\t')
        for row in history:
            update_ngrams(row)
    #write_ngrams()

    population = init_population()
    for i in range(GENERATIONS):
        population = next_generation(population)
        print(len(population))

    print('final elites:')
    fitnesses = np.array([get_solution_fitness(s) for s in population])
    elites = select_elites(population, fitnesses)
    for elite in elites:
        print(f'score: {1/get_solution_fitness(elite)}, {elite}')


def next_generation(population):
    fitnesses = np.array([get_solution_fitness(s) for s in population])
    elites = select_elites(population, fitnesses)

    scores = 1 / fitnesses
    print(f'avg score: {np.average(scores)}, min score: {np.min(scores)}, elite scores: {[1/get_solution_fitness(e) for e in elites]}')

    mating_pool = select_mating_pool(population, fitnesses)
    children = breed_many(mating_pool, len(mating_pool) - len(elites))
    return elites + list(mutate(children))


def init_population():
    return [np.random.permutation(RANGE) for i in range(POPULATION)]


def select_mating_pool(population, fitnesses):
    selection_board = np.cumsum(fitnesses) / np.sum(fitnesses)
    mating_pool = []
    for _ in range(len(population)):
        dart = random.random()
        for i, target in enumerate(selection_board):
            if dart <= target:
                mating_pool.append(population[i])
                break
    return mating_pool


def select_elites(population, fitnesses):
    rank = np.argsort(-fitnesses)
    return [population[i] for i in rank[:ELITE_COUNT]]


def breed_many(mating_pool, breed_count):
    sampling = random.sample(mating_pool, breed_count)
    for i in range(len(sampling)):
        yield breed(sampling[i], sampling[-(i+1)])


def breed(p1, p2):
    # order 1 crossover
    # select slice of p1 and apply it on p2
    gene1 = random.randint(0, len(p1) - 1)
    gene2 = random.randint(0, len(p1) - 1)

    start = min(gene1, gene2)
    end = max(gene1, gene2)

    slice = p1[start:end+1]
    rest = [x for x in p2 if x not in slice]
    return np.concatenate([rest[:start], slice, rest[start:]])


def mutate(population):
    for gene in population:
        mutate = random.random()
        mutated = np.copy(gene)
        if mutate < MUTATION_RATE:
            x = random.randint(0, len(gene)-1)
            y = random.randint(0, len(gene)-1)
            temp = mutated[x]
            mutated[x] = mutated[y]
            mutated[y] = temp
        yield mutated


def update_ngrams(row):
    for n in range(1, 5):
        for t in itertools.combinations(row, n):
            t = frozenset(t)
            c = ngram_count.get(t, 0)
            ngram_count[t] = c + 1


def write_ngrams():
    with open('ngram.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        for k, v in sorted(ngram_count.items(), key=lambda x : (len(x[0]), x)):
            writer.writerow([k, v])


def get_solution_fitness(solution):
    score = 0
    for i in range(0, len(RANGE), GROUP_SIZE):
        score += get_group_score(solution[i:i+GROUP_SIZE])
    return 1 / score


def get_group_score(group):
    score = 0
    for n in range(2, 5):
        for t in itertools.combinations(group, n):
            t = frozenset(t)
            count = ngram_count.get(t, 0)
            score = score + SCORING[n] * count

    return score


if __name__ == '__main__':
    main()
