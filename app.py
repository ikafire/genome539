import csv
import itertools
import numpy as np
import random

ngram_count = {}

SCORING = { 2: 1, 3: 6, 4: 20 }
RANGE = np.arange(39) + 1
GROUP_SIZE = 4
POPULATION = 100
GENERATIONS = 100

def main():
    with open('history.csv') as csvfile:
        history = np.genfromtxt(csvfile, delimiter='\t')
        for row in history:
            update_ngrams(row)
    #write_ngrams()

    population = init_population()
    print(population)
    for i in range(GENERATIONS):
        population = next_generation(population)
        #print(population)


def next_generation(population):
    fitnesses = np.array([get_solution_fitness(s) for s in population])
    scores = 1 / fitnesses
    print(f'avg score: {np.average(scores)}, min score: {np.min(scores)}')
    #print(f'min score: {1/np.max(fitnesses)}')
    mating_pool = select_mating_pool(population, fitnesses)
    return breed_population(mating_pool)


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


def breed_population(mating_pool):
    new_population = []
    for gene in mating_pool:
        mutate = random.random()
        child = np.copy(gene)
        if mutate > 0.1:
            x = random.randint(0, 38)
            y = random.randint(0, 38)
            temp = child[x]
            child[x] = child[y]
            child[y] = temp
        new_population.append(child)
    return new_population


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
