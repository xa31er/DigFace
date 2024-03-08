class Parser(object):
    def __init__(self):
        self.file = None
        self.result_file = None
        self.inst_dict = {
            "Nop": "00",
            "Add": "01",
            "Sub": "02",
            "And": "03",
            "Nand": "04",
            "Or": "05",
            "Nor": "06",
            "Xor": "07",
            "Xnor": "08",
            "Not": "09",
            "Asr": "0A",
            "Lsl": "0B",
            "Lsr": "0C",
            "Swap": "0D",
            "SwapN": "0E",
            "Ldi": "0F",
            "Lda": "10",
            "Sta": "11",
            "Ldp": "12",
            "Stp": "13",
            "Jmp": "14",
            "Bif": "15",
            "Hlt": "16"
        }

    def parse_file(self, file_path, result_file):
        """Loops through all the lines in a file and parses them.

            Arguments:

                file_path (str) : the path to the file to be parsed.
                result_file (str) : the path to the file to write the output to.

            Returns:

                Nothing.
        """
        parsedlines = []
        try:
            self.file = open(file_path, "r")
        except OSError:
            print("File does not exist!")
        try:
            self.result_file = open(result_file, "x")
        except OSError:
            print("Result file already exists!")
        line = self.file.readline()
        if line != "":
            parsedlines.append(self.parse(line))
        else:
            for parsedline in parsedlines:
                self.write_to_result(parsedline)

    def parse(self, line_to_parse):
        """Parses a line to hex code.

            Arguments:

                line_to_parse (str) : the line to be parsed.

            Returns:

                parsedline (str) : The parsed line in hex.
        """
        import re
        parsedline = ""
        for inst in self.inst_dict:
            match = re.match("^"+inst, line_to_parse, re.RegexFlag("g"))
            if match != "":
                parsedline += match
            else:
                continue
        return parsedline

    def write_to_result(self, line_to_write):
        """Writes a line to the result file.

            Arguments:

                line_to_write (str) : the line to write to the file.

            Returns:

                Nothing.
        """
        pass
