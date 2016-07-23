import csv


outputFile = open('output.csv', 'w')
outputWriter = csv.writer(outputFile)

with open("/Users/michael/Desktop/Denver_Clustering/sales.csv", "rb") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        if i > 0:
            outputWriter.writerow(line)
outputFile.close()
