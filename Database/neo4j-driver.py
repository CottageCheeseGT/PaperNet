from neo4j import GraphDatabase

class PaperNetApp:
	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))
		

	def close(self):
		# Don't forget to close the driver connection when you are finished with it
		self.driver.close()
			

	def populate_paper(self, index):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(self._populate_papers, index=index)
			return result

	@staticmethod
	    def _populate_papers(tx, index):
		# for i in range(index,index+5000,1000):
		query = (
		    '''
		    LOAD CSV WITH HEADERS FROM "https://www.dropbox.com/s/bzevrkg5yfspf7h/output.csv?dl=1" AS row
		    WITH row SKIP $i LIMIT 1000
		    MERGE (p:Paper { title: row.title, id: row.id,submitter: row.submitter, \
			comments: coalesce(row.comments, "Unknown"), \
			doi: coalesce(row.doi, "Unknown"), versions:row.versions})
		    WITH p, row
		    UNWIND split(coalesce(row.categories, "Unknown"), ' ') AS category
		    MERGE (c:Category {name: category})
		    MERGE (c)-[r:CONTAINS]->(p)
		    WITH p, row
		    MERGE (j:Journal {name:coalesce(row.journal_ref, "Unknown")})
		    MERGE (j)-[pub:PUBLISHED_IN]->(p)
		    WITH p, row
		    UNWIND split(row.authors_parsed, ':') AS author
		    MERGE (a:Author {name: author})
		    MERGE (a)<-[w:WRITTEN]->(p)
		    ''')
		print(i)
		result = tx.run(query, i=index)
		return result

		#  first_upload_date: $first_upload_date, update_date: $update_date })


	# # Creating the paper nodes
	# def create_paper(self, paper_info):
	# 	with self.driver.session() as session:
	# 		# Write transactions allow the driver to handle retries and transient errors
	# 		result = session.write_transaction(self._create_and_return_paper, paper_info)
	# 		return result

	# @staticmethod
	# def _create_and_return_paper(tx, paper_info):
	# 	query = (
	# 		"CREATE (p:Paper { id: $id, \
	# 			submitter: $submitter, authors: $authors, \
	# 			title: $title, comments: $comments, \
	# 			journal_ref: $journal_ref, doi: $doi \
	# 			abstract: $abstract, categories: $categories, \
	# 			first_upload_date: $first_upload_date, update_date: $update_date })"
	# 		"RETURN p"
	# 	)
	# 	result = tx.run(query, id=paper_info.id, submitter = paper_info.submitter, authors = paper_info.authors, title = paper_info.title, \
	# 			comments = paper_info.comments, journal_ref = paper_info.journal_ref,  doi = paper_info.doi, abstract =  paper_info.abstract, \
	# 			categories = paper_info.categories, first_upload_date = paper_info.first_upload_date, update_date = paper_info.update_date)
	# 	return result


	# Creating the citations connections
	def create_paper_citation(self):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			with open("test_output.txt") as file:
				for line in file:
					paper = line[:line.find(':') - 6]
					cited_papers = line[line.find('[')+1:-1]
					cited_papers = cited_papers.replace("\'", "")
					print(paper, cited_papers)
					# result = session.write_transaction(self._create_and_return_citation, paper, cited_papers)

	@staticmethod
	def _create_and_return_citation(tx, paper, papers_cited):
		# TODO: Create citation relationship between the paper and each of the papers_cited
		query = (
			'''
			WITH $papers_cited as y
			UNWIND split(y, ',') AS x
			MERGE (p {id: $paper})-[:CITED]->(m {id: x})
			'''
		)
		result = tx.run(query, paper=paper, papers_cited=papers_cited)
		return result
	

	def find_paper(self, paper_name):
		with self.driver.session() as session:
			result = session.read_transaction(self._find_and_return_paper, paper_name)
			for record in result:
				print("Found paper: {record}".format(record=record))

	@staticmethod
	def _find_and_return_paper(tx, paper_name): 
		query = (
			"MATCH (p:Paper) "
			"WHERE p.name = $paper_name "
			"RETURN p.name AS name"
		)
		result = tx.run(query, paper_name=paper_name)
		return [record["name"] for record in result]
		

# for i in range(0, 251000, 1000):
# 	paper = PaperNetApp("neo4j://104.198.183.32", "neo4j", "tSgiHA1DN9R98PeM")
# 	paper.populate_paper(index=i)
# 	paper.close()

paper = PaperNetApp("neo4j://104.198.183.32", "neo4j", "tSgiHA1DN9R98PeM")
paper.create_paper_citation()
