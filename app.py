import csv
import itertools
import numpy as np

ngram_count = {}

SCORING = { 2: 1, 3: 6, 4: 20 }

def main():
    with open('history.csv') as csvfile:
        history = np.genfromtxt(csvfile, delimiter='\t')
        for row in history:
            update_ngrams(row)

    #write_ngrams()

    print(get_score((36,38,5)))
    print(get_score((15,21,39,26)))
    print(get_score((12,24,13,1)))
    print(get_score((10,31,8,6)))
    print(get_score((19,35,7,27)))
    print(get_score((30,32,33,17)))
    print(get_score((11,18,2,16)))
    print(get_score((4,14,22,37)))
    print(get_score((3,25,29,20)))
    print(get_score((9,28,23,34)))

def update_ngrams(row):
    for n in range(1, 5):
        for t in itertools.combinations(row, n):
            c = ngram_count.get(t, 0)
            ngram_count[t] = c + 1


def write_ngrams():
    with open('ngram.csv', 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        for k, v in sorted(ngram_count.items(), key=lambda x : (len(x[0]), x)):
            writer.writerow([k, v])


def get_score(series):
    score = 0
    for n in range(2, 5):
        for t in itertools.combinations(series, n):
            count = ngram_count.get(t, 0)
            if count:
                print((t, ngram_count[t]))
            score = score + SCORING[n] * count

    return score



if __name__ == '__main__':
    main()
