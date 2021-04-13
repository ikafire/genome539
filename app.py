import csv
import itertools

history = []
ngram_count = {}

def main():
    with open('history.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            numeric_row = [int(x) for x in row]
            history.append(numeric_row)
            update_ngrams(numeric_row)

    write_ngrams()

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


if __name__ == '__main__':
    main()
