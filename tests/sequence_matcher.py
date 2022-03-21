from difflib import SequenceMatcher

text = """there are 
some 3rrors in my text
but I cannot find them"""

rus_text = ""

def fuzzy_search(search_key, text, strictness):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        words = line.split()
        for word in words:
            similarity = SequenceMatcher(None, word, search_key)
            print(similarity.ratio())
            if similarity.ratio() > strictness:
                print( " '{}' matches: '{}' in line {}".format(search_key, word, i + 1))


if __name__ == '__main__':
    fuzzy_search('вилка', rus_text, 0.8)
