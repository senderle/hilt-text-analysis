import sys
import os
import csv
import features3200
import features1600
import features800
import features400
import featuresweka

def dedupe(seq):
    seen = set()
    newseq = []
    for s in seq:
        s = clean(s)
        if s not in seen:
            seen.add(s)
            newseq.append(s)
    return newseq

def clean(s):
    return s.strip().upper().replace("'", '_').replace('"', '_')

with open(sys.argv[1]) as f:
    csvlines = [list(r) for r in csv.reader(f, delimiter=',')]

features = (featuresweka.features if len(sys.argv) < 3 else
            features3200.features if sys.argv[2] == '3200' else
            features1600.features if sys.argv[2] == '1600' else
            features800.features if sys.argv[2] == '800' else
            features400.features if sys.argv[2] == '400' else
            featuresweka.features)

features = dedupe(features)

csvlines[0].extend(features)
newlines = [csvlines[0]]
for line in csvlines[1:]:
    if line[4] == 'addcanon':
        print "skipping"
        continue
    filename = os.path.join('poems', line[0]) + '.poe.tsv'
    with open(filename) as f:
        count = {}
        for l in f:
            r = l.split('\t')
            if len(r) == 2:
                w, c = r
            count[clean(w)] = int(c)
        line.extend(count.get(w, 0) for w in features)
        newlines.append(line)

with open(sys.argv[1][:-4] + '-' + str(len(features)) + '.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerows(newlines)

