from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.qparser.dateparse import DateParserPlugin

import nltk
from nltk.corpus import stopwords


def tokenize(raw):
    """
    Function to get tokens from the query text
    :param raw: the query text
    :return: the processed tokens
    """
    tokens = nltk.word_tokenize(raw)  # isolate single words
    return tokens


def lemmatize(tokens):
    """
    Function to delete the stopwords and lemmatize the tokens from the original query
    :param tokens: words to analyze from the query
    :return: a list of words yet to finish their processing phase
    """

    wln = nltk.WordNetLemmatizer()

    list_words = [wln.lemmatize(t) for t in tokens if t not in stopwords.words('english')]  # delete stopwords
    return list_words


def processer(query_string):
    tokens = tokenize(query_string)
    query_string = ""
    for w in lemmatize(tokens):     # for each lemmatized word
        query_string += w + " "    # add it to the final query object
    # print(query, '\n')  # TODO: Delete this print statement when the query process is finished

    ix = open_dir("../index")  # open the index and assign it to "ix"

    qparser = QueryParser("path", ix.schema)
    query = qparser.parse(u"https://www.esa.int")
    print(query)

    parser = MultifieldParser(["title", "content", "date"],
                              ix.schema)  # setting the query parse with the specified field of the schema
    parser.add_plugin(DateParserPlugin(free=True))   # Add the DateParserPlugin to the parser
    user_query = parser.parse(query_string)  # parsing the query and returning a query object to search (use "date:")

    sources = query.Term()

    results = {}
    with ix.searcher() as searcher:
        result = searcher.search(user_query, filter=query)  # search the query
        # print(result[0:])  # print the top 10 results
        results = [{f:i[f] for f in i.fields()} for i in result]
    
    return results


"""def main():
    # processer(query)


if __name__ == '__main__':
    main()
"""