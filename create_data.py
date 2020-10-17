import json
import re
# id: ArXiv ID (can be used to access the paper, see below)
# submitter: Who submitted the paper
# authors: Authors of the paper
# title: Title of the paper
# comments: Additional info, such as number of pages and figures
# journal-ref: Information about the journal the paper was published in
# doi: [https://www.doi.org](Digital Object Identifier)
# abstract: The abstract of the paper
# categories: Categories / tags in the ArXiv system
# first_upload_date
# update_date, 

with open("/mnt/c/Users/Joshua Engels/Downloads/arxiv-metadata-oai-snapshot.json", "r") as input, open("output.csv", "w") as output:
        while True:
                line = input.readline()
                if (line == "" ):
                        break
                parsed = json.loads(line)
                if parsed["categories"].startswith("cs"):
                        fields = ["id", "submitter", "authors", "title", "comments", "journal-ref", "abstract", "categories"]
                        results = []
                        for field in fields:
                                so_far = parsed[field]
                                if so_far == None:
                                        results.append("")
                                else:
                                        so_far = re.sub("\\n[.!?\\-]", "", so_far)
                                        so_far = re.sub("\\n", " ", so_far)
                                        so_far = re.sub(' +',' ',so_far)
                                        so_far = so_far.strip()
                                        so_far = "\"" + so_far + "\""
                                        results.append(so_far)
                        output.write(",".join(results) + "\n")
