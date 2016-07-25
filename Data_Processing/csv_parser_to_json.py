import csv
import json

def csv_to_json(csv_file_path,json_file):

    with open(csv_file_path, "rb") as f:
        reader = csv.reader(f)
        i = reader.next()
        rest = [row for row in reader]

    csvfile = open(csv_file_path, 'r')
    jsonfile = open(json_file, 'w')

    fieldnames = i
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n,')



csv_to_json('liquor_lic.csv','liquor_lic.json')
