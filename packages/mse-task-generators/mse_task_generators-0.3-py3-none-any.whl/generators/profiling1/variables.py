from cfile.core import Variable


class StaticArray(Variable): 
    def __init__(self, name, data_type, size=0):
        super().__init__(name, data_type, array=size)

    def __getitem__(self, index):
        return Variable(f"{self.name}[{index}]", self.data_type)


class Counter(Variable):
    pass