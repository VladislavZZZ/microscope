from elasticsearch import Elasticsearch
import datetime
from utils.text_parser import TextParser
from utils.file_reader import FileReader
from utils.file_writer import FileWriter

datetime = datetime.datetime


def send_query(es: Elasticsearch, query: dict, index: str, size=1000, from_index=0):
    return es.search(index=index, query=query, size=size, from_=from_index)


def clear_similar_words(es: Elasticsearch, index: str, text_field: str, occurence: dict, num_of_non_proc_lexems):
    lexems = list(occurence.keys())
    pure_lexems = lexems[:num_of_non_proc_lexems]
    lexems_info = dict()
    result = dict()
    for pure_lexem in pure_lexems:
        pure_lexem_similarity = []
        q = {"match": {
            text_field: pure_lexem
        }}
        res = send_query(es, q, index)
        if res['timed_out']:
            print('time out on query ' + pure_lexem)
            return dict()
        for r in res['hits']['hits']:
            pure_lexem_similarity.append((r['_score'], r['_source'][text_field]))
        lexems_info[pure_lexem] = (res['hits']['total']['value'], res['hits']['total']['relation'])
        result[pure_lexem] = pure_lexem_similarity
    return result, lexems_info


def get_norm_requests(parser: TextParser):
    time1 = datetime.now()

    in_txt = FileReader('results/2021-09-09 21:03:47.785009_normalized_strings.txt')
    print('get_lexems_from_text')
    lexems = parser.get_lexems_from_text(in_txt.read_lines())
    in_txt.close()

    print('normalized_strings', datetime.now() - time1)

    return lexems


def fill_lexems_into_el(es: Elasticsearch, parser: TextParser):
    lexems = get_norm_requests(parser)

    out_txt = FileWriter(f'results/{cur_datetime}_2.unique_lexems_ABS.txt')
    print('get_percentage_of_occurrence')
    raw_occurrence = parser.get_percentage_of_occurrence(lexems)
    out_txt.save_dict_with_stat(raw_occurrence)
    out_txt.close()

    for i, lexem in enumerate(raw_occurrence.keys()):
        request = lexem.replace('\n', '')
        data = {
            'lexem': request,
            'upload_datetime': datetime.now()
        }
        res = es.index(index='lexems', id=i, document=data)
        print('id - ', res['_id'], ' ', lexem, ' was ', res['result'])
    es.indices.refresh(index="lexems")


if __name__ == '__main__':
    cur_datetime = datetime.now()

    es = Elasticsearch()
    parser = TextParser()

    out_txt = FileWriter(f'results/{cur_datetime}_13.ElasticSearch_similarity_detection.txt')
    lexems = get_norm_requests(parser)
    raw_occurrence = parser.get_percentage_of_occurrence(lexems)
    occurrence = parser.remove_rare(raw_occurrence, len(lexems))
    res, info = clear_similar_words(es, 'lexems', 'lexem', occurrence, len(occurrence.keys()))

    out_txt.save_elasticSearch_results(res, info)
    out_txt.close()

    # q = {"match": {
    #     "lexem": "перчатка"
    # }}
    #
    # res = send_query(es,q,'lexems')
    # print("done")

# inp = FileReader('resources/fullrequests.txt')
#
# requests = inp.read_lines()
#
# for i, request in enumerate(requests):
#     request = request.replace('\n','')
#     data = {
#         'request':request,
#         'upload_datetime': datetime.datetime.now()
#     }
#     res = es.index(index='requests', id=i, document=data)
#     print('id - ',res['_id'],' was ',res['result'])


# body = {
#     "from":0,
#     "size":0,
#     "query": {
#         "match": {
#             "sentence":"Перчатки"
#         }
#     }
# }
# res = es.search(index="requests", query={"match": {
#             "request":"размер"
#
#         }},size=1000, from_=0)
# # es.indices.refresh(index="requests")
# # res = es.get(index='requests', id=1567)
# print('Found')


# es = Elasticsearch()
#
# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.datetime.now(),
# }
# res = es.index(index="test-index", id=1, body=doc)
# print(res['result'])
#
# res = es.get(index="test-index", id=1)
# print(res['_source'])
#
# es.indices.refresh(index="test-index")
#
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

# print(es.get(index="requests",id='1'))
