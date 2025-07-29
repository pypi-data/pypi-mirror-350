SERMetric:

SERMetirc is an open-source library for evaluating how easy-to-read a text is. It supports a wide variety of indexes and allows the user to easily combine them. 


FEATURES:

Several indexes are provided:

* pointsIndex: it is the number of points in the text divided by the number of words.
* newParagraphIndex: it is the number of new paragraphs in the text divided by the number of words.
* CommaIndex: the number of commas in the text divided by the number of words.
* extensionIndex: ratio between the number of syllables in lexical words and the number of lexical words, lexical words being understood  as nouns, verbs, adjectives and adverbs.
* triPoliIndex: ratio of the number of trisyllabic and polysyllabic words to the number of lexical words.
* lexicTriPoliIndex: ratio of the  number of trisyllabic and polysyllabic lexical  words to the numberof lexical words.
* diversityIndex: ratio between the  number of different words in the text and the total number of words.
* lexicalFreqIndex: ratio between the number of low-frequency lexical words and the number of lexical words. The "Corpus de la Real Academia Española" (CREA) and the 'Gran diccionario del uso del español actual' will be used as a reference.
* wordForPhraseIndex: quotient resulting from the division between the number of words in the text and the number of sentences.
* sentenceComplexityIndex: the result of dividing the number of sentences by the number of propositions.
* complexityIndex: quotient between the number of low-frequency syllables and the total number of syllables (reference: 'Diccionario de frecuencias de las unidades lingüísticas del castellano')
* fernandezHuerta: is the result of 206.84-0.6P-1.02F, where P is the number of syllables per 100 words  and F is the number of sentences per 100 words.