Spacy-Web-Service
=================

v1.1.0 - Release

Made by: Fernando Pérez <fernaperg@gmail.com>

Web Service that allows to perform all the Natural Language Processing (NLP) through the Spacy library without needing to have it installed or to program with python.

Documentation
-------------

Allowed calls:
	
- /spacy/parse
This is the most important method. It works as an ApiRest web service.
Receives a json with a text (and if you want, a language) and return all the relevant information.

	Return:
	- A dictionary with the key "data" and value, the list of atributtes for each sentence.
 
 	- For each sentence, the spacy atributtes: start, end, start_char, end_char, text, text_with_ws, orth_, label, label_, lemma, ent_id, ent_id_, sentiment and, a list of nodes and a list of edges.
 
 	- For each node (word): text, text_with_ws, whitespace_, orth, orth_, head, left_edge, right_edge, i, ent_type, ent_type_, ent_iob, ent_iob_, ent_id, ent_id_, lemma, lemma_, norm, norm_, lower, shape, shape_, prefix, prefix_, suffix, suffix_, is_alpha, is_ascii, is_digit, is_lower, is_title, is_punct, is_left, is_left_punct, is_right_punct, is_space, is_bracket, is_quote, like_url, like_num, like_email, is_oov, is_stop, pos, pos_, tag, dep, dep_, lang, lang_, prob, idx, sentiment, lex_id, rank and cluster.
 
 	- For each edge (relation): parent, child and dep (Ej: ADJ,...)

- /spacy/set_language/<param>
Change the server language to the one indicated by the parameter.

- /spacy/parse_text
It takes a json file with a text and return those text separated into phrases.
If you do not pass a phrase, it gives you back the last text that you passed spearated into phrases.

- /spacy/get_tags
It takes a json file with a phrase and returns each word with his tag.

Requeriments
------------
We recommend using [conda](https://conda.io/docs/) to install all the dependencies in a virtual environment.

- [Python](https://www.python.org/) >= 3.4
- [SpaCy] (https://spacy.io/) 1.* < 2.0
- [DocOpt] (http://docopt.org/) >= 0.6.2
- [Bottle] (https://bottlepy.org/) >= 0.12.9

Author
------

Fernando Pérez Gutiérrez <fernaperg@gmail.com>