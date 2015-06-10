
import commons, graph, keywords, pagerank_weighted, summarizer, textcleaner
from collections import Counter

def textrank_keyphrase(text):

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = commons.build_graph([ syntacticUnit for syntacticUnit in text])
    summarizer._set_graph_edge_weights(graph)
    # Remove all nodes with all edges weights equal to zero.
    commons.remove_unreachable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    pagerank_scores = summarizer._pagerank(graph)

    results = []
    for su in text:
        score = (1-pagerank_scores[su.label, su.index]) if (su.label, su.index) in pagerank_scores.keys() else 0.0
        results.append(Counter({ 'TEXTRANK_SCORE': score }))
    return results


##### TODO - not done yet
def lexrank_keyphrase(text):

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = commons.build_graph([ syntacticUnit for syntacticUnit in text])
    summarizer._set_lex_graph_edge_weights(graph)
    # Remove all nodes with all edges weights equal to zero.
    commons.remove_unreachable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    pagerank_scores = summarizer._pagerank(graph)

    results = []
    for su in text:
        score = (1-pagerank_scores[su.label, su.index]) if (su.label, su.index) in pagerank_scores.keys() else 0.0
        results.append(Counter({ 'LEXRANK_SCORE': score }))
    return results

def textrank_keyword(text):
    txt = u' '.join([ su.text for su in text ])
    # Gets a dict of word -> lemma
    tokens = textcleaner.clean_text_by_word(text, 'english')
    split_text = list(textcleaner.tokenize_by_word(txt))

    # Creates the graph and adds the edges
    graph = commons.build_graph(keywords._get_words_for_graph(tokens))
    keywords._set_graph_edges(graph, tokens, split_text)
    del split_text # It's no longer used
    commons.remove_unreachable_nodes(graph)

    # # Ranks the tokens using the PageRank algorithm. Returns dict of lemma -> score
    pagerank_scores = keywords._pagerank_word(graph)
    extracted_lemmas = keywords._extract_tokens(graph.nodes(), pagerank_scores, 0.2, None)
    lemmas_to_word = keywords._lemmas_to_words(tokens)
    keyWords = keywords._get_keywords_with_score(extracted_lemmas, lemmas_to_word)
    # # text.split() to keep numbers and punctuation marks, so separeted concepts are not combined
    combined_keywords = keywords._get_combined_keywords(keyWords, txt.split())
    kw_scores = keywords._format_results(keyWords, combined_keywords, False, True)

    results = [ Counter({ 'TEXTRANK_KEYWORD_SCORE': keyword_mean_score(su.basic, kw_scores) }) for su in text ]
    return results

def keyword_mean_score(sentence, wordScores):
    totalScore = sum([ s for w, s in wordScores if w in sentence ])
#     print sentence.split()
    if not sentence.split(): return 0.0
    return totalScore / len(sentence.split())

