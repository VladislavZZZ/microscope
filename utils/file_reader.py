

class FileReader:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.__open_file()

    def __open_file(self):
        self.file = open(self.filepath,'r')

    def read_lexems(self):
        count = int(self.file.readline())
        lexems = []
        for i in range(count):
            lexem_line = self.file.readline().split(' ')
            lexems.append(lexem_line)
        return lexems

    def read_lines(self):
        return self.file.readlines()

    def read_single_line(self):
        return self.file.readline()

    def close(self):
        self.file.close()