import os

class LogReader:

    def __init__(self, path=os.getcwd(), mask='*.log'):
        self.path = path
        self.mask = mask
        self.log_filenames = None
        self.txt_files = None

    def __iter__(self):
        for file in self.txt_files:
            for l in file:
                yield l.rstrip('\n')

    def __enter__(self):
        try:
            self.log_filenames = sorted([f for f in os.listdir(self.path) if f[-4:] == self.mask[-4:]])
            self.txt_files = list(map(lambda x: open(os.path.join(self.path, x), 'r'), self.log_filenames))
            return self
        except Exception as ex:
            print(ex)

    def __exit__(self, exp_type, exp_value, exp_tr):
        if self.txt_files:
            for file in self.txt_files:
                file.close()
    @property
    def files(self):
        return self.log_filenames


with LogReader() as logreader:
    for line in logreader:
        print(line)

    print('Logfiles names get by property:', logreader.files )