import re
import os
import sys
import spacy

sys.path.append(os.path.abspath(os.path.join('..')))


class LexicalAnalyzer:
    def __init__(self, input_path: str):
        with open(input_path, 'r', encoding='utf-8') as file:
            input_text = file.read().replace('\n', ' ')
            nlp = spacy.load('pt_core_news_sm')

        input_text_corrected = ""

        for word in input_text.split(' '):
            if word[-1] in ['.', ',', '!', '?']:
                word = self._convert_plural_to_singular(word[:-1]) + word[-1]
            else:
                word = self._convert_plural_to_singular(word)

            input_text_corrected += word + ' '
        print(input_text_corrected)
        
        self._doc = nlp(input_text_corrected)

    def _replace_characters(self, word, start_index, end_index, new_characters):
        word_characters = list(word)
        word_characters[start_index:end_index] = ''
        i = 0

        for character in list(new_characters):
            word_characters.insert(start_index+i, character)
            i += 1

        word = "".join(word_characters)

        return word

    def _convert_plural_to_singular(self, word):
        if word[-3:] in ['ões', 'ãos', 'ães']:
            return self._replace_characters(word, len(word)-3, len(word), 'ão')
        elif word[-3:] in ['res', 'ses', 'zes']:
            return self._replace_characters(word, len(word)-3, len(word), word[-3])
        elif word[-3:] in ['ais', 'eis', 'éis', 'ois', 'óis', 'uis']:
            return self._replace_characters(word, len(word)-2, len(word), 'l')
        elif word[-2:] == 'ns':
            return self._replace_characters(word, len(word)-2, len(word), 'm')
        elif word[-1] == 's':
            return self._replace_characters(word, len(word)-1, len(word), '')
        else:
            return word            

    def _convert_part_of_speech_spacy_to_portuguese(self, spacy_pos: str) -> str:
        if spacy_pos == 'PROPN':
            part_of_speech = 'nome próprio'
        elif spacy_pos == 'PRON':
            part_of_speech = 'pronome'
        elif spacy_pos == 'ADJ':
            part_of_speech = 'adjetivo'
        elif spacy_pos == 'NOUN':
            part_of_speech = 'substantivo'
        elif spacy_pos == 'ADV':
            part_of_speech = 'advérbio'
        elif spacy_pos == 'VERB':
            part_of_speech = 'verbo'
        elif spacy_pos == 'AUX':
            part_of_speech = 'verbo auxiliar' 
        elif spacy_pos == 'DET':
            part_of_speech = 'determinante'
        elif spacy_pos in ['CONJ', 'CCONJ', 'SCONJ']:
            part_of_speech = 'conjunção'
        elif spacy_pos == 'INTJ':
            part_of_speech = 'interjeição'
        elif spacy_pos == 'ADP':
            part_of_speech = 'preposição'
        elif spacy_pos == 'PUNCT':
            part_of_speech = 'pontuação'
        elif spacy_pos == 'SYM':
            part_of_speech = 'símbolo'
        elif spacy_pos == 'NUM':
            part_of_speech = 'numeral'
        elif spacy_pos == 'SPACE':
            part_of_speech = 'espaçamento'
        else:
            part_of_speech = 'desconhecido'

        return part_of_speech

    def _is_stopword(self, token: str, part_of_speech: str) -> bool:
        portuguese_contractions = [
            'à', 'às', 'ao', 'aos', 'cum', 'do', 'da', 'dos', 'das', 'dum', 'duns', 'duma', 
            'dumas', 'no', 'na', 'nos', 'nas', 'num', 'nuns', 'numa', 'numas', 'pro', 'pra', 
            'pros', 'pras', 'prum', 'pruns', 'pruma', 'prumas', 'pelo', 'pela', 'pelos', 'pelas']
        
        portuguese_articles = ['a', 'o', 'as', 'os', 'em', 'de', 'por']
        
        if part_of_speech in ["conjunção", "preposição", "determinante", "interjeição"]:
            return True
        elif token in portuguese_contractions or token in portuguese_articles:
            return True
        else:
            return False
    
    def create_table(self) -> list:
        table = []
        
        for element in self._doc:
            # Extrai a classe gramátical da palavra e converte para português:
            part_of_speech = self._convert_part_of_speech_spacy_to_portuguese(element.pos_)
            print(element.orth_, element.pos_)

            # Checa se a palavra é um verbo:
            if part_of_speech in ['verbo', 'verbo auxiliar']:
                # Caso seja, extrai o verbo stemizado:
                token = element.lemma_.lower()
            else:
                # Caso contrário, extrai a palavra do token:
                token = element.orth_.lower()

            # Não inclusão das stopwords:
            if self._is_stopword(token, part_of_speech):
                continue

            table.append({'token': token, 'class': part_of_speech})
        
        return table