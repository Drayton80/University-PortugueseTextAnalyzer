import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.LexicalAnalyzer import LexicalAnalyzer
from src.SyntaticAnalyzer import SyntaticAnalyzer
from src.BagOfWords import BagOfWords


if __name__ == '__main__':
    table = LexicalAnalyzer('../data/input.txt').create_table()
    
    print()
    for element in table:
        print(element)

    print()
    BagOfWords('../data/input.txt', 'portuguese').print_bag_of_words()

    syntatic_analyzer = SyntaticAnalyzer('../data/input.txt')

    try:
        syntatic_analyzer.analyze_syntax()
        print('\nO texto não possui qualquer erro sintático')
    except Exception as e:
        print('e, devido a esse motivo, o texto está escrito com uma sintaxe incorreta.')

    