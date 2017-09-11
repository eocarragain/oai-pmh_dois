import os
import csv
import pandas as pd
base_dir = 'cache'
print(len(os.listdir(base_dir)))

harvested_counts = []

with open('overall_counts.csv', 'w') as csvfile:
    fieldnames = ['org', 'count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for dirname in os.listdir(base_dir):
        org_dir = "{0}/{1}".format(base_dir, dirname)
        org_count = len(os.listdir(org_dir))
        writer.writerow({"org": dirname, "count": org_count})
        harvested_counts.append({"org": dirname, "count": org_count})

df_harvested = pd.DataFrame(harvested_counts)
print(df_harvested)

df_dois_all = pd.read_csv('output.csv')
df_dois = df_dois_all.groupby(['org']).size().to_frame("count").reset_index()
df_dois = df_dois.rename(columns = {'count':'doi_count'})

dfs_merged = pd.merge(df_harvested, df_dois, on='org', how='inner')
dfs_merged = dfs_merged[['org', 'count', 'doi_count']].sort_values(['org'])
print(dfs_merged)
dfs_merged.to_csv('output_merged.csv')
