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


Com o texto checado a partir das técnicas de analise gramatical e léxicas aprendidas durante a disciplina de compiladores, caso nenhuma exceção venha a aparecer, a linguagem presente no texto está definida corretamente, logo podemos a usar como entrada para um modelo de machine Learning.

Entretanto, os modelos de machine learning que realizam o processamento de texto, demandam uma estrutura organizada de entrada de forma que ele possa performar encima desses dados, ao invés apenas do texto bruto, uma das formas que são usadas para estruturar esses dados é o que chamamos de **Bag of Words**, nela nos agrupamos a quantidade de ocorrências de uma palavras em um pedaço de texto. Ela é chamada de "Bag", pois toda a informação da estrutura do texto ou ordem que as palavras estão presentes no texto é descartado, o modelo apenas se preocupará quando alguma palavra aparece no texto, mas não onde ela se localiza.

Para realizar a contagem, primeiramente transformamos todas as palavras em um token numeral e então realizamos sua contagem com o auxilio de uma função de vetorização do **Sklearn**. Para a geração do **Bag of Words** uma coisa que os estudos atuais tem demonstrado grande impacto na melhora da performance do modelo é quando essa entrada não está levando em consideração stopwords, como artigos ou preposições, por isso usamos a listagem de stopwords disponíveis para download através do **Nltk** ou **Natural Language Toolkit**.

# Analise de uso

Um texto, após passar pelas etapas desenvolvidas nesse projeto, estaria tanto com uma gramática de português apta para analise, quanto com um formato de input aceitável para as técnicas de machine learning hoje vigentes no mercado para processamento de textos.

Existem várias técnicas hoje no mercado para o aprendizado de máquina, como Naive Bayes ou Support Vector Machine, entretanto, atualmente uma das abordagens que vem trazendo mais resultados são de uma ramificação do machine learning chamado deep learning, sendo dessa área o algoritmo de Redes Neurais recorrentes as que tem trazido maiores resultados para o processamento de texto.

 ## Rede Neural
Primeiro precisamos entender o que é uma rede neural para entender a base de uma rede recorrente. Uma rede neural pode ser entendida como um conjunto de combinações lineares. Observe a figura 1, nela cada nó de entrada(nós roxos) são multiplicado por um peso que estão representados nas arestas entre os nós, sendo que, em cada neurônio(nós azuis escuros) eles são combinados em um valor a partir de uma soma
![Imagem 1 - Exemplo de rede neural](https://miro.medium.com/fit/c/1838/551/1*ySYgu-DDvVjKU_rW_g-pUA.jpeg)

Isso vai acontecendo sequencialmente até a camada de saída(nó azul ciano), onde todas essas somas são combinadas a partir uma função de a ativação e esse resultado é interpretado em uma classificação ou regressão.

![Imagem 2 - Sigmoid Function](https://image.slidesharecdn.com/nlppresentation-171127220207/95/aprendizado-de-mquina-em-linguagem-natural-9-638.jpg?cb=1512141144)

Vários inputs são passados por essas redes, várias vezes de forma a cada vez mais obter arestas que quando multiplicados aos valores presentes nos nós, cheguem mais próximos de um valor real, isso é executado a partir de um algoritmo chamado backpropagation, onde o erro de uma atribuição é passado para as arestas de maneira a corrigir as inferências.

## Redes Neurais Recursivas

Uma rede neural recursiva pode ser entendida como uma redes neural com memória de estado anterior, onde entre as conexões dos nós, o resultado é retroalimentado formando uma espécie de loop no próprio, assim o próximo valor daquele neurônio tem sempre como base um valor prévio, como pode ser visto na imagem 3.

![Imagem 3](https://www.researchgate.net/profile/Lei_Tai/publication/311805526/figure/fig3/AS:667790805565446@1536225143793/Recurrent-Neural-Network-Structure-The-left-is-the-typical-RNN-structure-The-right-part.png)

A partir disso a aplicação em documentos, em que geramos diversos vetores de bag of words, podem ser usados para retroalimentar um próximo vetor, logo uma ou várias sentenças anteriores, podem ser levadas em consideração na hora de avaliar a validade de uma outra, fazendo a analise de um documento contar não só com o vetor atual de um bag of words, mas de anteriores também.

Com isso em mente, várias aplicaçes onde a analise de vários documentos são necessrios poderia ser possível, a partir de um conjunto de treinamento adequado, vejamos aqui quais seriam interessantes aplicações para essas técnicas.


## Classificação de documentos

A partir do uso dessas técnicas, um classificador de documento autônomo passa a ser viabilizado, aqui teríamos a analise se o texto de fato compreende uma linguagem passível de leitura correta, a partir dos analisadores sintático e léxico, além da classificação correspondente do documento com um modelo de machine learning, em especial sendo o Rnn previamente explicado, executando encima do bag of words que podemos oferecer.

## Auditor Computadorizado
 
Instituições como o TCU(Tribunal de Contas da União) e TCE(Tribunal de contas do Estado) são organizações responsáveis da fiscalização fiscal contábil e financeira do dinheiro público, isso se é possível ao realizar a investigação dos documentos referentes a operações financeiras.
Devido a grande quantidade de documentação pública e movimentações financeiras que acontecem diariamente. 

Uma aplicação que seja capaz de realizar uma triagem automatizada dessa documentação, procurando inconsistências nos registros ou situações fora do padrão, traria grande economia de tempo e eficiência de processos, para os auditores.

## Analise jurídica preliminar

Uma outra situação que poderíamos processar informações de texto e aumentar a eficiência de processos é no setor de defesa jurídica, que assim como no caso da auditoria de contas, tem seus integrantes desperdiçando grande parte dos seus recursos de tempo e dinheiro analisando centenas de documentos, aonde uma ferramenta que faça a analise textual poderia facilitar esse processo e trazer apenas os trechos de importante leitura.
