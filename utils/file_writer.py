from typing import List


class FileWriter:

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.__open_file()

    def __open_file(self):
        self.file = open(self.filepath, 'w+')

    def write_line(self,text):
        self.file.write(text+'\n')

    def save_lexems(self, lexems: List[list]):
        lexems = [x for x in lexems if x != []]
        self.file.write(str(len(lexems)))
        for line in lexems:
            self.file.write('\n')
            self.file.write(line[0])
            for i in range(1,len(line)):
                self.file.write(' '+line[i])

    def save_list_of_dicts(self, list_of_dicts):
        self.file.write(str(len(list_of_dicts)))
        for dictionary in list_of_dicts:
            for key,val in dictionary.items():
                self.file.write(key+' -> '+val+'\n')

    def save_dict_with_stat(self, occurrance: dict):
        self.file.write(str(len(occurrance)))
        for key,val in occurrance.items():
            self.file.write('\n')
            self.file.write(key+": "+str(val))

    def save_matrix_with_full_percentage(self, matr, req_len):
        self.file.write(str(len(matr)))
        for key,val in matr.items():
            self.file.write('\n')
            self.file.write((key+'-> ['))
            for line in val[1]:
                self.file.write(line[0] + ": " + str(round(line[1]/req_len, 3))+' ('+str(line[1])+'); ')
            self.file.write(']')

    def save_matrix_with_percentage(self, matr):
        self.file.write(str(len(matr)))
        for key,val in matr.items():
            self.file.write('\n')
            self.file.write((key+'-> ['))
            count = val[0]
            for line in val[1]:
                self.file.write(line[0] + ": " + str(round(line[1]/count, 3))+' ('+str(line[1])+'); ')
            self.file.write(']')

    def save_dict(self, occurrance: dict):
        self.file.write(str(len(occurrance)))
        for key,val in occurrance.items():
            self.file.write('\n')
            self.file.write(key)

    def save_meeting_vectors(self, meeting_vectors:dict):
        self.file.write(str(len(meeting_vectors))+'\n')
        for key,val in meeting_vectors.items():
            self.file.write(key)
            for i in range(18-len(key)):
                self.file.write(' ')
            self.file.write('[')
            for v  in val:
                self.file.write(str(round(v,3)))
                for kk in range(6 - len(str(round(v,3)))):
                    self.file.write(' ')
            self.file.write(']\n')

    def save_dist_matrix(self, matrix):
        self.file.write(str(len(matrix))+'\n')
        for i,(lexem, line) in enumerate(matrix.items()):
            self.file.write(str(lexem))
            for k in range(18-len(lexem)):
                self.file.write(' ')
            for j in range(i+1):
                self.file.write(str(line[j]))
                for kk in range(6 - len(str(line[j]))):
                    self.file.write(' ')
            self.file.write('\n')

    def save_lexem_groups(self, lexem_groups:dict):
        self.file.write(str(len(lexem_groups))+'\n')
        for key, vals in lexem_groups.items():
            self.file.write(str(key)+ ' -> ')
            for val in vals:
                self.file.write(str(val)+', ')
            self.file.write('\n')

    def close(self):
        self.file.close()