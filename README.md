# Spacy-Web-Service

v1.0.0 - Release

Made by: Fernando Pérez <fernaperg@gmail.com>

Web Service that allows to perform all the Natural Language Processing (NLP) through the Spacy library without needing to have it installed or to program with python.

   Allowed calls:
	- /spacy/set_language/<param>
      Change the server language to the one indicated by the parameter.
      
	- /spacy/get_span (The most important)
      Receive a json with a text (and if you want a language) and return all the relevant information with Spacy calculations for that phrase.
      
	- /spacy/parse_text
      It takes a json file with a text and return those text separated into phrases.
      If you do not pass a phrase, it gives you back the last text that you passed spearated into phrases.
      
	- /spacy/get_tags
      It takes a json file with a phrase and returns each word with his tag.
