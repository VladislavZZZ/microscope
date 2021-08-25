import re

import pymorphy2

main_words = {
    'перчатка'
}

sizes = {
    'xs',
    's',
    'm',
    'м',
    'l',
    'xl',
    'xxl'
}

measure_types = {
    'размер',
    'номер'
    'мм',
    'см',
    'шт'
}




class TextParser:

    def __init__(self) -> None:
        self.morph = pymorphy2.MorphAnalyzer()

    def set_to_str(self, data, requests_count, same_line=True):
        res = ''
        for entity in data:
            if same_line:
                res += ', ' + entity
            else:
                res += ' ' + entity[0] + ' - ' + str(entity[1]) + '/' + str(requests_count) + ' (' + str(
                    round(entity[1] / requests_count * 100, 4)) + '%)\n'
        return res + ';'

    def get_lexems_from_text(self, text):
        all_lexems = []
        for sentence in text:
            all_lexems.append(self._get_lexems_from_sentence(sentence))
        return all_lexems

    def _get_lexems_from_sentence(self, sentence):
        splitted_words = re.split('[,.\+](?!\d)|[^\w.,\\\/]+', sentence.lower())
        low_cased_norm_words = [word for word in splitted_words if word != '']
        morph_norm_words = [self.morph.parse(word)[0].normal_form for word in low_cased_norm_words]
        morph_norm_words = list(dict.fromkeys(morph_norm_words))
        word_num = 0
        full_normed_sentence = []
        while word_num < len(morph_norm_words):
            norm_word = morph_norm_words[word_num]
            parsed = self.morph.parse(norm_word)
            part_of_speech = re.split('[ ,]+', str(parsed[0].tag))[0]
            if norm_word in measure_types:
                word_num += 1
                continue
            if part_of_speech == 'PRCL' or part_of_speech == 'PREP' or part_of_speech == 'CONJ':
                word_num += 1
                continue
            if norm_word in sizes or part_of_speech == 'NUMB':
                if word_num - 1 >= 0 and morph_norm_words[word_num - 1] in measure_types:
                    norm_word = morph_norm_words[word_num - 1] + ' ' + norm_word
                if word_num + 1 < len(morph_norm_words) and morph_norm_words[word_num + 1] in measure_types:
                    norm_word = norm_word + ' ' + morph_norm_words[word_num + 1]
                    word_num += 1
            full_normed_sentence.append(norm_word)
            word_num+=1
        return full_normed_sentence

    def get_percentage_of_occurrence(cls, all_lexems):
        occurrence = dict()
        for lexems in all_lexems:
            for lexem in lexems:
                if lexem not in occurrence.keys():
                    occurrence[lexem] = 0
                occurrence[lexem] += 1
        sorted_occurrence = dict(sorted(occurrence.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
        return sorted_occurrence

    def remove_rare(self, occurence: dict, requests_count,  eps=0.01):
        main_lexems = list(occurence.items())
        main_lexems = [main_lexem for main_lexem in main_lexems if main_lexem[1] > eps * requests_count]
        return dict(main_lexems)

    def find_words_with_no_common(self, occurence, all_normed_sentences):
        words_with_no_common = dict()
        lexems = list(occurence.keys())
        for i, lexem in enumerate(lexems):
            lexems_copy = lexems.copy()
            lexems_copy.remove(lexem)
            for i, norm_sentence in enumerate(all_normed_sentences):
                if lexem in norm_sentence:
                    for normed_lexem in norm_sentence:
                        if normed_lexem in lexems_copy:
                            lexems_copy.remove(normed_lexem)
            words_with_no_common[lexem] = lexems_copy
        return words_with_no_common