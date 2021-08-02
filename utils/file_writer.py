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
        self.file.write(str(len(lexems)))
        for line in lexems:
            self.file.write('\n')
            self.file.write(line[0])
            for i in range(1,len(line)):
                self.file.write(' '+line[i])
    def close(self):
        self.file.close()