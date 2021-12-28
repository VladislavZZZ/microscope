from elasticsearch import Elasticsearch
import datetime
import json
import requests as req
from utils.text_parser import TextParser
from utils.file_reader import FileReader
from utils.file_writer import FileWriter

DATA_PATH = 'resources/fullrequests.txt'
RESULT_PATH = 'results/elastic_parsed.txt'
INDEX_NAME = 'rustest'
HOSTPORT = 'http://localhost:9200'
HEADERS = {'content-type': 'application/json'}
ANALYZER_NAME = "my_analyzer"
ANALYZER_PATTERN = {
    "settings": {
        "analysis": {
            "analyzer": {
                ANALYZER_NAME: {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "my_stopwords", "russian_stemmer"]
                }
            },
            "filter": {
                "my_stopwords": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            }

        }
    }
}


def create_index(url, index, is_use_russ_morph=False):
    data = {}
    if is_use_russ_morph:
        data = ANALYZER_PATTERN
    resp = req.put(url + '/' + index, data=json.dumps(data), headers=HEADERS)
    return resp.status_code, resp


def get_analyzed_text(url, index, text):
    data = {
        "analyzer": ANALYZER_NAME,
        "text": text
    }
    resp = req.post(url + '/' + index + '/_analyze', data=json.dumps(data), headers=HEADERS)
    if resp.status_code != 200:
        return resp, ""
    data = json.loads(resp.content)
    if len(data['tokens']) == 0:
        return ""
    normed_text = ''
    for token in data['tokens']:
        normed_text += token['token'] + ' '
    return resp, normed_text[:-1]


def insert_request_to_es(es: Elasticsearch, index, text, doc_index):
    data = {
        'request': text
    }
    try:
        es.index(index=index, id=doc_index, document=data)
    except Exception:
        print("ERROR while insert : " + str(doc_index) + ": " + text)
        exit()

    # print('id - ', res['_id'], ' ', text, ' was ', res['result'])


if __name__ == '__main__':
    cur_datetime = datetime.datetime.now()

    es = Elasticsearch(HOSTPORT)
    parser = TextParser()

    in_txt = FileReader(DATA_PATH)
    requests = in_txt.read_lines()
    in_txt.close()

    print('creating index...')
    status, info = create_index(HOSTPORT, INDEX_NAME, is_use_russ_morph=True)

    if status != 200:
        print('Something went wrong: ' + info.text)
    else:
        print("Success!")

    out_txt = FileWriter(RESULT_PATH)
    print('analyze and insert...')
    for i, request in enumerate(requests):
        if i % 100 == 1:
            print(str(datetime.datetime.now()) + ': ' + str(i) + ' requests done..')
        info, normed_request = get_analyzed_text(HOSTPORT, INDEX_NAME, request)
        if info.status_code != 200:
            print('ERROR while analyzing: ' + info.text)
            exit()
        out_txt.write_line(normed_request)
        insert_request_to_es(es, INDEX_NAME, normed_request, doc_index=i)
    out_txt.close()

    print(str(datetime.datetime.now() - cur_datetime) + " took time")
