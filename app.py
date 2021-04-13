import csv

history = []
unigram_count = {}
bigram_count = {}
trigram_count = {}
fourgram_count = {}

def main():
    with open('history.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            numeric_row = [int(x) for x in row]
            history.append(numeric_row)
            update_ngrams(numeric_row)

    write_ngrams('unigram.csv', unigram_count)
    write_ngrams('bigram.csv', bigram_count)
    write_ngrams('trigram.csv', trigram_count)
    write_ngrams('fourgram.csv', fourgram_count)


def update_ngrams(row):
    for i in range(5):
        unigram = row[i]
        c = unigram_count.get(unigram, 0)
        unigram_count[unigram] = c + 1

        for j in range(i + 1, 5):
            bigram = (row[i], row[j])
            c = bigram_count.get(bigram, 0)
            bigram_count[bigram] = c + 1

            for k in range(j + 1, 5):
                trigram = (row[i], row[j], row[k])
                c = trigram_count.get(trigram, 0)
                trigram_count[trigram] = c + 1

        fourgram = tuple(row[0:i] + row[i+1:5])
        c = fourgram_count.get(fourgram, 0)
        fourgram_count[fourgram] = c + 1


def write_ngrams(filename, counts):
    with open(filename, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for k, v in sorted(counts.items()):
            writer.writerow([k, v])


if __name__ == '__main__':
    main()
