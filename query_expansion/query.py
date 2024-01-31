import nltk
import re
from nltk.corpus import stopwords
from query_expansion.utils import Utils



nltk.download('stopwords')


LANGUAGES = {
    "fr": "french",
    "en": "english"
}


class Query:
    def __init__(self, query, index, documents, path=".", file="results.json", lang='fr') -> None:
        '''
        Initialize a Query object.

        Parameters:
        - query (str): The input query text.
        - index (dict): The index containing token information.
        - documents (dict): A dictionary of documents with their titles and URLs.
        - path (str): The directory path for exporting the result file.
        - file (str): The name of the result file.
        - lang (str): The language code for stop words.

        Returns:
        - None
        '''
        self.query = query
        self.index = index
        self.documents = documents
        self.stop_words = stopwords.words(LANGUAGES[lang])
        self.pattern = re.compile(r'([؟!\?]+|[:\.،؛»\]\)\}"«\[\(\{])')
        self.tokens = []
        self.path = path
        self.file = file

    def tokenize_query(self):
        '''
        Tokenizes the query and removes stop words.

        Returns:
        - None
        '''
        text = self.pattern.sub(
            r' \1 ', self.query.replace('\n', ' ').replace('\t', ' '))
        self.tokens = [
            word.lower() for word in text.split(' ') if word not in self.stop_words
        ]

    def find_token_in_document(self):
        '''
        Finds documents containing the query tokens in the index.

        Returns:
        - None
        '''
        documents_ids = []
        documents = {}
        for token in self.tokens:
            if token in self.index.keys():
                for document_id in self.index[token].keys():
                    documents_ids.append(document_id)
                    documents[token] = self.index[token]
        if documents:
            self.found_documents = documents
        else:
            self.found_documents = None

    def rank_documents_from_index(self):
        '''
        Ranks documents based on the count of query tokens in the index.

        Returns:
        - None
        '''
        ranked_documents = {}
        for token in self.found_documents:
            for document in self.found_documents[token]:
                if document in ranked_documents:
                    ranked_documents[document] += self.found_documents[token][document]['count']
                else:
                    ranked_documents[document] = self.found_documents[token][document]['count']
        self.ranked_documents = dict(
            sorted(ranked_documents.items(), key=lambda item: item[1], reverse=True))

    def get_documents_from_ranking(self):
        '''
        Extracts document titles and URLs from the ranked documents.

        Returns:
        - None
        '''
        result = []
        for document in self.ranked_documents:
            result.append(
                {
                    'title': self.documents[int(document)]['title'],
                    'url': self.documents[int(document)]['url']
                }
            )
        result.append(
            {
                'infos': {
                    'nb_docs': len(self.documents),
                    'nb_filtered_docs': len(result)
                }
            }
        )
        self.result = result

    def export_ranking(self):
        '''
        Exports the ranked documents to a JSON file.

        Returns:
        - None
        '''
        Utils().write_json_file(path=self.path, file=self.file, result=self.result)

    def rank(self):
        '''
        Performs the entire process of querying, ranking, and exporting.

        Returns:
        - None
        '''
        self.tokenize_query()
        self.find_token_in_document()
        self.rank_documents_from_index()
        self.get_documents_from_ranking()
        self.export_ranking()
