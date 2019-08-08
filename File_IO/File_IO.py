class TxtFile:
    def __init__(self):
        # Flag to indicate whether a file has been loaded
        self.fileloaded = False
        # A list will be used to contain contents of file
        self.txt = []


    def load(self, filename):
        ''' load txt file from current directory '''
        self.fileloaded = False

        # try / except used to check to see if file exists
        try:
            txtfile = open(filename, "r")
        except IOError:
            print "txt file does not exist!"
            return
        # loop through the lines in the file and add them to list
        for line in txtfile:
            self.txt.append(line)
        self.fileloaded = True


    def save(self, filename):
        ''' save txt file from current directory '''

        if not self.fileloaded: # check to see if file has been loaded
            print "Error: no file has been loaded!"
            return

        """
            Try / except used to check to see if file exists warning:
            "w" option will overwrite existing file contents if
            IOError is raised, file could not be loaded.
        """
        try:
            txtfile = open(filename, "w")
        except IOError:
            print "Error: txt file could not be saved!"
            return

        # loop through the lines in the file could have used
        # whitelines without loop
        for line in self.txt:
            txtfile.write(line)


    def display(self):
        # check to see if file has been loaded
        if not self.fileloaded:
            print "error no file has been laoded!"
            return
        # loop through list to display contents
        for line in self.txt:
            print line,
        print "working"




class CsvFile:
    def __init__(self):
        # flag to indicate whether a file has been loaded
        self.fileloaded = False
        # a list will be used to contain contents of file
        self.csv = []


    def load(self, filename):
        ''' load csv file from current directory'''
        self.fileloaded = False

        try:
            csvfile = open(filename, 'r')
        except IOError:
            print "csv file does not exist!"
            return
        for line in csvfile:
            self.csv.append(map(int.line.split(",")))
        self.fileloaded = True


    def save(self, filename):
        ''' save csv file from current directory'''
        if not self.fileloaded: # check to see if file has been loaded
            print "Error: No file has been loaded!"
            return
        try:
            csvfile = open(filename, 'w')
        except IOError:
            print "Error, csv file could not be saved!"
            return
        for line in self.csv:
            csvfile.write("".join([str(number)+ "," for number in line])[:-1]+"\n") #python at its best


    def display(self):
        if not self.fileloaded:
            print "error: No file has been loaded!"
            return
        for line in self.csv:
            print line
        print "working"



if __name__ == '__main__':
    txtfile = TxtFile()
    txtfile.load("test.txt")
    txtfile.display()
    txtfile.save("test.txt")

    csvfile = CsvFile()
    csvfile.load("test.csv")
    csvfile.display()
    csvfile.save("test.csv")
