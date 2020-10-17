import os
import subprocess
import csv
import pandas as pd
import json

result = subprocess.run(['wc', '-l', 'ids'], stdout=subprocess.PIPE)
total_size = int(result.stdout.decode('utf-8').split(" ")[0])
df = pd.read_csv('output.csv',nrows=total_size,low_memory=False)

def fill_in_later(file_name):
	result = subprocess.run(['anystyle', 'find', file_name], stdout=subprocess.PIPE)
	if len(result.stdout.decode('utf-8')) == 0:
		return []
	refs = json.loads(result.stdout)
	ref_ids = []
	ref_title_list = [x['title'][0] for x in refs if 'title' in x]
	for ref_title in ref_title_list:
		if not df.loc[df.title == ref_title].empty:
			ref_ids.append(str(df.loc[df.title == ref_title].id.values.item())) 
	return ref_ids


batch_size = 100
with open("connections", "w") as connections_file:
	for start in range(100000, total_size, batch_size):
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
			connections_file.flush()
