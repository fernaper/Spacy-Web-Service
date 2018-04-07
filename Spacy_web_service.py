from bottle import run, get, post, request
import spacy

'''
    GLOBAL VARIABLES
'''
# Sometimes, it simply does this work unnecessarily, but when necessary it makes a quicker response
lang = 'en'
nlp = spacy.load(lang)
parse = None

'''
    Create a natural language processing object in the language indicated by parameter
'''
@get('/spacy/set_language/<param>')
def set_language(param):
    # If it is already preprocessed, it does not repeat the job
    global lang
    
    if param == lang:
        return {'data':True}
    
    try:
        global nlp 
        nlp = spacy.load(param)
    except:
        return {'data':False}
    
    lang = param;
        
    return {'data':True}

@post('/spacy/get_span')
def get_span():
    text = request.json.get('text')
    local_lang = request.json.get('lang')
    
    # If yoy pass a new lang at the same time
    if local_lang != None and local_lang != lang:
        try:
            global nlp
            nlp = spacy.load(local_lang)
        except:
            pass
    
    try:
        global parse
        parse = nlp(text)
    except:
        return {}
    
    sents = []
    for tree in parse.sents:
        # Span
        full = dict(text=[word.text for word in tree])
        root = dict(root=[{word.text:word.head.text} for word in tree])
        atr_start = {'start':tree.start}
        atr_end = {'end':tree.end}
        atr_start_char = {'start_char':tree.start_char}
        atr_end_char = {'end_char':tree.end_char}
        atr_text = {'full_text':tree.text}
        atr_text_with_ws = {'full_text_with_ws':tree.text_with_ws}
        #atr_orth = {'orth':tree.orth} # v2.0
        atr_orth_ = {'orth_':tree.orth_}
        atr_label = {'label':tree.label}
        atr_label_ = {'label':tree.label_}
        atr_lemma_ = {'lemma_':tree.lemma_}
        atr_ent_id = {'ent_id':tree.ent_id}
        atr_ent_id_ = {'ent_id_':tree.ent_id_}
        atr_sentiment = {'sentiment':tree.sentiment}
        # Doc.vocab
        #vocab = tree.doc.vocab
        #atr_vocab = {'vocab':[{'strings':vocab.strings.string},{'vectors_length':vocab.length}]}
    
        # I join all the dictionaries in one
        full.update(root)
        full.update(atr_start)
        full.update(atr_end)
        full.update(atr_start_char)
        full.update(atr_end_char)
        full.update(atr_text)
        full.update(atr_text_with_ws)
        #full.update(atr_orth) # v2.0
        full.update(atr_orth_)
        full.update(atr_label)
        full.update(atr_label_)
        full.update(atr_lemma_)
        full.update(atr_ent_id)
        full.update(atr_ent_id_)
        full.update(atr_sentiment)
        #full.update(atr_vocab)
        sents.append(full)
    
    return dict(data=sents)

'''
    It takes a json file with a text and return thosw text separated into phrases.
    
    INPUT
    Key: text
    Valute: "..."
    
    OUTPUT
    Key: data
    Value: ["...", ... ,"..."]
    
    If you do not send a json or send an incorrect json, it returns {}.
'''
@post('/spacy/parse_text')
def parse_text():
    text = request.json.get('text')
    try:
        global parse
        parse = nlp(text)
    except:
        parse = None
            
    return dict(data=[str(s) for s in list(parse.sents)]) if parse != None else {}


'''
    Returns the previously parsed text
'''
@get('/spacy/parse_text')
def parsed_text():
    return dict(data=[str(s) for s in list(parse.sents)]) if parse != None else {}

'''
    It takes a json file with a phrase and returns each word with his tag.
    
    INPUT
    Key: text
    Valute: "..."
    
    OUTPUT
    Key: each word
    Value: what tag
'''
@post('/spacy/get_tags')
def get_tags():
    text = request.json.get('text')
    global parse
    parse = nlp(text)
    ans = {}
    for word in list(parse.sents)[0]:
        ans.update({str(word):str(word.tag_)})
    
    return ans if ans != None else {}

@get('/spacy/get_tags')
def get_current_tags():
    ans = {}
    if parse != None:
        for word in list(parse.sents)[0]:
            ans.update({str(word):str(word.tag_)})
    return ans

'''
    Main
'''
if __name__ == "__main__":
    run(host='localhost', port=8081, debug=True)