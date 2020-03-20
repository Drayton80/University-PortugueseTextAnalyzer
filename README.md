# Introdução

## Descrição
O projeto aqui descrito serve como uma introdução para uma análise mais complexa de texto da língua portuguesa, utilizando uma verificação e extração de palavras através de um molde similar ao funcionamento de um compilador com o objetivo de pré-processar essas palavras e fazer a verificação da sintaxe do texto para checar se ela está correta para futuramente esses dados servirem como entrada para um modelo de inteligência artificial. 

## Dependências
Além do **Python 3** e seu pacote de módulos padrões, a única biblioteca externa necessária para executar o programa é a **SpaCy** e as importações que acompanham ela.

# Aplicação

## Analisador Léxico
Nessa classe situa-se os métodos que geram uma tabela com os **tokens** e **classes gramaticais** de cada palavra e sinais de pontuação presentes no texto dado como entrada.

Para a geração dessa tabela foi usado o módulo de **Processamento Natural de Linguagem (NLP)** da língua portuguesa disponibilizado pela **SpaCy**. Escolhemos ele pois sua análise para definir a classe gramatical de cada palavra é feita checando a posição da palavra na frase e verificando as demais palavras anteriores e posteriores a ela, assim obtendo uma acurácia maior nessa definição. Além disso, a biblioteca utiliza essa mesma checagem de contexto para separar cada token presente no texto, separando cada palavra e sinais com uma boa precisão. Porém, foi necessário fazer um tratamento prévio no texto transformando a maioria das palavras para a sua forma no singular já que isso melhora a acurácia na definição correta da classe gramatical do SpaCy.

É dentro dessa classe em que é aplicado  a **lematização dos verbos** utilizando um dos retornos do método de NLP do SpaCy em conjunto com uma checagem simples da classe retornada por ele. Além disso, é feito também a **não inclusão de stopwords** na tabela de retorno através de uma checagem da classe gramatical do token e comparação dele com uma lista de contrações e artigos da língua portuguesa.

## Analisador Sintático