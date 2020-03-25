from LexicalAnalyzer import LexicalAnalyzer

class SyntaticAnalyzer:
    def __init__(self, input_path):
        self._lexical_table = LexicalAnalyzer(input_path).create_table()
        self._current_value = None
        self._old_value = None

    def _next_value(self):
        if self._lexical_table != []:
            self._old_value = self._current_value
            self._current_value = self._lexical_table.pop(0)
        else:
            self._current_value = {'token': '', 'class': '', 'line': ''}

        #print(self._old_value, self._current_value, "\n", sep="\n")
        
        return self._current_value

    def _previous_value(self):
        if self._old_value:
            if self._current_value['token'] != '':
                self._lexical_table.insert(0, self._current_value)
                
            self._current_value = self._old_value
            self._old_value = None

            #print("Previous Value()", self._current_value, "\n", sep="\n")
        
            return self._current_value

    def _sentenca1(self):
        if self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]:
            self._sintagma_nominal()
            
            self._next_value()
            self._sentenca2()


    def _sentenca2(self):
        if self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]:
            self._sintagma_nominal()
            
            self._next_value()
            self._sentenca2()
        if self._current_value['class'] in ['advérbio', "verbo", "verbo auxiliar"]:
            self._sintagma_verbal()
            
            self._next_value()
            self._sentenca2()
        else:
            self._previous_value()
            return

    # Caso haja um if antes do sintagma nominal checando se self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]
    # antes da chamada do método não deve haver um self._next_value()
    def _sintagma_nominal(self):
        if self._current_value['class'] == "adjetivo":
            self._next_value()
            self._sintagma_adjetival()

            self._next_value()
            if self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]:         
                self._sintagma_nominal()
            else:
                return

        elif self._current_value['class'] == "pronome":
            self._next_value()
            if self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]:
                self._sintagma_nominal()
            else:
                self._previous_value()
                return

        elif self._current_value['class'] == "substantivo":
            self._next_value()
            if self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]:
                self._sintagma_nominal()
            else:
                self._previous_value()
                return
        else:
            print("A sentença não possui um sujeito")
            raise Exception()

    def _sintagma_verbal(self):
        if self._current_value['class'] == "advérbio":
            self._next_value()
            self._sintagma_adverbial()
            
            self._next_value()
            self._sintagma_verbal()
        elif self._current_value['class'] == "verbo":
            self._next_value()
            if self._current_value['class'] == "adjetivo":
                self._next_value()
                self._sintagma_adjetival()
            else:
                self._sintagma_verbal()

        elif self._current_value['class'] == "verbo auxiliar":
            self._next_value()
            if self._current_value['class'] == "verbo":
                return
            else:
                print("Verbo auxiliar não é precedido de um verbo")
                raise Exception()
        else:
            self._previous_value()
            return

    def _sintagma_adverbial(self):
        if self._current_value['class'] == "advérbio":
            self._next_value()
            self._sintagma_adverbial()
        else:
            self._previous_value()
            return

    def _sintagma_adjetival(self):
        if self._current_value['class'] == "advérbio":
            self._next_value()
            self._sintagma_adverbial()
            
            self._next_value()
            self._sintagma_adjetival()
        elif self._current_value['class'] == "adjetivo":
            self._next_value()
            self._sintagma_adjetival()
        else:
            self._previous_value()
            return

    def _text(self):
        if self._current_value['class'] == "advérbio":
            self._sintagma_adverbial()

            self._text()
        elif self._current_value['class'] in ['substantivo', 'pronome', 'adjetivo']:
            self._sentenca1()
            
            self._next_value()
            if self._current_value['class'] == 'pontuação':
                self._next_value()
                # Next Sentence da gramática livre de contexto:
                if self._current_value['class'] != '':
                    self._text()
                else:
                    # Caso class seja igual a vazio significa que chegou ao fim do texto
                    return
            else:
                print("Falta de pontuação final")
                raise Exception()

    def analyze_syntax(self):
        self._next_value()
        self._text()
