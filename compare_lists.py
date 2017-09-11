import csv

scopus_file = '/home/eoghan/dev/scopus_exports/combined_csv/combined.csv'
harvested_file = 'output.csv'
scopus_dois = []
harvested_dois = []

def clean_doi(doi):
    doi = doi.strip('\n')
    doi = doi.strip('\r')
    doi = doi.strip()
    return doi

with open(scopus_file, 'r', encoding='utf-8', errors='ignore') as scopus:
    reader = csv.DictReader(scopus)

    for row in reader:
        scopus_doi = clean_doi(row['DOI'])
        scopus_dois.append(scopus_doi)

with open(harvested_file, 'r', encoding='utf-8', errors='ignore') as harvested:
    reader = csv.DictReader(harvested)

    for row in reader:
        harvested_doi = clean_doi(row['identifier'])
        harvested_dois.append(harvested_doi)

scopus_set = set(scopus_dois)
harvested_set = set(harvested_dois)
intersect = scopus_set.intersection(harvested_set)

print("scopus set: {0}".format(len(scopus_set)))
print("harvested set: {0}".format(len(harvested_set)))
print("intersect: {0}".format(len(intersect)))
