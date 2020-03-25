from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import nltk
#Donwload das palavras definidas para stopwords no nltk
nltk.download('stopwords')
pd.set_option('display.max_columns', 500)

class BagOfWords:
    def __init__(self, input_path, language):
        input_text = []
        documents = ["document1"]
        with open(input_path, 'r', encoding='utf-8') as file:
            text_line = ""
            for line in file:
                text_line += line
            input_text = [text_line]
        # Construção do vetorizador, ele terá as palavras presentes em todos os documentos no input
        # junto também definimos quais serão as palavras ignoradas para fazer o bag of word, por serem
        # irrelevantes a maioria dos modelos, vamos pegar a padronização disponível na biblioteca nltk
        vectorizer = CountVectorizer(input_text, stop_words = nltk.corpus.stopwords.words(language))
        #Geração da vetorização do texto e get do array respectivo
        doc_array = vectorizer.fit_transform(input_text).toarray()

        self._bagOfWords = pd.DataFrame(doc_array,index=documents,columns=vectorizer.get_feature_names())


    def get_bag_of_words(self):
        return self._bagOfWords

    def print_bag_of_words(self):
        print(self._bagOfWords)

# BagOfWords("../data/input.txt", 'english').print_bag_of_words()