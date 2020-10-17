from neo4j import GraphDatabase

class PaperNetApp:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
            

    def populate_paper(self):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(self._populate_papers)
            return result

    @staticmethod
    def _populate_papers(tx):
        query = (
            '''
            LOAD CSV WITH HEADERS FROM "https://www.dropbox.com/s/q1vjcik6dayqezx/output.csv?dl=1" AS row
            MERGE (p:Paper { title: row.title, id: row.id,submitter: row.submitter, authors: row.authors_parsed, \
                comments: coalesce(row.comments, "Unknown"), \
                journal_ref: coalesce(row.journal_ref, "Unknown"), doi: coalesce(row.doi, "Unknown"), \
                abstract: row.abstract, categories: coalesce(row.categories, "Unknown")})
            '''
        )
        result = tx.run(query)
        return result


        #  first_upload_date: $first_upload_date, update_date: $update_date })


    # Creating the paper nodes
    def create_paper(self, paper_info):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(self._create_and_return_paper, paper_info)
            return result

    @staticmethod
    def _create_and_return_paper(tx, paper_info):
        query = (
            "CREATE (p:Paper { id: $id, \
                submitter: $submitter, authors: $authors, \
                title: $title, comments: $comments, \
                journal_ref: $journal_ref, doi: $doi \
                abstract: $abstract, categories: $categories, \
                first_upload_date: $first_upload_date, update_date: $update_date })"
            "RETURN p"
        )
        result = tx.run(query, id=paper_info.id, submitter = paper_info.submitter, authors = paper_info.authors, title = paper_info.title, \
                comments = paper_info.comments, journal_ref = paper_info.journal_ref,  doi = paper_info.doi, abstract =  paper_info.abstract, \
                categories = paper_info.categories, first_upload_date = paper_info.first_upload_date, update_date = paper_info.update_date)
        return result


    # Creating the citations connections
    def create_paper_citation(self, paper, papers_cited):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_citation, paper, papers_cited)
            # for record in result:
            #     print("Created citation between: {p1}, {p2}".format(
            #         p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_citation(tx, paper, papers_cited):
        # TODO: Create citation relationship between the paper and each of the papers_cited
        pass
    

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

    # def find_papers_citatons(self, paper_name):
    #      with self.driver.session() as session:
    #         result = session.read_transaction(self._find_and_return_papers_citations, paper_name)
    #         for record in result:
    #             print("Found paper: {record}".format(record=record))

    # @staticmethod
    # def _find_and_return_papers_citations(tx, paper_name): 
    #      query = (
    #         "MATCH (p1:Paper {title: $paper_name})-[:CITED]->(p2:Paper)"
    #         "RETURN p2.name AS name"
    #     )
    #     result = tx.run(query, paper_name=paper_name)
    #     return [record["name"] for record in result]
        
    


    

    # def print_greeting(self, message):
    #     with self.driver.session() as session:
    #         greeting = session.write_transaction(self._create_and_return_greeting, message)
    #         print(greeting)

    # @staticmethod
    # def _create_and_return_greeting(tx, message):
    #     result = tx.run("CREATE (a:Greeting) "
    #                     "SET a.message = $message "
    #                     "RETURN a.message + ', from node ' + id(a)", message=message)
    #     return result.single()[0]



paper = PaperNetApp("neo4j://104.198.183.32", "neo4j", "tSgiHA1DN9R98PeM")
paper.populate_paper()
paper.close()