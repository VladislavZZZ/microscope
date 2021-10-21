

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
            lexem_line = self.file.readline().replace('\n','').split(' ')
            lexems.append(lexem_line)
        return lexems


    def get_matrix_with_percentage(self):
        data = dict()
        count = int(self.file.readline())
        for i in range(count):
            key, matr = self.file.readline().split('-> [')
            matr = matr[:-2]
            elems = matr.split('); ')
            m = []
            for elem in elems:
                if elem == '':
                    continue
                if elem.endswith(');'):
                    elem = elem[:-2]
                first, second = elem.split(": ")[0], int(elem.split(" (")[1])
                m.append([first,second])
            data[key] = m
        return data


    def read_lines(self):
        return self.file.readlines()

    def read_single_line(self):
        return self.file.readline()

    def close(self):
        self.file.close()