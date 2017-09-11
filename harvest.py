import csv
import os
import re
from lxml import etree
import sickle
from sickle import Sickle
endpoint_file = 'RIAN_endpoints.csv'
output_file = 'output.csv'
base_cache_dir = './cache/'
dc_fields = ['identifier', 'relation', 'source']
doi_regex = re.compile('10.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
cache_mode = 'cache'

if not os.path.exists(base_cache_dir):
    os.makedirs(base_cache_dir)

with open(output_file, 'w') as csvfile:
    fieldnames = ['org', 'identifier']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    with open(endpoint_file, 'r', encoding='utf-8', errors='ignore') as endpoints:
        reader = csv.DictReader(endpoints)

        for row in reader:
            org = row['org']
            base_url = row['base_url']
            metadata_prefix = row['metadataPrefix']
            doi_field = row['doi_field'].replace("dc:", "")
            org_dois = set([])
            print(org)
            save_dir = "{0}/{1}".format(base_cache_dir, org)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            if cache_mode == 'cache':
                print("Loading {0} records from cache".format(org))
                records = []
                for filename in os.listdir(save_dir):
                    if filename.endswith(".xml"):
                        filepath = "{0}/{1}".format(save_dir, filename)
                        try:
                            with open(filepath, 'r') as rawfile:
                                xml = rawfile.read()
                                sickle_record = sickle.models.Record(etree.fromstring(xml))
                                records.append(sickle_record)
                        except:
                            print("Failed to load {0}".format(filename))
            else:
                print("About to connect to {0} OAI endpoint".format(org))
                sickle = Sickle(base_url, max_retries=30)
                records = sickle.ListRecords(metadataPrefix=metadata_prefix, ignore_deleted=True)

            for record in records:
                id = record.header.identifier.replace("oai:", "").replace(":", "-").replace("/", "_")
                print(record.header.identifier)
                if cache_mode != 'cache_mode':
                    with open("./{0}/{1}.xml".format(save_dir, id), 'w') as record_file:
                        record_file.write(record.raw)

                try:
                    for field in dc_fields:
                        if field in record.metadata:
                            for id in record.metadata[field]:
                                if id and "10." in id:
                                    matches = doi_regex.findall(id)
                                    for match in matches:
                                        print(match)
                                        org_dois.add(match)
                                        #writer.writerow({"org": org, "identifier": match})
                except AttributeError:
                    print("skipping as no metdata attribute")

            for doi in org_dois:
                writer.writerow({"org": org, "identifier": doi})
