import re
import pymorphy2


class Lexem:

    def __init__(self, text, part_of_speech) -> None:
        self.text = text
        self.part_of_speech = part_of_speech

def set_to_str(cur_set, same_line=True):
    res = ''
    for entity in cur_set:
        if same_line:
            res += ', '+entity
        else:
            res += ' '+entity+'\n'
    return res+';'

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
    'мм',
    'см',
    'шт'
}

if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    main_characteristicts = set()
    main_measures = set()
    main_others = set()
    with open('results/out.txt', 'w+') as out:
        with open('results/detailed_out.txt', 'w+') as det_out:
            with open('resources/fullrequests.txt', 'r') as req_file:
                requests = req_file.readlines()
                count = 0
                for i, request in enumerate(requests):
                    det_out.write('--------------------------------------\n'+str(i+1)+') '+request+'\n')
                    splitted_words = re.split('[,.\+](?!\d)|[^\w.,\\\/:]+', request.lower())
                    low_cased_norm_words = [word for word in splitted_words if word != '']
                    print(low_cased_norm_words)
                    morph_norm_words = [morph.parse(word)[0].normal_form for word in low_cased_norm_words]

                    main_word = None
                    for main_word in main_words:
                        for word in morph_norm_words:
                            if re.search(main_word, word):
                                main_word = word
                                morph_norm_words.remove(word)
                    if not main_word:
                        continue
                    characteristicts = set()
                    measures = set()
                    others = set()
                    word_num = 0
                    while word_num < len(morph_norm_words):
                        norm_word = morph_norm_words[word_num]
                        parsed = morph.parse(norm_word)
                        print(str(parsed[0].normal_form) + ' -' + str(parsed[0].tag))
                        part_of_speech = re.split('[ ,]+',str(parsed[0].tag))[0]

                        if norm_word in measure_types:
                            word_num+=1
                            continue

                        if part_of_speech == 'PRCL' or part_of_speech == 'PREP' or part_of_speech =='CONJ':
                            word_num+= 1
                            # if word_num+1<len(morph_norm_words) and (part_of_speech == 'PRCL' or part_of_speech == 'PREP'):
                            #     norm_word += ' '+ morph_norm_words[word_num]
                            #     part_of_speech = re.split('[ ,]+',str(morph.parse(morph_norm_words[word_num])[0].tag))[0]
                            # else:
                            continue

                        if part_of_speech == 'ADJF' or part_of_speech == 'ADJS':
                            characteristicts.add(norm_word)
                        elif norm_word in sizes or part_of_speech == 'NUMB':
                            if word_num-1>=0 and morph_norm_words[word_num-1] in measure_types:
                                norm_word = morph_norm_words[word_num-1] + ' ' + norm_word
                            if word_num+1<len(morph_norm_words) and morph_norm_words[word_num+1] in measure_types:
                                norm_word = norm_word + ' '+ morph_norm_words[word_num+1]
                                word_num+=1
                            measures.add(norm_word)
                        else:
                            others.add(norm_word)
                        word_num += 1
                    det_out.write('MAIN WORD - '+main_word+'\nWORD DESCR - '+set_to_str(characteristicts)+'\nMEASURES - '
                                  + set_to_str(measures)+'\nOTHER - '+set_to_str(others)+'\n')
                    main_measures.update(measures)
                    main_characteristicts.update(characteristicts)
                    main_others.update(others)
                out.write('MAIN WORDS:\n'+set_to_str(main_words,False)+'\n\nWORD DESCR:\n'
                          +set_to_str(main_characteristicts,False)+'\n\nMEASURES:\n'+set_to_str(main_measures,False)
                          +'\n\nOTHERS:\n'+set_to_str(main_others,False))





