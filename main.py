import re
import pymorphy2

eps = 0.00
class Lexem:

    def __init__(self, text, part_of_speech) -> None:
        self.text = text
        self.part_of_speech = part_of_speech


def set_to_str(cur_set, same_line=True):
    res = ''
    for entity in cur_set:
        if same_line:
            res += ', ' + entity
        else:
            res += ' ' + entity[0] +' - ' +str(entity[1]) +'/'+str(len(requests))+' ('+str(round(entity[1]/len(requests)*100, 4))+'%)\n'
    return res + ';'


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

if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    main_lexems = dict()
    words_len = 0
    all_normed_senteces = []
    with open('results/new_out.txt', 'w+') as out:
        with open('resources/generated_requests.txt', 'r') as req_file:
            requests = req_file.readlines()
            count = 0
            for i, request in enumerate(requests):
                words_len += 1
                splitted_words = re.split('[,.\+](?!\d)|[^\w.,\\\/]+', request.lower())
                low_cased_norm_words = [word for word in splitted_words if word != '']
                # print(low_cased_norm_words)
                morph_norm_words = [morph.parse(word)[0].normal_form for word in low_cased_norm_words]
                morph_norm_words = list(dict.fromkeys(morph_norm_words))
                # main_word = None
                # for main_word in main_words:
                #     for word in morph_norm_words:
                #         if re.search(main_word, word):
                #             main_word = word
                # if not main_word:
                #     continue
                word_num = 0
                full_normed_sentence = []
                while word_num < len(morph_norm_words):
                    norm_word = morph_norm_words[word_num]
                    parsed = morph.parse(norm_word)
                    # print(str(parsed[0].normal_form) + ' -' + str(parsed[0].tag))
                    part_of_speech = re.split('[ ,]+', str(parsed[0].tag))[0]

                    if norm_word in measure_types:
                        word_num += 1
                        continue

                    if part_of_speech == 'PRCL' or part_of_speech == 'PREP' or part_of_speech == 'CONJ':
                        word_num += 1
                        continue

                    # if part_of_speech == 'ADJF' or part_of_speech == 'ADJS':
                    #     characteristicts.add(norm_word)
                    if norm_word in sizes or part_of_speech == 'NUMB':
                        if word_num - 1 >= 0 and morph_norm_words[word_num - 1] in measure_types:
                            norm_word = morph_norm_words[word_num - 1] + ' ' + norm_word
                        if word_num + 1 < len(morph_norm_words) and morph_norm_words[word_num + 1] in measure_types:
                            norm_word = norm_word + ' ' + morph_norm_words[word_num + 1]
                            word_num += 1
                    #     measures.add(norm_word)
                    # else:
                    full_normed_sentence.append(norm_word)
                    if norm_word not in main_lexems.keys():
                        main_lexems[norm_word] = 0
                    main_lexems[norm_word] += 1
                    word_num += 1
                all_normed_senteces.append(full_normed_sentence)
            main_lexems = sorted(main_lexems.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            main_lexems = [main_lexem for main_lexem in main_lexems if main_lexem[1] > eps*words_len]
            out.write(str(len(main_lexems))+'\nLEXEMS:\n' + set_to_str(main_lexems, False))
            most_usable_lexems = [entry[0] for entry in main_lexems]
            synonyms = dict()
            print(str(len(most_usable_lexems))+' MOST USABLE LEXEMES ')
            for ij,most_usable_lexem in enumerate(most_usable_lexems):
                print(str(ij+1)+") LEXEM ")
                most_usable_lexems_copy = most_usable_lexems.copy()
                most_usable_lexems_copy.remove(most_usable_lexem)
                for i, norm_sentence in enumerate(all_normed_senteces):
                    if i%5000==0:
                        print('    '+str(i+1)+' sentences')
                    if most_usable_lexem in norm_sentence:
                        for normed_lexem in norm_sentence:
                            if normed_lexem in most_usable_lexems_copy:
                                most_usable_lexems_copy.remove(normed_lexem)
                synonyms[most_usable_lexem] = most_usable_lexems_copy
    with open('results/synonyms.txt','w+') as out:
        for entry in synonyms.items():
            out.write(entry[0]+' -> '+str(entry[1])+'\n')