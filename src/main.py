import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.LexicalAnalyzer import LexicalAnalyzer
from src.SyntaticAnalyzer import SyntaticAnalyzer


if __name__ == '__main__':
    table = LexicalAnalyzer('../data/input.txt').create_table()
    
    for element in table:
        print(element)

    try:
        SyntaticAnalyzer('../data/input.txt').text()
        print('O texto não possui qualquer erro sintático')
    except Exception as e:
        print('O texto está escrito com uma sintaxe incorreta.')

    