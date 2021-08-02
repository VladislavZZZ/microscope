import requests
path = 'http://synonyms.iba1d.icdc.io/'


class IBA_Synonyms:

    def __init__(self) -> None:
        self.root_path = path

    def get_all_synonyms(self):
        resp = requests.get(self.root_path+'all', )
        print(resp.status_code)
        data = resp.json()
        print(data)
        return data

    def get_word_synonyms(self, word: str):
        resp = requests.get(self.root_path+'all/'+word)
        print(resp.status_code)
        data = resp.json()
        print(data)
        return data

    def add_new_word_group(self, word: str):
        resp = requests.post(self.root_path+'add/'+word+'&')
        print(resp.status_code)
        data = resp.json()
        print(data)
        return data

    def add_synonym_to_word(self, word: str, synonym: str):
        resp = requests.post(self.root_path + 'add/' + word + '&'+synonym)
        print(resp.status_code)
        data = resp.json()
        print(data)
        return data

    def delete_word(self, word: str):
        resp = requests.delete(self.root_path + 'delete/' + word)
        print(resp.status_code)
        data = resp.json()
        print(data)
        return data