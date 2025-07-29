import abc


class WriteStream:
    def __init__(self, writepath=None, print=False):
        self.writepath = writepath
        self.print = print
        self.buffer = []

    def write(self, data):
        if self.print is True:
            print(data)
        else:
            self.buffer.append(data)

    def flush(self):
        if self.writepath is not None:
            with open(self.writepath, "w") as f:
                for data in self.buffer:
                    f.write(data)
                    f.write("\n")
        else:
            print('\n'.join(self.buffer))
