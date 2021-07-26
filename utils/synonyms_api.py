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