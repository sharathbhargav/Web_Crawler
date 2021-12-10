import math

from SE.UtilityFunctions import CommonHelpers

import os,pathlib
class TF_IDF:
    def __init__(self):
        pass
    def load_docs(self,doc_list):
        self.cleaned_words=doc_list

    def calcIDF(self, total_number_of_docs):
        """
        Function that calculates the inverse document frequency of each of the terms in vocab
        """
        self.doc_idf = {}
        for each in self.inverted_index:
            self.doc_idf[each] = math.log(
                (total_number_of_docs/len(self.inverted_index[each])))

    def generate_inverted_index(self):
        """
        Function to map each term in vocab to all documents it occurs in coupled with the number of occurrences in each document.
        """
        self.inverted_index = {}
        cleaned_words_dict = dict(
            sorted(self.cleaned_words.items(), key=lambda item: item[0]))  # sort the <Document,[words]> pair by document id
        for key in list(cleaned_words_dict.keys()):
            # sort the word list of each document
            word_list = sorted(cleaned_words_dict[key])
            for each_word in word_list:
                if each_word in self.inverted_index:  # Check if inverted index has already been constructed for the given term
                    individual_index = self.inverted_index[each_word]
                    if key in individual_index:  # Check if the current document has already been added to the inverted index of term
                        count = individual_index[key]
                        # increase the term frequency by 1
                        individual_index[key] = count+1
                    else:
                        # add the document to the term index and set term frequency as 1
                        individual_index[key] = 1
                    self.inverted_index[each_word] = individual_index
                else:
                    # add the term to inverted index and add the document to the term index
                    self.inverted_index[each_word] = {key: 1}

        # Once the entire inverted index is generated calculate inverted document frequency for each of the terms
        self.calcIDF(len(cleaned_words_dict))
        CommonHelpers.dump_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/individual_index.pickle"), self.inverted_index)
        CommonHelpers.dump_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/doc_idf.pickle"), self.doc_idf)


    def calculate_doc_length(self):
        """
        Calculate the normalized document vector magnitude by summing the squares of weights of each of the term. In this case weights is tf*idf of the term
        """
        self.doc_length = {}
        for key in self.cleaned_words:
            word_list = self.cleaned_words[key]
            sq_sum = 0
            for each_word in word_list:
                index_obj = self.inverted_index[each_word]
                idf = self.doc_idf[each_word]
                tf = index_obj[key]
                sq_sum = sq_sum + (tf*idf)**2
            self.doc_length[key] = math.sqrt(sq_sum)

        CommonHelpers.dump_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/doc_length.pickle"), self.doc_length)

    def init_data_from_pickle(self):
        self.inverted_index = CommonHelpers.load_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/individual_index.pickle"))
        self.doc_idf = CommonHelpers.load_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/doc_idf.pickle"))
        self.doc_length = CommonHelpers.load_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/doc_length.pickle"))

    def query_similarity(self, query):
        """
        Given a query string, calculate the similarity with all documents whose words intersect with the terms in query. Similarity is cosine distance of query vector and document vector
        """
        doc_set = set()
        # Find the subset of documents whose words overlap with that of query given
        for each_query_word in query:
            if each_query_word in self.inverted_index:
                index_obj = self.inverted_index[each_query_word]
                doc_list = index_obj.keys()
                doc_list = list(doc_list)
                doc_set.update(doc_list)
        doc_scores = {}
        for doc in doc_set:
            doc_len = self.doc_length[doc]
            s = 0
            for each_word in query:
                if each_word in self.inverted_index:
                    index_obj = self.inverted_index[each_word]
                    if doc in index_obj:
                        tf = index_obj[doc]
                        idf = self.doc_idf[each_word]
                        s = s + tf*idf*idf  # Dot product

            cos = s/doc_len  # normalize dot product
            doc_scores[doc] = cos
            
        doc_scores = dict(
            sorted(doc_scores.items(), key=lambda item: item[1], reverse=True))
        return doc_scores

    def get_tf_idf_score(self,word,doc_id):
        index_obj = self.inverted_index[word]
        tf = index_obj[doc_id]
        idf = self.doc_idf[word]
        return tf*idf