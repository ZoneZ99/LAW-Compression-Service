class InputFile:
    def __init__(self, raw_file, filename):
        self.raw_file = raw_file
        self.filename = filename


class OutputFile:
    def __init__(self, compressed_file, filename):
        self.compressed_file = compressed_file
        self.filename = filename
