class FileWriter:

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.__open_file()

    def __open_file(self):
        self.file = open(self.filepath, 'w+')

    def write_line(self,text):
        self.file.write(text+'\n')

    def close(self):
        self.file.close()