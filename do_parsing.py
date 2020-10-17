import os
import subprocess
import csv
import pandas as pd
import json


TOTAL_ROWS = 250000
df = pd.read_csv('output.csv',nrows=TOTAL_ROWS,low_memory=False)

def fill_in_later(file_name):
        result = subprocess.run(['anystyle', 'find', file_name], stdout=subprocess.PIPE)
        refs = json.loads(result.stdout)
        ref_ids = []
        ref_title_list = [x['title'][0] for x in refs if 'title' in x]
                for ret_title in ref_title_list
                        ref_ids.append(str(df.loc[df.title == title_name].id.values.item())) 

# ids = []
# with open('output.csv', newline='') as base_data:
#         base_data_reader = csv.reader(base_data, delimiter=',', quotechar='"')
#         for line in base_data_reader:
#                 if line[0] != "id":
#                         ids.append(line[0])



batch_size = 10
result = subprocess.run(['wc', '-l', 'ids'], stdout=subprocess.PIPE)
total_size = int(result.stdout.decode('utf-8').split(" ")[0])
with open("connections", "w") as connections_file:
        for start in range(0, total_size, batch_size):
                os.system('rm -r papers/*')
                end = min(start + batch_size, total_size)
                print(start, end)
                os.system(f"awk 'FNR>={start} && FNR<{end}' ids | gsutil -m cp -I papers")  
                
                result = subprocess.run(['ls', 'papers/'], stdout=subprocess.PIPE)
                files = result.stdout.decode('utf-8').split("\n")
                for i in range(len(files)):
                        if files[i].strip() == "":
                                files = files[:i] + files[i + 1:]
                
                index = 0
                while index < len(files):
                        current = files[index]
                        while index + 1 < len(files) and int(current[-5]) < int(files[index + 1][-5]):
                                index += 1
                                current = files[index]
                        index += 1

                        citations = fill_in_later("papers/" + current)
                        connections_file.write(f"{current}: {citations}\n")
