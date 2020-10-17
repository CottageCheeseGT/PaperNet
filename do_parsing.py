import os
import subprocess
import csv
import pandas as pd
import json
import re

result = subprocess.run(['wc', '-l', 'ids'], stdout=subprocess.PIPE)
total_size = int(result.stdout.decode('utf-8').split(" ")[0])
df = pd.read_csv('output.csv',nrows=total_size,low_memory=False)
df['title'] = df['title'].apply(lambda name: re.sub("[^a-zA-Z]", "", name).lower().strip())

import sys
folder = sys.argv[1]
start_here = int(sys.argv[2])
stop_here = int(sys.argv[3])
output_file = sys.argv[4]


def fill_in_later(file_name):
	result = subprocess.run(['anystyle', 'find', file_name], stdout=subprocess.PIPE)
	if len(result.stdout.decode('utf-8')) == 0:
		return []
	refs = json.loads(result.stdout)
	ref_ids = []
	ref_title_list = [x['title'][0] for x in refs if 'title' in x]
	for ref_title in ref_title_list:
		ref_title = re.sub("[^a-zA-Z]", "", ref_title).lower().strip()
		if len(df.loc[df.title == ref_title]) == 1:
			ref_ids.append(str(df.loc[df.title == ref_title].id.values.item())) 
	return ref_ids


batch_size = 100
with open(output_file, "w") as connections_file:
	for start in range(start_here, min(total_size, stop_here), batch_size):
		os.system(f'rm -r {folder}/*')
		end = min(start + batch_size, total_size)
		os.system(f"awk 'FNR>={start} && FNR<{end}' ids | gsutil -m cp -I {folder}")  
		
		result = subprocess.run(['ls', f'{folder}/'], stdout=subprocess.PIPE)
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

			citations = fill_in_later(folder + "/" + current)
			connections_file.write(f"{current}: {citations}\n")
			connections_file.flush()
