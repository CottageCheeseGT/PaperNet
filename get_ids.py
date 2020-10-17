import csv
with open('output.csv', newline='') as csvfile, open("ids", "w") as output:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in reader:
			identifier = row[0]
			if identifier.startswith("id"):
				continue
			elif identifier.startswith("cs"):
				cs, number = identifier.split("/")
				output.write(f"gs://arxiv-dataset/arxiv/cs/pdf/{number[:4]}/{number}*" + "\n")
				pass
			else:
				first, second = identifier.split(".")
				output.write(f"gs://arxiv-dataset/arxiv/arxiv/pdf/{first}/{first}.{second}*" + "\n")
			
