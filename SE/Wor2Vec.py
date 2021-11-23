from gensim.models import  KeyedVectors
import numpy as np
import Tf_Idf
from scipy import spatial
from UtilityFunctions import PreprocessHelpers
from UtilityFunctions import CommonHelpers

class Word_2_Vec:
    def __init__(self):
        self.google_corpus_path = "models/GoogleNews-vectors-negative300.bin"
        self.num_features=300
        self.tf_idf = Tf_Idf.TF_IDF()
        self.tf_idf.init_data_from_pickle()
        self.weighted_avg=True

    def set_weighted_avg(self,set=True):
        self.weighted_avg=set


    def set_model(self):
        self.model_google = KeyedVectors.load_word2vec_format(self.google_corpus_path,binary=True)
        self.index2word_set = set(self.model_google.index_to_key)  # words known to the model

    def set_data(self,doc_list):
        self.doc_list = doc_list
    
    def make_feature_vector(self,words,doc_key,query=False):
        """
        Average the word vectors for a set of words
        """
        feature_vec = np.zeros((self.num_features,),dtype="float32")  # pre-initialize (for speed)
        n_words = 0
    
        for word in words:
            if word in self.index2word_set: 
                n_words = n_words + 1
                word_vec = self.model_google[word]
                if self.weighted_avg == True and query==False:
                    tf_score=  self.tf_idf.get_tf_idf_score(word,doc_key)
                    word_vec=word_vec*tf_score
                feature_vec = np.add(feature_vec,word_vec)
        
        feature_vec = np.divide(feature_vec, n_words)
        return feature_vec


    def get_avg_feature_vectors(self):
        """
        Calculate average feature vectors for all books
        """
        counter = 0
        self.feature_vectors = {}  # pre-initialize (for speed)
        for doc in self.doc_list:
            self.feature_vectors[doc] = self.make_feature_vector(self.doc_list[doc],doc)
            counter = counter + 1
        CommonHelpers.dump_pickle("data/word2vec/feature_vectors.pickle",self.feature_vectors)
        return self.feature_vectors

    def init_data_from_pickle(self):
        self.feature_vectors=CommonHelpers.load_pickle("data/word2vec/feature_vectors.pickle")
        self.set_model()

    def get_query_vectors(self,query_words):
        return self.make_feature_vector(query_words,None,True)


    def cosine_similarity(self,doc1,doc2):
        return spatial.distance.cosine(doc1,doc2)

    def get_top_n_documents(self,query):
        similar_docs={}
        preprocessor = PreprocessHelpers.Preprocessor()
        preprocessor.set_text(query)
        cleaned_query = preprocessor.run_lemma_pipeline(True)
        query_vec = self.get_query_vectors(cleaned_query)
        for each in self.feature_vectors:
            similar_docs[each] = self.cosine_similarity(self.feature_vectors[each],query_vec)

        result = {k: v for k, v in sorted(similar_docs.items(), key=lambda item: item[1],reverse=True)}
        return result

    
        


