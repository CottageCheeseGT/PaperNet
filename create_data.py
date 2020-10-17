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

pretty_fields = ["id", "submitter", "authors_parsed", "title", "comments", "journal_ref", "doi", "abstract", "categories"]
fields = ["id", "submitter", "authors_parsed", "title", "comments", "journal-ref", "doi", "abstract", "categories"]
with open("/mnt/c/Users/Joshua Engels/Downloads/arxiv-metadata-oai-snapshot.json", "r") as input, open("output.csv", "w") as output:
        count = 0
        output.write(",".join(pretty_fields) + "\n")
        while True:
                line = input.readline()
                if (line == "" ):
                        break
                parsed = json.loads(line)
                if parsed["categories"].startswith("cs"):
                        results = []
                        for field in fields:
                                so_far = parsed[field]
                                if so_far == None:
                                        so_far = ""
                                else:
                                        if field == "authors_parsed":
                                                so_far = ":".join([" ".join(name[:2] + name[3:]) for name in so_far])
                                        so_far = re.sub("\\r\\n[.!?\\-]", "", so_far)
                                        so_far = re.sub("\\r", " ", so_far)
                                        so_far = re.sub("\\n[.!?\\-]", "", so_far)
                                        so_far = re.sub("\\n", " ", so_far)
                                        so_far = re.sub("\\r[.!?\\-]", "", so_far)
                                        so_far = re.sub("\\r", " ", so_far)
                                        so_far = re.sub("\\r", " ", so_far)
                                        so_far = re.sub("\"", "'", so_far)

                                        
                                        so_far = re.sub(' +',' ',so_far)
                                        so_far = so_far.strip()
                                        so_far = "\"" + so_far + "\""
                                results.append(so_far)

                        count += 1
                        if (count % 1000 == 0):
                                print(count)
                        output.write(",".join(results) + "\n")
