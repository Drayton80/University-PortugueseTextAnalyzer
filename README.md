# Introdução

## Descrição
O projeto aqui descrito é relativo a avaliação final da disciplina de Construção de Compiladores I do curso de Ciência da Computação da Universidade Federal da Paraíba (UFPB) ministrada pelo professor Clauirton de Albuquerque Sierra e serve como uma introdução para uma análise mais complexa de textos da língua portuguesa, utilizando uma verificação e extração de palavras através de um molde similar ao funcionamento de um compilador com o objetivo de pré-processar essas palavras e fazer a verificação da sintaxe do texto para checar se ela está correta para possibilitar que futuramente isso sirva como entrada de um modelo de inteligência artificial. 

## Dependências
Além do **Python 3** e seu pacote de módulos padrões, a única biblioteca externa necessária para executar o programa é a **SpaCy** e as importações que acompanham ela.

# Aplicação

## Analisador Léxico
Na classe relativa a esse analisador situa-se os métodos que geram uma tabela com os **tokens** e **classes gramaticais** de cada palavra e sinais de pontuação presentes no texto.

Para a geração dessa tabela foi usado o módulo de **Processamento Natural de Linguagem (NLP)** da língua portuguesa disponibilizado pela **SpaCy**. Escolhemos ele pois sua análise para definir a classe gramatical de cada palavra é feita checando a posição da palavra na frase e verificando as demais palavras anteriores e posteriores a ela, assim obtendo uma boa acurácia nessa definição. Porém, antes de aplicar o NLP em si foi necessário fazer um tratamento prévio no texto transformando a maioria das palavras para a sua forma no singular já que isso melhora a porcentagem na definição correta da classe gramatical do SpaCy. Além disso, a biblioteca utiliza essa mesma checagem de contexto para separar cada token presente no texto, separando cada palavra e sinais com uma boa precisão. 

É dentro dessa classe em que é aplicado  a **lematização dos verbos** utilizando um dos retornos do método de NLP em conjunto com uma checagem simples da classe retornada por ele. Assim como é feito também a **não inclusão de stopwords** na tabela de retorno através de uma checagem da classe gramatical do token e comparação dele com uma lista de contrações e artigos da língua portuguesa.

## Analisador Sintático
A classe que representa esse analisador faz a verificação da sintaxe do texto utilizando métodos recursivos que foram implementados com base na **gramática livre de contexto** expressa abaixo a qual tenta simular parcialmente a **gramática portuguesa** no contexto reduzido relativo ao texto simplificado entregue nas especificações do projeto.

*Texto &#8594; SintagmaAdverbial Texto | Sentença pontuação Texto | Sentença pontuação*  
*Sentença &#8594; Sentença SintagmaNominal | Sentença SintagmaVerbal | SintagmaNominal*  
*SintagmaNominal  &#8594; SintagmaAdjetival SintagmaNominal  | substantivo SintagmaNominal  | pronome SintagmaNominal  | substantivo | pronome*  
*SintagmaVerbal &#8594; SintagmaAdverbial SintagmaVerbal | verbo-auxiliar verbo | verbo SintagmaVerbal | verbo SintagmaAdjetival | verbo*  
*SintagmaAdjetival  &#8594; SintagmaAdverbial adjetivo | adjetivo SintagmaAdjetival | ε*  
*SintagmaAdverbial &#8594; advérbio SintagmaAdverbial | advérbio | ε*  

Para adequar a gramática aos métodos de recursão utilizados para a análise sintática foi necessário aplicar o método de desambiguação e remover as recursões à esquerda, transformado a gramática da seguinte forma:

*Texto &#8594; SintagmaAdverbial Texto | Sentença1 pontuação SentençasPosteriores*  
*SentençasPosteriores &#8594; Texto | ε*  
*Sentença1 &#8594; SintagmaNominal Sentença2*  
*Sentença2 &#8594; SintagmaNominal  Sentença2 | SintagmaVerbal Sentença2 | ε*  
*SintagmaNominal  &#8594; SintagmaAdjetival SintagmaNominal  | substantivo SintagmaNominal  | pronome SintagmaNominal  | substantivo | pronome*  
*SintagmaVerbal &#8594; SintagmaAdverbial SintagmaVerbal | verbo-auxiliar verbo | verbo PosteriorVerbo*  
*PosteriorVerbo &#8594; SintagmaVerbal | SintagmaAdjetival | ε*  
*SintagmaAdjetival  &#8594; SintagmaAdverbial adjetivo | adjetivo SintagmaAdjetival | ε*  
*SintagmaAdverbial &#8594; advérbio SintagmaAdverbial | advérbio | ε*  


