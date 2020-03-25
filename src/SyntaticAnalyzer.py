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
            self._current_value = {'token': '', 'class': '', 'number': ''}
        
        return self._current_value

    def _previous_value(self):
        if self._old_value:
            if self._current_value['token'] != '':
                self._lexical_table.insert(0, self._current_value)
                
            self._current_value = self._old_value
            self._old_value = None

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

    def _sintagma_nominal(self):
        if self._current_value['class'] == "adjetivo":
            self._next_value()
            self._sintagma_adjetival()

            self._next_value()
            if self._current_value['class'] in ['pronome', "substantivo", "adjetivo"]:         
                self._sintagma_nominal()
            else:
                self._previous_value()
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
                print("O verbo auxiliar", self._old_value["token"], "da palavra de nº", self._old_value["number"], "não está precedindo um verbo ", end='')
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
                print("A pontuação final do texto está faltando ", end='')
                raise Exception()

    def analyze_syntax(self):
        self._next_value()
        self._text()
