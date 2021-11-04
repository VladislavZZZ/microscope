from utils.file_reader import FileReader
from utils.file_writer import FileWriter
from utils.text_parser import TextParser
from utils.synonyms_api import IBA_Synonyms
from utils.synonyms_excel import SynonymsExcel
from fonetika.soundex import RussianSoundex
from  fonetika.distance import PhoneticsInnerLanguageDistance
import datetime


# CONSTANTS
MINIMUM_RAW_OCCURANCE = 1
COUNT_LEXEMS_NOT_PROC_FONETIKA = 1000
SYNONYMS_EDGE = 0.001
MEETING_EDGE = 0.2
VECT_DIST_1 = 0.7
VECT_DIST_2 = 0.9
MAIN_LEXEMS = ['перчатка']

datetime = datetime.datetime

def change_lexems_by_synonym(lexems, number_of_synonym:int):
    new_lexems = []
    for line in lexems:
        new_line = []
        for lexem in line:
            synonym = api.get_word_synonyms(lexem)[number_of_synonym]
            new_line.append(synonym)
        new_lexems.append(new_line)
    return new_lexems


if __name__ == '__main__':
    cur_datetime = datetime.now()
    # cur_time = datetime.time()
    api = IBA_Synonyms()

    time1 = datetime.now()

    # in_txt = FileReader('resources/fullrequests.txt')
    # out_txt = FileWriter(f'results/{cur_datetime}_normalized_strings.txt')
    # print('get_lexems_from_text')
    parser = TextParser()
    # lexems = parser.get_lexems_from_text(in_txt.read_lines())
    # in_txt.close()
    # out_txt.save_lexems(lexems)
    # out_txt.close()
    #
    # print('normalized_strings', datetime.now() - time1)
    #
    # time1 = datetime.now()
    #
    # out_txt = FileWriter(f'results/{cur_datetime}_1.normalized_strings_without_synonyms.txt')
    # excel = SynonymsExcel('synonyms/synonyms_lexems.xlsx')
    # synonyms = excel.get_synonyms(38)
    # lexems = parser.replace_to_synonym(lexems, synonyms)
    # out_txt.save_lexems(lexems)
    # out_txt.close()
    #
    fr = FileReader('results/2021-09-10 20:01:35.285461_normalized_strings_without_synonyms.txt')
    lexems = fr.read_lexems()
    fr.close()

    lexems = parser.delete_main_lexem(lexems, MAIN_LEXEMS)

    out_txt = FileWriter(f'results/{cur_datetime}_2.unique_lexems_ABS.txt')
    print('get_percentage_of_occurrence')
    raw_occurrence = parser.get_percentage_of_occurrence(lexems)
    out_txt.save_dict_with_stat(raw_occurrence)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_5.unique_lexems_REL.txt')
    print('remove_rare')
    occurrence = parser.remove_rare(raw_occurrence, len(lexems))
    out_txt.save_dict_with_stat(occurrence)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_6a.meetings_matrix.txt')
    with_no_common = parser.find_words_with_no_common(occurrence,lexems)
    out_txt.save_matrix_with_full_percentage(with_no_common, len(lexems))
    out_txt.close()


    out_txt = FileWriter(f'results/{cur_datetime}_6.meetings_matrix.txt')
    with_no_common = parser.find_words_with_no_common(occurrence, lexems)
    out_txt.save_matrix_with_percentage(with_no_common)
    out_txt.close()

    # fr = FileReader('results/2021-09-10 20:01:35.285461_normalized_strings_without_synonyms.txt')
    # lexems = fr.read_lexems()
    # fr.close()
    #
    #
    # fr = FileReader('results/2021-09-21 13:45:24.640982_meetings_matrix.txt')
    # with_no_common = fr.get_matrix_with_percentage()
    # fr.close()

    out_txt = FileWriter(f'results/{cur_datetime}_7a.meetings_vectors.txt')
    vectorsA = parser.get_synonyms_full_vectors(with_no_common,len(lexems),SYNONYMS_EDGE)
    out_txt.save_meeting_vectors(meeting_vectors=vectorsA)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_7.meetings_vectors.txt')
    vectors = parser.get_synonyms_vectors(with_no_common, SYNONYMS_EDGE)
    out_txt.save_meeting_vectors(meeting_vectors=vectors)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_8a.meetings_vectors_distance.txt')
    dist_vectors_matr = parser.get_dist_between_vectors(vectorsA)
    out_txt.save_dist_matrix(dist_vectors_matr)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_8.meetings_vectors_distance.txt')
    dist_vectors_matr = parser.get_dist_between_vectors(vectors)
    out_txt.save_dist_matrix(dist_vectors_matr)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_9.similar_lexems_with_edge_{VECT_DIST_1}.txt')
    lexems_similarity = parser.find_similar_lexems_by_dist(dist_vectors_matr,list(occurrence.keys()),VECT_DIST_1)
    out_txt.save_lexem_groups(lexems_similarity)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_9.similar_lexems_with_edge_{VECT_DIST_2}.txt')
    lexems_similarity = parser.find_similar_lexems_by_dist(dist_vectors_matr, list(occurrence.keys()), VECT_DIST_2)
    out_txt.save_lexem_groups(lexems_similarity)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_10.meetings_vectors_decimal.txt')
    vectors = parser.get_synonyms_vectors_decimal(with_no_common)
    out_txt.save_meeting_vectors(meeting_vectors=vectors)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_11.meetings_vectors_distance.txt')
    dist_vectors_matr = parser.get_dist_between_vectors(vectors)
    out_txt.save_dist_matrix(dist_vectors_matr)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_12.similar_lexems_with_edge_{VECT_DIST_1}.txt')
    lexems_similarity = parser.find_similar_lexems_by_dist(dist_vectors_matr, list(occurrence.keys()), VECT_DIST_1)
    out_txt.save_lexem_groups(lexems_similarity)
    out_txt.close()

    out_txt = FileWriter(f'results/{cur_datetime}_12.similar_lexems_with_edge_{VECT_DIST_2}.txt')
    lexems_similarity = parser.find_similar_lexems_by_dist(dist_vectors_matr, list(occurrence.keys()), VECT_DIST_2)
    out_txt.save_lexem_groups(lexems_similarity)
    out_txt.close()

    # out_txt = FileWriter('results/products_microscope_with_syns.txt')
    # changed_lexems = change_lexems_by_synonym(lexems, 0)
    # out_txt.save_lexems(changed_lexems)
    # out_txt.close()