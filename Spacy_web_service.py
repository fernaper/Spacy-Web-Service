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
    This is a method that works like an Api Rest.
    It receives a json with the text you want to parse and, optionally, with
    a language (if you do not send the language, it will use the last one).
    Returns a json with two lists, one of edges and one of nodes, as well as
    all the attributes that may be useful.
'''
@post('/spacy/parse')
def parse():
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
        nodes = []
        edges = []
        for word in tree:
            edges.append({'parent': word.i, 'child':word.left_edge.i, 'dep':word.left_edge.dep_})
            edges.append({'parent': word.i, 'child':word.right_edge.i, 'dep':word.right_edge.dep_})
            
            nodes_dict = {'text':word.text}
            nodes_dict.update({'text_with_ws':word.text_with_ws})
            nodes_dict.update({'whitespace_':word.whitespace_})
            nodes_dict.update({'orth':word.orth})
            nodes_dict.update({'orth_':word.orth_})
            nodes_dict.update({'head':word.head.ent_id})
            nodes_dict.update({'left_edge':word.left_edge.i})
            nodes_dict.update({'right_edge':word.right_edge.i})
            nodes_dict.update({'i':word.i})                         # -> This is what I'm using as id
            nodes_dict.update({'ent_type':word.ent_type})
            nodes_dict.update({'ent_type_':word.ent_type_})
            nodes_dict.update({'ent_iob':word.ent_iob})
            nodes_dict.update({'ent_iob_':word.ent_iob_})
            nodes_dict.update({'ent_id':word.ent_id})
            nodes_dict.update({'ent_id_':word.ent_id_})
            nodes_dict.update({'lemma':word.lemma})
            nodes_dict.update({'lemma_':word.lemma_})
            nodes_dict.update({'norm':word.norm})
            nodes_dict.update({'norm_':word.norm_})
            nodes_dict.update({'lower':word.lower})
            nodes_dict.update({'lower_':word.lower_})
            nodes_dict.update({'shape':word.shape})
            nodes_dict.update({'shape_':word.shape_})
            nodes_dict.update({'prefix':word.prefix})
            nodes_dict.update({'prefix_':word.prefix_})
            nodes_dict.update({'suffix':word.suffix})
            nodes_dict.update({'suffix_':word.suffix_})
            nodes_dict.update({'is_alpha':word.is_alpha})
            nodes_dict.update({'is_ascii':word.is_ascii})
            nodes_dict.update({'is_digit':word.is_digit})
            nodes_dict.update({'is_lower':word.is_lower})
            #nodes_dict.update({'is_upper':word.is_upper})
            nodes_dict.update({'is_title':word.is_title})
            nodes_dict.update({'is_punct':word.is_punct})
            nodes_dict.update({'is_left_punct':word.is_left_punct})
            nodes_dict.update({'is_right_punct':word.is_right_punct})
            nodes_dict.update({'is_space':word.is_space})
            nodes_dict.update({'is_bracket':word.is_bracket})
            nodes_dict.update({'is_quote':word.is_quote})
            nodes_dict.update({'like_url':word.like_url})
            nodes_dict.update({'like_num':word.like_num})
            nodes_dict.update({'like_email':word.like_email})
            nodes_dict.update({'is_oov':word.is_oov})
            nodes_dict.update({'is_stop':word.is_stop})
            nodes_dict.update({'pos':word.pos})
            nodes_dict.update({'pos_':word.pos_})
            nodes_dict.update({'tag':word.tag})
            nodes_dict.update({'dep':word.dep})
            nodes_dict.update({'dep_':word.dep_})
            nodes_dict.update({'lang':word.lang})
            nodes_dict.update({'lang_':word.lang_})
            nodes_dict.update({'prob':word.prob})
            nodes_dict.update({'idx':word.idx})
            nodes_dict.update({'sentiment':word.sentiment})
            nodes_dict.update({'lex_id':word.lex_id})
            nodes_dict.update({'rank':word.rank})
            nodes_dict.update({'cluster':word.cluster})            
            nodes.append(nodes_dict)
        
        full = dict(nodes=nodes)
        full.update(dict(edges=edges))
    
        # I join all the dictionaries in one
        full.update({'start':tree.start})
        full.update({'end':tree.end})
        full.update({'start_char':tree.start_char})
        full.update({'end_char':tree.end_char})
        full.update({'text':tree.text})
        full.update({'text_with_ws':tree.text_with_ws})
        #full.update({'orth':tree.orth}) # v2.0
        full.update({'orth_':tree.orth_})
        full.update({'label':tree.label})
        full.update({'label':tree.label_})
        full.update({'lemma_':tree.lemma_})
        full.update({'ent_id':tree.ent_id})
        full.update({'ent_id_':tree.ent_id_})
        full.update({'sentiment':tree.sentiment})
        #vocab = tree.doc.vocab
        #full.update({'vocab':[{'strings':vocab.strings.string},{'vectors_length':vocab.length}]})
        sents.append(full)
    
    return dict(data=sents)

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
    run(host='localhost', port=8080, debug=True, reloader=True)