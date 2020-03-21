# Introdução

## Descrição
O projeto aqui descrito é relativo a avaliação final da disciplina de Construção de Compiladores I do curso de Ciência da Computação da Universidade Federal da Paraíba (UFPB) ministrada pelo professor Clauirton de Albuquerque Sierra e serve como uma introdução para uma análise mais complexa de textos da língua portuguesa, utilizando uma verificação e extração de palavras através de um molde similar ao funcionamento de um compilador com o objetivo de pré-processar essas palavras e fazer a verificação da sintaxe do texto para checar se ela está correta para possibilitar que futuramente isso sirva como entrada de um modelo de inteligência artificial. 

## Dependências
Além do **Python 3** e seu pacote de módulos padrões, as únicas bibliotecas externas necessárias para executar o programa são as do **SpaCy**, **Sklearn** e **Nltk**, junto das importações que as acompanham.

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

## Bag of Words

Com o texto checado a partir das técnicas de analise gramátical e léxicas aprendidas durante a disciplina de compiladores, caso nenhuma exceção venha a aparecer, a linguagem presente no texto está definida corretamente, logo podemos a usar como entrada para um modelo de machine Learning.
Entretanto, os modelos de machine learning que realizam o processamento de texto, demandam uma estrutura organizada de entrada de forma que ele possa performar encima desses dados, ao invés apenas do texto bruto, uma das formas que são usadas para estruturar esses dados é o que chamamos de **Bag of Words**, nela nos agrupamos a quantidade de ocorrências de uma palavras em um pedaço de texto. Ela é chamada de "Bag", pois toda a informação da estrutura do texto ou ordem que as palavras estão presentes no texto é descartado, o modelo apenas se preocupará quando alguma palavra aparece no texto, mas não onde ela se localiza.
Para realizar a contagem, primeiramente transformamos todas as palavras em um token numeral e então realizamos sua contagem com o auxilio de uma função de vetorização do **Sklearn**. Para a geração do **Bag of Words** uma coisa que os estudos atuais tem demonstrado grande impacto na melhora da performace do modelo é quando essa entrada não está levando em consideração Stopwords, como artigos ou preposições, por isso usamos a listagem de stopwords disponveis para download através do **Nltk** ou **Natural Language Toolkit**.

# Analise de uso

## Classificação de documentos
 
A partir do uso dessas tecnicas, um classificador de documento automizatizado passa a ser viabilizado, aqui teriamos a analise se o texto de fato compreende uma linguagem passível de leitura correta, a partir dos analisadores sintático e léxico, além da classificação correspondente do documento com um modelo de machine learning executando encima do bag of words que podemos oferecer.

## Auditor Computadorizado
 
Instituições como o TCU(Tribunal de Contas da União) e TCE(Tribunal de contas do Estado) são organizações responsáveis da fiscalização fiscal contábil e financeira do dinheiro público, isso se é possível ao realizar a investigação dos documentos referentes a operações financeiras.
Devido a grande quantidade de documentação pública e movimentações financeiras que acontecem diariamente. Uma aplicação que seja capaz de realizar uma triagem automatizada dessa documentação, procurando inconsistências nos registros ou situações fora do padrão, traria grande economia de tempo e eficiência de processos, para os auditores.

## Analise jurídica preliminar

Uma outra situação que poderíamos processar informações de texto e aumentar a eficiência de processos é no setor de defesa jurídica, que assim como no caso da auditoria de contas, tem seus integrantes desperdiçando grande parte dos seus recursos de tempo e dinheiro analisando centenas de documentos, aonde uma ferramenta que faça a analise textual poderia facilitar esse processo e trazer apenas os trechos de importante leitura.
