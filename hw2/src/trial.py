# This is my trial program to check out things I am unsure of. 
# It can be ignored

class A:
    def __init__(self):
        pass

    def sampleFunc(self, arg):
        print("Called arg with ", arg)

getattr(globals()['A'](), 'sampleFunc')()

print("done")