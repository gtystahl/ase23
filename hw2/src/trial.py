class A:
    def __init__(self):
        pass

    def sampleFunc(self, arg):
        print("Called arg with ", arg)

getattr(globals()['A'](), 'sampleFunc')()

print("done")