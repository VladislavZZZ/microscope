import re
import time
import numpy as np

import pymorphy2
from typing import List

from fonetika.soundex import RussianSoundex
from fonetika.distance import PhoneticsInnerLanguageDistance

from operator import itemgetter

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
    'номер',
    'мм',
    'см',
    'шт',
    'тип',
    'ширина',
    'р',
    'разм'
}


class TextParser:

    def __init__(self) -> None:
        self.morph = pymorphy2.MorphAnalyzer()
        self.soundex = RussianSoundex(delete_first_letter=True)
        self.phon_distance = PhoneticsInnerLanguageDistance(self.soundex)

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

    def delete_main_lexem(self,all_lexems, MAIN_LEXEMS):
        cleared_all_lexems = []
        for lexems in all_lexems:
            cleared_lexems = []
            for lexem in lexems:
                if lexem not in MAIN_LEXEMS:
                    cleared_lexems.append(lexem)
            cleared_all_lexems.append(cleared_lexems)
        return cleared_all_lexems


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
            word_num += 1
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

    def remove_rare(self, occurence: dict, requests_count, eps=0.01):
        main_lexems = list(occurence.items())
        main_lexems = [main_lexem for main_lexem in main_lexems if main_lexem[1] > eps * requests_count]
        return dict(main_lexems)

    def find_words_with_no_common(self, occurence, all_normed_sentences):
        words_with_no_common = dict()
        lexems = list(occurence.keys())
        for i, lexem in enumerate(lexems):
            lexems_copy = [[lexem1, 0] for lexem1 in lexems if lexem1 != lexem]
            full_lexems_info = [0, lexems_copy]
            for i, norm_sentence in enumerate(all_normed_sentences):
                if lexem in norm_sentence:
                    full_lexems_info[0]+=1
                    for normed_lexem in norm_sentence:
                        found_lexem = [item for item in lexems_copy if normed_lexem == item[0]]
                        if len(found_lexem) > 0:
                            found_lexem[0][1] += 1
            # words_with_no_common[lexem] = sorted(lexems_copy, key=itemgetter(1), reverse=True)
            words_with_no_common[lexem] = full_lexems_info
        return words_with_no_common


    def get_synonyms_full_vectors(self, dict_of_syns: dict, req_size, edge):
        vector_dict = dict()
        keys = list(dict_of_syns.keys())
        for key, val in dict_of_syns.items():
            vector = [0 for i in range(len(keys) - 1)]
            for lex in keys:
                for i, entry in enumerate(val[1]):
                    if entry[0] == lex and entry[1] / req_size < edge:
                        vector[i] = 1
            vector_dict[key] = vector
        for i in range(len(keys)):
            vector_dict[keys[i]].insert(i, 1)
        return vector_dict

    def get_synonyms_vectors(self, dict_of_syns: dict, edge):
        vector_dict = dict()
        keys = list(dict_of_syns.keys())
        for key, val in dict_of_syns.items():
            vector = [0 for i in range(len(keys) - 1)]
            count = val[0]
            for lex in keys:
                for i, entry in enumerate(val[1]):
                    if entry[0] == lex and entry[1] / count < edge:
                        vector[i] = 1
            vector_dict[key] = vector
        for i in range(len(keys)):
            vector_dict[keys[i]].insert(i, 1)
        return vector_dict

    def get_synonyms_vectors_decimal(self, dict_of_syns: dict):
        vector_dict = dict()
        keys = list(dict_of_syns.keys())
        for key, val in dict_of_syns.items():
            vector = [0. for i in range(len(keys) - 1)]
            count = val[0]
            for lex in keys:
                for i, entry in enumerate(val[1]):
                    if entry[0] == lex :
                        vector[i] = entry[1] / count
            vector_dict[key] = vector
        for i in range(len(keys)):
            vector_dict[keys[i]].insert(i, 1)
        return vector_dict

    def get_dist_between_vectors(self, dict_of_vectors: dict):
        distance_matrix = dict()
        for lexem, vector in dict_of_vectors.items():
            vector = np.array(vector)
            distance_list = []
            for vector2 in dict_of_vectors.values():
                vector2 = np.array(vector2)
                distance_list.append(round(np.linalg.norm(vector2 - vector),3))
            distance_matrix[lexem] =distance_list
        return distance_matrix

    def find_similar_lexems_by_dist(self, distances: dict,lexems:list, similarity_edge:float):
        similarity_groups = dict()
        for key, vals in distances.items():
            lexem_group = []
            for i, val in enumerate(vals):
                if val < similarity_edge and lexems[i]!=key:
                    lexem_group.append(lexems[i])
            similarity_groups[key] = lexem_group
        return similarity_groups

    def replace_to_synonym(self, all_lexems: List[list], synonyms: dict):
        st_time = time.time()
        all_synonyms_lexems = []
        for lexems in all_lexems:
            synonyms_lexems = []
            for lexem in lexems:
                has_found = False
                for syn_key in synonyms.keys():
                    if lexem in synonyms[syn_key]:
                        synonyms_lexems.append(syn_key)
                        has_found = True
                        break
                if not has_found:
                    print(lexem, "was not found")
                    synonyms_lexems.append(lexem)
            print('lexems size', len(lexems))
            print('synonems lexems size', len(synonyms_lexems))
            all_synonyms_lexems.append(synonyms_lexems)
        print("time is, ", time.time() - st_time)

        return all_synonyms_lexems

    def clear_similar_words(self, occurence: dict, num_of_non_proc_lexems):
        lexems = list(occurence.keys())
        pure_lexems = lexems[:num_of_non_proc_lexems]
        raw_lexems = lexems[num_of_non_proc_lexems::]
        changes = []
        for raw_lexem in raw_lexems:
            for pure_lexem in pure_lexems:
                if len(raw_lexem) > 5 and self.get_fonetika_distance(raw_lexem, pure_lexem) < 2:
                    changes.append({raw_lexem: pure_lexem})
                    # lexems.remove(raw_lexem)
                    try:
                        occurence.pop(raw_lexem, False)
                    except Exception:
                        print("exception", raw_lexem)
        return changes, occurence

    def get_fonetika_distance(self, word1, word2):
        try:
            return self.phon_distance.distance(word1, word2)
        except Exception:
            print("Exteption in dist", word1, "and", word2)
            return 5

    def get_fonetika_codec(self, word):
        return self.soundex.transform(word)
